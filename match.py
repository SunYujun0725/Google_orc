import os
import shutil

# 設定兩個資料夾路徑
folder1 = './wzm_complete'
folder2 = './calligraphy_photo'

# 創建用於存放複製圖片的目錄
output_dir = './output'
os.makedirs(output_dir, exist_ok=True)

# 儲存檔名相同的圖片檔案路徑
matching_images = []

# 取得資料夾1中的所有圖片檔案
folder1_files = os.listdir(folder1)

# 尋找檔名相同的圖片
for file_name in folder1_files:
    if file_name.endswith('.jpg') or file_name.endswith('.png') or file_name.endswith('.JPG'):  # 根據實際情況調整檔案類型條件
        matching_images.append((file_name, os.path.join(folder1, file_name)))

# 取得資料夾2中的所有圖片檔案
folder2_files = os.listdir(folder2)

# 尋找檔名相同的圖片
for file_name in folder2_files:
    if file_name.endswith('.jpg') or file_name.endswith('.png') or file_name.endswith('.JPG'):  # 根據實際情況調整檔案類型條件
        matching_images.append((file_name, os.path.join(folder2, file_name)))

# 儲存已處理的圖片檔案，避免重複處理
processed_images = set()

# 將相同檔名的圖片複製到以檔名第一個字命名的目錄中
for file_name, image_path in matching_images:
    if file_name not in processed_images:

        first_letter = file_name[0]

         # 設定檔名前綴
        if image_path.startswith(folder1):
            prefix = "style_20_"
        elif image_path.startswith(folder2):
            prefix = "reg_"
        else:
            prefix = ""

        # 新的檔名
        new_file_name = prefix + file_name[0] + ".jpg"

        destination_dir = os.path.join(output_dir, first_letter)
        os.makedirs(destination_dir, exist_ok=True)
        destination_path = os.path.join(destination_dir, new_file_name)
        shutil.copy(image_path, destination_path)

        processed_images.add(file_name)


print("圖片複製完成！")