import re
import os
import sys
import json
import torch
import shutil
import random
import subprocess
import postprocess
from preprocess import preprocess_data, rename_files

def print_and_log(message):
    print(message)
    with open("log.txt", "a") as log_file:
        log_file.write(message + "\n")

def run_command(command):
    try:
        result = subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print_and_log(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print_and_log(f"Error executing command: {command}")
        print_and_log(f"Error message: {e.stderr}")
        return False

def check_directory(directory):
    if not os.path.exists(directory):
        print_and_log(f"Error: Directory '{directory}' does not exist.")
        return False
    if not os.listdir(directory):
        print_and_log(f"Warning: Directory '{directory}' is empty.")
        return False
    return True

def main():
    print_and_log(f"Torch version: {torch.__version__}")
    root_dir = os.path.dirname(__file__)

    os.makedirs(f"{root_dir}/nnUNet_raw_data_base", exist_ok = True)
    os.makedirs(f"{root_dir}/nnUNet_preprocessed", exist_ok = True)

    # Set environment variables
    os.environ['nnUNet_raw_data_base'] = f"{root_dir}/nnUNet_raw_data_base"
    os.environ['nnUNet_preprocessed'] = f"{root_dir}/nnUNet_preprocessed"
    os.environ['RESULTS_FOLDER'] = f"{root_dir}/3d_fullres"

    base_path = os.path.join(root_dir, 'BraTS2024-SSA-Challenge-ValidationData')
    destination_path = os.path.join(root_dir, 'imagesTs')
    prediction_path = os.path.join(root_dir, 'MedNext_Predictions')

    # Preprocessing
    print_and_log("Starting preprocessing...")
    try:
        os.makedirs(destination_path, exist_ok=True)
        preprocess_data(base_path, destination_path)
        rename_files(destination_path)
        if not check_directory(destination_path):
            raise Exception("Preprocessing failed: Output directory is empty or doesn't exist.")
        print_and_log("Preprocessing completed successfully.")
    except Exception as e:
        print_and_log(f"Error during preprocessing: {str(e)}")
        sys.exit(1)

    # Prediction
    print_and_log("Starting prediction...")
    os.makedirs(prediction_path, exist_ok=True)
    prediction_command = f'python {root_dir}/predict.py -i imagesTs -o MedNext_Predictions -m 3d_fullres -f 4 --num_threads_preprocessing 1'
    if not run_command(prediction_command):
        print_and_log("Prediction failed. Exiting.")
        sys.exit(1)
    
    if not check_directory(prediction_path):
        print_and_log("Prediction output not found or empty. Exiting.")
        sys.exit(1)
    
    print_and_log("Predictions completed successfully.")

    # Postprocessing
    print_and_log("Starting postprocessing...")
    try:
        postprocess.main()
        if not check_directory('Predictions'):
            raise Exception("Postprocessing failed: Output directory is empty or doesn't exist.")
        print_and_log("Postprocessing completed successfully.")
    except Exception as e:
        print_and_log(f"Error during postprocessing: {str(e)}")
        sys.exit(1)

    print_and_log("All processes completed successfully.")

if __name__ == "__main__":
    main()