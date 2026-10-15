from progress import update_progress
import os
import glob
import datetime as dt
import fitz
from tkinter import messagebox
import sys

# if getattr(sys, 'frozen', False):
#     cur_dir = os.path.dirname(sys.executable)
# else:
#     cur_dir = os.path.dirname(os.path.abspath(__file__))
#
# os.chdir(cur_dir)
# temp_dir = os.path.join(cur_dir, 'temp_dir')

def TB_merge(files,file_name,update_progress,title,callback):
    now = dt.datetime.now()
    ymdhms = now.strftime('%Y%m%d%H%M%S')

    if file_name == 'TB_明細_':
        files.sort()
    else:
        files.sort(reverse=True)

    combined_pdf = fitz.open()

    for f_cnt,file in enumerate(files,start=1):
        total_files = len(files)
        update_progress(f_cnt-1, total_files , title)

        with open(file,'rb') as pdf_file:
            pdf_document = fitz.open(stream=pdf_file.read(),filetype='pdf')
            combined_pdf.insert_pdf(pdf_document)

    save_path = os.path.join(cur_dir,f'{file_name}{ymdhms}.pdf')
    combined_pdf.save(save_path, garbage=4, deflate=True)
    combined_pdf.close()

    # try:
    #     for file in files:
    #         pdf_path = os.path.join(temp_dir, file)
    #         os.remove(pdf_path)
    # except:
    #     messagebox.showerror('削除エラー',f'削除に失敗しました。temp_dirの中身を削除してください。\n{file}')

def generate_new_pdf(update_progress,callback,MsgBox,download_path,output_pages):
    for group_name, items in output_pages.items:
        print(group_name,len(items))
        # if output_pages['明細']:
        #     file_name = 'TB_明細_'
        #     title = '工程2-4 明細ファイル再構成'
        #
        #     TB_merge(doc, output_pages['明細'], file_name,update_progress, title, callback)
    #
    # os.chdir(os.path.dirname(os.path.abspath(__file__)))
    #
    # files = glob.glob(rf'{temp_dir}\meisai*.pdf')
    #
    # if len(files) !=0:
    #     file_name = 'TB_明細_'
    #     title = '工程2-4 明細ファイル再構成'
    #
    #     TB_merge(files,file_name,progress_bar, progress_label,title,callback)
    #
    # files = glob.glob(rf'{temp_dir}\osakabe*.pdf')
    #
    # if len(files) !=0:
    #     file_name = 'TB_刑部_'
    #     title = '工程3-4 刑部カンバンファイル再構成'
    #
    #     TB_merge(files,file_name,update_progress,title,callback)
    #
    # files = glob.glob(rf'{temp_dir}\*.pdf')
    #
    # if len(files) !=0:
    #     file_name = 'TB_かんばん_'
    #
    #     title = '工程4-4 その他カンバンファイル再構成'
    #     TB_merge(files,file_name,update_progress,title,callback)

    callback()
    MsgBox('完了', 'カンバン再構成完了','info')


if __name__ == '__main__':
    import tkinter as tk
    from tkinter.ttk import Progressbar

    root = tk.Tk()
    root.title('PDF Progress')
    root.geometry('300x100')

    # プログレスバーとラベルの設定
    progress_bar = Progressbar(root, orient=tk.HORIZONTAL, length=200, mode='determinate')
    progress_label = tk.Label(root, text='ラベル')

    progress_bar.pack(pady=10)
    progress_label.pack(pady=5)

    generate_new_pdf(progress_bar, progress_label)
    root.mainloop()
