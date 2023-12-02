#!./.env/bin/python3
import subprocess
import os
import logging
from camunda.external_task.external_task import ExternalTask, TaskResult
from camunda.external_task.external_task_worker import ExternalTaskWorker
from camunda.client.engine_client import EngineClient
from concurrent.futures import ThreadPoolExecutor


# Configure the logging module
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


DEFAULT_CONFIG = {
    "maxTasks": 15,
    "lockDuration": 1000,
    "asyncResponseTimeout": 3000,
    "retries": 4,
    "retryTimeout": 5000,
    "sleepSeconds": 30,
    "isDebug": True,
    "httpTimeoutMillis": 3000,
    "auth_basic": {"username": "TEST", "password": "TEST"} # replace with your credentials
}

WORKFLOW_NAME = "REPLACE_WITH_WORKFLOW_NAME"  # replace with your workflow name


VARS_LIST = []


MODULES_PATH = "REPLACE_WITH_PATH"  # Path to the main directory
FETCHER_PATH = f"{MODULES_PATH}/dicom_fetcher/"  # Path to the fetcher directory
DICOM_DEID_PATH = f"{MODULES_PATH}/dicom_deidentifier/"  # Path to the deidentifier directory
TEXT_DEID_PATH = f"{MODULES_PATH}/text_deidentifier/"  # Path to the text deidentifier directory


def do_dicom_qr(task: ExternalTask) -> TaskResult:
    project_id = task.get_variable("project_id")
    accession_id = task.get_variable("accession_id") or None
    clinic_number = task.get_variable("clinic_id") or None
    exam_date = task.get_variable("exam_date") or None
    modality = task.get_variable("modality") or None
    series_id = task.get_variable("series_id") or None
    study_id = task.get_variable("study_id") or None

    logger.info(f"dicom_ftecher started with: project_id: {project_id}, accession_id: {accession_id}, clinic_number: {clinic_number}, exam_date: {exam_date}")
    try:
        
        # Build the command for DICOM fetcher
        args = ["python3", "fetcher.py", project_id]
        if series_id:
            args.append(["-s", series_id])
        elif study_id:
            args.append(["-S", study_id], ["-m", modality] if modality else [])
        elif accession_id:
            args.append(["-a", accession_id], ["-m", modality] if modality else [])
        elif clinic_number:
            args.append(["-c", clinic_number, "-d", exam_date], ["-m", modality] if modality else [])
        else:
            raise Exception("No search criteria provided")

        logger.info(f"Calling fetcher with args: {args}")

        # Call DICOM fetcher using subprocess.check_output
        subprocess.check_output(args, cwd=FETCHER_PATH, text=True, stderr=subprocess.STDOUT)

        logger.info("DICOM fetcher call completed")

    except subprocess.CalledProcessError as e:
        logger.error(f"DICOM fetcher failed with error: {e.output}")
        raise Exception("DICOM fetcher failed")

    except Exception as e:
        logger.error(f"Exception occurred: {str(e)}")
        return str(e)

    # Check the result of the fetcher
    series_path = os.path.join(FETCHER_PATH, "data", project_id, series_id)
    if os.path.exists(series_path):
        # Send the series path to the next module
        return task.complete({
            "series_path": series_path,
            "project_id": project_id,
            "series_id": series_id,
        })

    else:
        return task.failure(
            error_message="DICOM fetcher failed",
            error_details="DICOM fetcher failed",
            max_retries=DEFAULT_CONFIG["retries"],
            retry_timeout=DEFAULT_CONFIG["retryTimeout"],
        )


def do_DeIDImages(task: ExternalTask) -> TaskResult:
    """"
    This function is called by the Camunda engine to call the DICOM deidentifier and deidentify the DICOM study.
    """
    series_path = task.get_variable("series_path")
    series_id = task.get_variable("series_id")
    project_id = task.get_variable("project_id")
    output_path = task.get_variable("output_path")

    logger.info(f"do_DeIDImages started with series_path: {series_path}")

    try:
        # Call DICOM deidentifier
        args = [
            "python", "dicom_deidentifier.py", 
            "-i", series_path, 
            "-o", output_path
        ]
        logger.info(f"Calling deidentifier with args: {args}")
        subprocess.check_output(args, cwd=DICOM_DEID_PATH, text=True, stderr=subprocess.STDOUT)
        logger.info("DICOM deidentifier call completed")
    
    except subprocess.CalledProcessError as e:
        logger.error(f"DICOM deidentifier failed with error: {e.output}")
        return TaskResult(
            task,
            success=False,
            error_message="DICOM deidentifier failed",
            error_details=str(e),
            max_retries=DEFAULT_CONFIG["retries"],
            retry_timeout=DEFAULT_CONFIG["retryTimeout"],
        )
    
    except Exception as e:
        logger.error(f"Exception occurred: {str(e)}")
        return TaskResult(
            task,
            success=False,
            error_message="Exception occurred during DICOM deidentifier",
            error_details=str(e),
            max_retries=DEFAULT_CONFIG["retries"],
            retry_timeout=DEFAULT_CONFIG["retryTimeout"],
        )

    # Check the result of the deidentifier
    deid_series_path = os.path.join(output_path, series_id)
    if os.path.exists(deid_series_path):
        # Send the deid series path to the next module
        return TaskResult(
            task,
            success=True,
            local_variables={
                "deid_series_path": deid_series_path,
                "project_id": project_id,
                "series_id": series_id,
            },
        )
    else:
        return TaskResult(
            task,
            success=False,
            error_message="DICOM deidentifier failed",
            error_details="DICOM deidentifier failed",
            max_retries=DEFAULT_CONFIG["retries"],
            retry_timeout=DEFAULT_CONFIG["retryTimeout"],
        )


