import os
import shutil

# 設定資料夾路徑
folder_path = './output'

# 取得所有子資料夾
subfolders = [f.path for f in os.scandir(folder_path) if f.is_dir()]

# 對每個子資料夾執行操作
for subfolder in subfolders:
    # 取得子資料夾中的圖片檔案
    image_files = [f for f in os.listdir(subfolder) if f.endswith('.jpg') or f.endswith('.png') or f.endswith('.JPG')]

    # 建立新資料夾
    for image_file in image_files:
        if image_file[0] == "r":
            prefix, name = image_file.split('_', 1)
        else:
            prefix, name, name_2 = image_file.split('_', 2)
            prefix = prefix + "_" + name
        destination_folder = os.path.join(subfolder, prefix)
        os.makedirs(destination_folder, exist_ok=True)

        # 複製圖片到新資料夾
        source_path = os.path.join(subfolder, image_file)
        destination_path = os.path.join(destination_folder, image_file)
        shutil.copy(source_path, destination_path)

        # 刪除原始圖片
        os.remove(source_path)

print("圖片移動並刪除完成！")
