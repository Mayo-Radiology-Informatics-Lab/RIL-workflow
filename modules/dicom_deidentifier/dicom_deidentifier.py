import subprocess
import argparse
import os
import shutil
import logging


def setup_logger():
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def convert_dicom_to_nifti(dicom_dir, output_dir):
    output_nifti_dir = os.path.join(output_dir, 'nifti')
    os.makedirs(output_nifti_dir, exist_ok=True)

    dcm2niix_path = shutil.which('dcm2niix')

    if not dcm2niix_path:
        logging.error("Error: dcm2niix not found in the system PATH.")
        return

    command = [
        dcm2niix_path,
        '-z', 'y',
        '-f', '%i_%g_%p_%t_%s',
        '-o', output_nifti_dir,
        dicom_dir
    ]

    try:
        result = subprocess.check_output(command, text=True, stderr=subprocess.STDOUT)

        # Get the output file name
        output_file_name = result.strip()

        # Check if the output file exists
        output_file_path = os.path.join(output_nifti_dir, output_file_name)
        if os.path.exists(output_file_path):
            logging.info(f"Conversion successful. Output file: {output_file_path}")
        else:
            logging.error(f"Error: Output file not found at {output_file_path}")

    except subprocess.CalledProcessError as e:
        logging.error(f"Error while running dcm2niix: {e}")
        logging.error(e.output)

def main():
    """
    The purpose of this module is to convert DICOM files to NIfTI format 
    and remove identifying information from the DICOM files.
    """
    
    setup_logger()

    parser = argparse.ArgumentParser(description="Convert DICOM to NIfTI")
    parser.add_argument("-i", "--dicom_dir", required=True, help="Path to the DICOM directory")
    parser.add_argument("-o", "--output_dir", required=True, help="Path to the output directory")
    args = parser.parse_args()

    dicom_dir = os.path.abspath(args.dicom_dir)
    output_dir = os.path.abspath(args.output_dir)

    convert_dicom_to_nifti(dicom_dir, output_dir)


if __name__ == "__main__":
    main()