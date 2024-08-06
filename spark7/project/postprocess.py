import os
import shutil


def copy_brats_files(path: str):
    if not os.path.exists(path):
        os.makedirs(path)

    for file in os.listdir("MedNext_Predictions"):
        if "BraTS" in file:
            shutil.copy(os.path.join("MedNext_Predictions", file), path)

    print("Copied BraTS Files to Predictions Folder.")


def rename_files(path):
    directory = path

    for filename in sorted(os.listdir(directory)):
        if filename.startswith("BraTS") and filename.endswith(".nii.gz"):
            case_id = filename[5:10]
            sequence = "000"
            new_filename = f"BraTS-SSA-{case_id}-{sequence}.nii.gz"

            old_file = os.path.join(directory, filename)
            new_file = os.path.join(directory, new_filename)

            os.rename(old_file, new_file)

            print(f'Renamed "{filename}" to "{new_filename}"')


def main():
    print("Starting postprocessing...")
    copy_brats_files()
    rename_files()
    print("Postprocessing completed.")


if __name__ == "__main__":
    main()
