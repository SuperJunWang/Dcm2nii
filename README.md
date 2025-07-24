# DCM Anonymization and Conversion to NIfTI Format

This repository contains code for anonymizing CT images in DCM format. The primary purpose of this code is to remove sensitive patient information, such as names, patient IDs, and birth dates, from the DICOM files. After anonymization, the modified files are converted into the NIfTI format (.nii.gz), which is widely used for neuroimaging data.

## Features

- **Anonymization**: Removes sensitive patient information from DICOM files.
- **File Conversion**: Converts anonymized DICOM files to NIfTI format (.nii.gz).
- **Batch Processing**: Supports the processing of multiple DICOM files at once.

## Requirements

To run this code, you'll need the following:

- Python 3.x
- Required Python packages:
  - `pydicom`
  - `nibabel`
  - Any other relevant dependencies (list them here)

You can install the required packages using pip:

```bash
pip install pydicom nibabel
