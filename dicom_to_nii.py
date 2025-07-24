import os
import pydicom
import os
import pydicom
import SimpleITK as sitk


'''
This program is used to anonymize DICOM format CT images and convert them to .nii.gz format.
'''
def remove_patient_info(dcm_file, output_dir):
    ds = pydicom.dcmread(dcm_file)
    # 删除特定的元数据元素
    if 'PatientName' in ds:
        ds.PatientName = "Removed"
    if 'PatientID' in ds:
        ds.PatientID = "Removed"
    if 'PatientBirthDate' in ds:
        ds.PatientBirthDate = "Removed"
    # 根据需要添加更多字段

    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 保存到新文件
    anonymized_file_name = os.path.join(output_dir, os.path.basename(dcm_file).replace(".dcm", "_anonymized.dcm"))
    ds.save_as(anonymized_file_name)

def process_directory(input_dir, output_dir):
    # 处理输入目录下的所有子文件夹
    for subfolder in os.listdir(input_dir):
        subfolder_path = os.path.join(input_dir, subfolder)
        if os.path.isdir(subfolder_path):  # 确保是文件夹
            # 创建对应的输出子文件夹
            output_subfolder = os.path.join(output_dir, subfolder)
            os.makedirs(output_subfolder, exist_ok=True)

            for filename in os.listdir(subfolder_path):
                if filename.lower().endswith(".dcm"):  # 注意文件扩展名
                    dcm_file_path = os.path.join(subfolder_path, filename)
                    remove_patient_info(dcm_file_path, output_subfolder)

            # 打印子文件夹处理完成的信息
            print(f"'{subfolder}' 子文件夹处理完成。")

def get_series_with_most_images(data_dir):
    series_ids = sitk.ImageSeriesReader.GetGDCMSeriesIDs(data_dir)
    if not series_ids:
        raise ValueError("未找到任何DICOM系列。请检查目录。")

    series_image_count = {}

    for series_id in series_ids:
        file_names = sitk.ImageSeriesReader.GetGDCMSeriesFileNames(data_dir, series_id)
        series_image_count[series_id] = len(file_names)

    max_series_id = max(series_image_count, key=series_image_count.get)
    print(f"图像数量最多的系列ID: {max_series_id}, 图像数量: {series_image_count[max_series_id]}")

    for series_id in series_ids:
        if series_id != max_series_id:
            file_names_to_delete = sitk.ImageSeriesReader.GetGDCMSeriesFileNames(data_dir, series_id)
            for file_name in file_names_to_delete:
                print(f"删除文件: {file_name}")
                os.remove(file_name)

    return max_series_id

def get_series_id(data_dir):
    series_id = sitk.ImageSeriesReader.GetGDCMSeriesIDs(data_dir)
    assert len(series_id) == 1, "存在不同系列id的dicom数据"
    return series_id[0]

def run_transform(dicom_dir, save_path):
    series_file_names = sitk.ImageSeriesReader.GetGDCMSeriesFileNames(dicom_dir, get_series_id(dicom_dir))
    series_reader = sitk.ImageSeriesReader()
    series_reader.SetFileNames(series_file_names)
    images = series_reader.Execute()
    sitk.WriteImage(images, save_path)


# # 隐藏患者个人信息
# input_directory = "./CT_ori"  # DICOM 文件的主目录（您的 A 文件夹）
# output_directory = "./scientific_data_Dcm"  # 保存匿名化 DICOM 文件的目录（您的 B 文件夹）
#
# process_directory(input_directory, output_directory)
# print("所有患者信息已成功隐藏并保存。")


path_dicom = "./scientific_data_Dcm"  # DICOM 文件的主目录（例如，A文件夹）
path_gz = "./scientific_data_nii"  # 转换后 NIFTI 文件的存放路径（例如，B文件夹）

os.makedirs(path_gz, exist_ok=True)  # 确保结果保存到B文件夹

for subfolder in os.listdir(path_dicom):  # 遍历A文件夹中的所有子文件夹
    dicom_series_path = os.path.join(path_dicom, subfolder)

    if os.path.isdir(dicom_series_path):  # 确保是文件夹
        try:

            # 删选患者序列，保留图像数量最多的系列
            series_id = get_series_with_most_images(dicom_series_path)
            print(f"获取到的系列 ID: {series_id}")

            # 转成 NIFTI 后的保存路径
            output_file_path = os.path.join(path_gz, f"{subfolder}.nii.gz")
            run_transform(dicom_series_path, output_file_path)  # 运行转换

            print('第', subfolder, '个文件转换完成')
        except Exception as e:
            print(f"发生错误: {str(e)}")
            continue  # 出现错误时，继续下一个文件夹