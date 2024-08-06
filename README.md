### Installation Guide

After pulling the SPARK-DOCKER repository, follow the steps below to install the required dependencies within the SPARK-DOCKER Directory:

1. **Install PyTorch**

   Ensure you have the correct version of PyTorch installed based on your system configuration. You can find the appropriate installation command from the [PyTorch website](https://pytorch.org/get-started/locally/).

   ```bash
   pip install torch torchvision torchaudio
   ```

2. **Install nnU-Net**

   Clone the nnU-Net repository and install it:

   ```bash
   git clone https://github.com/MIC-DKFZ/nnUNet.git
   cd nnUNet
   git checkout nnunetv1
   pip install -e .
   ```

3. **Install MedNeXt**

   Clone the MedNeXt repository and install it:

   ```bash
   git clone https://github.com/MIC-DKFZ/MedNeXt.git mednext
   cd mednext
   pip install -e .
   ```

---

### Additional Notes
- Setup the paths correctly within the scripts.
- Ensure you have all necessary Python dependencies installed.
- Verify that your environment is set up correctly to run both nnU-Net and MedNeXt.
- Refer to the official documentation for any issues encountered during installation.

---
