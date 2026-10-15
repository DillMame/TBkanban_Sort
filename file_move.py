import os
import shutil
import sys
from tkinter import messagebox

# if getattr(sys, 'frozen', False):
#     cur_dir = os.path.dirname(sys.executable)
# else:
#     cur_dir = os.path.dirname(os.path.abspath(__file__))
def file_move(folder,files):
   # 元ファイルを加工済みフォルダに移動
    processed_folder = os.path.join(folder,'加工済')

    if not os.path.exists(processed_folder):
        os.makedirs(processed_folder)

    for file in files:
        src_path = file
        dest_path = os.path.join(processed_folder,os.path.basename(file))

        try:
            shutil.move(src_path,dest_path)
        except:
            messagebox.showerror('移動エラー',f'移動に失敗しました。手動で移動してください。'
                                              f'\n{os.path.basename(src_path)}')