import os

def delete_non_mp3_files(folder_path):
    count = 0
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and not filename.lower().endswith('.mp3'):
            os.remove(file_path)
            print(f"已删除：{filename}")
            count += 1
    print(f"\n共删除 {count} 个非 .mp3 文件。")

# 使用示例：替换为你自己的文件夹路径
folder = r"./songs"  # 示例路径，记得用 r'' 或双斜杠
delete_non_mp3_files(folder)
