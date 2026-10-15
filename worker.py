# import pretty_errors

from progress import update_progress
import fitz
from pyzbar.pyzbar import decode
from PIL import Image
import io
import tkinter as tk
from tkinter.ttk import Progressbar
import os
import glob
import re
from extract_text import *
from generate_new_pdf import generate_new_pdf
from file_move import file_move
from tkinter import messagebox
from file_delete import file_delete

# pretty_errors.activate()

"""
工場によってQRにズレがあるのですべてテキストで取得する
"""

import os
import sys

if getattr(sys, 'frozen', False):
    cur_dir = os.path.dirname(sys.executable)
else:
    cur_dir = os.path.dirname(os.path.abspath(__file__))

# ワーキングディレクトリを変更
os.chdir(cur_dir)

# temp_dirの作成
temp_dir = os.path.join(cur_dir, 'temp_dir')
os.makedirs(temp_dir, exist_ok=True)

cnt = 0

def detect_qr_code_from_image(image):

    # pyzbarでQRコードをデコード
    decoded_objects = decode(image)
    for obj in decoded_objects:
        if obj.type == 'QRCODE':
            return obj.data.decode('utf-8')  # QRコードのデータを返す
    return None

def execute_task(progress_bar, progress_label, callback):
    files = glob.glob(os.path.join(cur_dir,'一括_*発行_かんばん*.pdf')) \
            + glob.glob(os.path.join(cur_dir,'一括_*発行_便チケット*.pdf')) \
            + glob.glob(os.path.join(cur_dir,'一括_*発行_受注明細*.pdf'))

    if not files:
        messagebox.showinfo('ファイルなし','処理ファイルがありません。処理を終了します。')
        callback()
        return

    keywords = ['発行_かんばん','発行_便チケット','発行_受注明細']

    if not all(any(keyword in path for path in files) for keyword in keywords):
        response = messagebox.askyesno('ファイルなし','3ファイルありません。このまま処理を続けますか？')
        if not response:
            callback()
            return

    for f_cnt,file in enumerate(files,start=1):
        total_files = len(files)

        with open(file, 'rb') as f:
            doc = fitz.open('pdf', f.read())
            # max_steps = len(doc)

            for page_num in range(len(doc)):
                global cnt
                cnt += 1

                combined_doc = fitz.open()
                page = doc.load_page(page_num)

                # ページの回転角を元に戻す
                rotation = page.rotation
                if rotation == 90:
                    page.set_rotation(page.rotation + 90)

                width, height = page.rect.width, page.rect.height


                text = page.get_text()
                lines = text.split('\n')

                if '便チケット' in text:
                    output_file_name = f'{extract_ticket(lines)}{cnt:04}.pdf'

                elif '仕切りかんばん' in text:
                    output_file_name = f'{extract_sikiri(lines)}{cnt:04}.pdf'

                elif '受　注　明　細' in text:
                    output_file_name = f'{extract_meisai(lines)}{cnt:04}.pdf'

                else:
                    pix = page.get_pixmap(matrix=fitz.Matrix(4, 4))
                    img = Image.open(io.BytesIO(pix.tobytes("png")))

                    # QRコード検出
                    qr_code_data = detect_qr_code_from_image(img)

                    if qr_code_data:
                        output_file_name = f'{extract_kanban(lines)}{cnt:04}.pdf'
                    else:
                        output_file_name = f'不明{cnt:04}.pdf'

                new_page = combined_doc.new_page(width=width, height=height)
                new_page.show_pdf_page(new_page.rect, doc, page_num)

                # 更に回転角を元に戻す
                if rotation == 90:
                    page.set_rotation(page.rotation + 90)
                    new_page.set_rotation(new_page.rotation + 90)

                output_path = os.path.join(temp_dir,output_file_name)
                combined_doc.save(output_path)
                combined_doc.close()

                label_text = f'工程1-3 ファイル分割 {f_cnt} / {total_files} ファイル : '
                update_progress(progress_bar, progress_label, page_num, len(doc), label_text)

    file_move(cur_dir, files)
    file_delete()
    generate_new_pdf(progress_bar, progress_label,callback)

if __name__ == '__main__':
    files = []

    root = tk.Tk()
    root.title('PDF Progress')
    root.geometry('300x100')

    # プログレスバーとラベルの設定
    progress_bar = Progressbar(root, orient=tk.HORIZONTAL, length=200, mode='determinate')
    progress_label = tk.Label(root, text='ラベル')

    progress_bar.pack(pady=10)
    progress_label.pack(pady=5)


    def callback():
        print('完了')

    execute_task(progress_bar, progress_label, callback)
    root.mainloop()