def do_DeIDText(task: ExternalTask) -> TaskResult:
    project_id = task.get_variable("project_id")
    clinic_id = task.get_variable("clinic_id")
    date = task.get_variable("date")
    report_txt = task.get_variable("report_txt")
    report_id = task.get_variable("report_id")
    output_path = task.get_variable("output_path")

    logger.info(f"do_DeIDText started with project_id: {project_id}, clinic_id: {clinic_id}")

    try:
        # Call text deidentifier
        args = [
            "python", "text_deidentifier.py", 
            "-i", report_txt,
            "-o", output_path,
            "-c", clinic_id,
            "-d", date,
            "-r", report_id
        ]
        if clinic_id:
            args.extend(["-c", clinic_id])
        logger.info(f"Calling text deidentifier with args: {args}")
        subprocess.check_output(args, cwd=TEXT_DEID_PATH)
        logger.info("Text deidentifier call completed")

    except subprocess.CalledProcessError as e:
        logger.error(f"Text deidentifier failed with error: {e.output}")
        return TaskResult(
            task,
            success=False,
            error_message="Text deidentifier failed",
            error_details=str(e),
            max_retries=DEFAULT_CONFIG["retries"],
            retry_timeout=DEFAULT_CONFIG["retryTimeout"],
        )
    
    except Exception as e:
        logger.error(f"Exception occurred: {str(e)}")
        return TaskResult(
            task,
            success=False,
            error_message="Exception occurred during text deidentifier",
            error_details=str(e),
            max_retries=DEFAULT_CONFIG["retries"],
            retry_timeout=DEFAULT_CONFIG["retryTimeout"],
        )

    # Check the result of the deidentifier
    deid_text_file = f"{output_path}/{clinic_id}_{date}_{report_id}.npy"
    if os.path.exists(deid_text_file):
        # Send the deid text path to the next module
        return TaskResult(
            task,
            success=True,
            local_variables={
                "deid_text_path": deid_text_file,
                "project_id": project_id,
            },
        )
    else:
        return TaskResult(
            task,
            success=False,
            error_message="Text deidentifier failed",
            error_details="Text deidentifier failed",
            max_retries=DEFAULT_CONFIG["retries"],
            retry_timeout=DEFAULT_CONFIG["retryTimeout"],
        )

    
# Define topics and corresponding routines
TOPICS = ['DICOM_QR', "DeIDImages", "DeIDText"]
ROUTINES = [do_dicom_qr, do_DeIDImages, do_DeIDText]


def handle_task(task: ExternalTask) -> TaskResult:
    for index, topic in enumerate(TOPICS):
        if topic == task.get_topic_name():
            result_message = ROUTINES[index](task)
            if result_message.success:
                return task.complete(...)
            else:
                return task.failure(...)

    # If the task's topic is not found, mark the task as failed
    return task.failure(
        error_message="Unknown topic",
        error_details="Unknown topic",
        max_retries=0,
        retry_timeout=0,
    )


def my_task_worker(worker_id, topic_names):
    ExternalTaskWorker(worker_id=worker_id, config=DEFAULT_CONFIG).subscribe(topic_names=topic_names, action=handle_task)


def main():
    client = EngineClient()
    vars_dict = {var: "Not Set" for var in VARS_LIST}
    resp_json = client.start_process(process_key=WORKFLOW_NAME, variables=vars_dict)

    with ThreadPoolExecutor(max_workers=len(TOPICS) + 2) as executor:
        jobs = []

        for index, topic in enumerate(TOPICS):
            kw = {"worker_id": index, "topic_names": topic}
            args = [DEFAULT_CONFIG]
            jobs.append(executor.submit(my_task_worker, *args, **kw))

if __name__ == '__main__':
    main()