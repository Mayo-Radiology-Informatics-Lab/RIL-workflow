import numpy as np
import argparse
import logging
import tempfile
import subprocess
import os

# Configure the logging module
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TEXT_DEIDENTIFIER_APP = "./app/main.py"

def save_string_to_npy(string_data, file_path):
    """Save a string to a .npy file."""
    bytes_data = string_data.encode('utf-8')
    np_array = np.frombuffer(bytes_data, dtype=np.uint8)
    np.save(file_path, np_array)

def generate_output_file_path(output_dir, clinic_id, date, report_id):
    """Generate the output file path based on clinic_id, date, and report_id."""
    file_name = f"{clinic_id}_{date}_{report_id}.npy"
    return os.path.join(output_dir, file_name)

def de_identify_npy_file(input_file, output_path, de_identify_script=TEXT_DEIDENTIFIER_APP):
    """Call the de-identification script with input and output paths."""
    try:
        args = [de_identify_script, "-i", input_file, "-o", output_path]
        logger.info(f"Calling de-identification script with args: {args}")
        subprocess.check_output(args)

    except subprocess.CalledProcessError as e:
        logger.error(f"De-identification script failed with error: {e.output}")
        raise Exception("De-identification script failed")

    except Exception as e:
        logger.error(f"Exception occurred: {str(e)}")
        raise Exception("De-identification script failed")

def main():
    parser = argparse.ArgumentParser(description="Create and read .npy files with strings.")
    parser.add_argument("-i", "--input_string", required=True, help="The string to store in the .npy file")
    parser.add_argument("-o", "--output_dir", required=True, help="Path to the output directory")
    parser.add_argument("-c", "--clinic_id", required=True, help="Clinic ID")
    parser.add_argument("-d", "--date", required=True, help="Date")
    parser.add_argument("-r", "--report_id", required=True, help="Report ID")

    args = parser.parse_args()

    logger.info(f"Input String: {args.input_string}")
    logger.info(f"Output Directory: {args.output_dir}")
    logger.info(f"Clinic ID: {args.clinic_id}")
    logger.info(f"Date: {args.date}")
    logger.info(f"Report ID: {args.report_id}")

    # Create a temporary folder
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_npy_file = os.path.join(temp_dir, "temp.npy")

        try:
            # Save the string to a temporary .npy file
            save_string_to_npy(args.input_string, temp_npy_file)
            logger.info(f"String saved to temporary file: {temp_npy_file}")

            # Generate the output file path
            output_file_path = generate_output_file_path(args.output_dir, args.clinic_id, args.date, args.report_id)

            # Call de-identification script and store the result in the specified output path
            de_identify_npy_file(temp_npy_file, output_file_path)
            logger.info(f"De-identified data saved to {output_file_path}")

        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
