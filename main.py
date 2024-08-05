import re
import os
import sys
import json
import torch
import shutil
import random
import subprocess
print(torch.__version__)

os.environ['nnUNet_raw_data_base'] = "SPARK-DOCKER/imagesTs"
os.environ['nnUNet_preprocessed'] = "SPARK-DOCKER/imagesTs"
os.environ['RESULTS_FOLDER'] = "SPARK-DOCKER/3d_fullres"

#import predict
from preprocess import preprocess_data, rename_files

root_dir = 'SPARK-DOCKER/'

base_path = root_dir + 'BraTS2024-SSA-Challenge-ValidationData/'
destination_path = root_dir + 'imagesTs/'
prediction_path = root_dir + 'MedNext_Predictions/'

os.makedirs(destination_path, exist_ok=True)
preprocess_data(base_path, destination_path)
rename_files(destination_path)
os.makedirs(prediction_path, exist_ok=True)

os.system('python predict.py -i imagesTs -o MedNext_Predictions -m 3d_fullres -f 4 --num_threads_preprocessing 1')
