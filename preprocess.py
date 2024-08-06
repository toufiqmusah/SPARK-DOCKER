import os
import re
import shutil

root_dir = os.path.dirname(__file__)
print(root_dir)

def preprocess_data(base_path, destination_path):
    replacements = {'t1c': '0000', 't1n': '0001', 't2f': '0002', 't2w': '0003'}

    for folder in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder)
        if os.path.isdir(folder_path):
            for filename in os.listdir(folder_path):
                new_filename = filename
                for old, new in replacements.items():
                    new_filename = new_filename.replace(old, new)
                src = os.path.join(folder_path, filename)
                dst = os.path.join(destination_path, new_filename)
                shutil.copy(src, dst)
                os.rename(dst, os.path.join(destination_path, new_filename))
    print('Done Replacing Modalities')

def rename_files(destination_path):
    def rename_file(filename, patient_counters):
        pattern = re.compile(r'BraTS-SSA-(\d+)-(\d+)-(\d+)\.nii\.gz')
        match = pattern.match(filename)
        if match:
            patient_id = match.group(1)
            modality_part = match.group(3)

            if patient_id not in patient_counters:
                patient_counters[patient_id] = len(patient_counters)

            series_part = str(patient_counters[patient_id]).zfill(4)

            new_filename = f'BraTS{patient_id}_{series_part}_{modality_part}.nii.gz'
            return new_filename
        return None

    patient_counters = {}
    file_list = sorted(os.listdir(destination_path))

    for filename in file_list:
        new_filename = rename_file(filename, patient_counters)
        if new_filename:
            os.rename(os.path.join(destination_path, filename), os.path.join(destination_path, new_filename))
    
    print('Done Formatting to nnU-Net Format')

if __name__ == "__main__":
    base_path = root_dir + '/BraTS2024-SSA-Challenge-ValidationData/'
    destination_path = root_dir + '/imagesTs/'

    os.makedirs(destination_path, exist_ok=True)
    preprocess_data(base_path, destination_path)
    rename_files(destination_path)