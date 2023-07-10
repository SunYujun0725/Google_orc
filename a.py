import os
import shutil

output_dir = './output'

# 取得 output 資料夾中的所有子資料夾
subfolders = [f.path for f in os.scandir(output_dir) if f.is_dir()]

# 檢查每個子資料夾中的圖片數量
for subfolder in subfolders:
    image_files = [f for f in os.listdir(subfolder) if f.endswith('.jpg') or f.endswith('.png') or f.endswith('.JPG')]
    if len(image_files) < 2:
        # 刪除只有一張或沒有圖片的子資料夾
        absolute_path = os.path.abspath(subfolder)  # 取得子資料夾的絕對路徑
        shutil.rmtree(absolute_path)

print("資料夾刪除完成！")