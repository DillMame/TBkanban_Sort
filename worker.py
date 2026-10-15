import fitz
from pyzbar.pyzbar import decode
from PIL import Image
import io
import tkinter as tk
from tkinter.ttk import Progressbar
import os
import glob
from extract_text import *
from tkinter import messagebox
from file_delete import file_delete
from pathlib import Path
from datetime import datetime
import fnmatch
# pretty_errors.activate()

"""
工場によってQRにズレがあるのですべてテキストで取得する
"""

# import os
# import sys

# if getattr(sys, 'frozen', False):
#     cur_dir = os.path.dirname(sys.executable)
# else:
#     cur_dir = os.path.dirname(os.path.abspath(__file__))

# temp_dirの作成
# temp_dir = download_path / 'temp_dir'
#
# if not temp_dir:
#     temp_dir.mkdir(exist_ok=True)

TB_folder = Path(r'\\jimny\snet01\トヨタ紡織')
cnt = 0

def detect_qr_code_from_image(image):
    # pyzbarでQRコードをデコード
    decoded_objects = decode(image)
    for obj in decoded_objects:
        if obj.type == 'QRCODE':
            return obj.data.decode('utf-8')  # QRコードのデータを返す
    return None

def execute_task(update_progress, callback,MsgBox,download_path):
    from generate_new_pdf import generate_new_pdf
    from collections import defaultdict
    from file_move import file_move

    files = glob.glob(os.path.join(download_path,'一括_*発行_かんばん*.pdf')) \
            + glob.glob(os.path.join(download_path,'一括_*発行_便チケット*.pdf')) \
            + glob.glob(os.path.join(download_path,'一括_*発行_受注明細*.pdf')) \
            + glob.glob(os.path.join(download_path, '一括_*発行_納品書*.pdf')) \
            + glob.glob(os.path.join(download_path, '納入指示*.csv'))

    if not files:
        MsgBox('ファイルなし','処理ファイルがありません。処理を終了します。','warning')
        # messagebox.showinfo('ファイルなし','処理ファイルがありません。処理を終了します。')
        callback()
        return

    keywords = ['発行_かんばん','発行_便チケット','発行_受注明細','納入指示']

    if not all(any(keyword in path for path in files) for keyword in keywords):
        response = messagebox.askyesno('ファイルなし','3ファイルありません。このまま処理を続けますか？')
        if not response:
            callback()
            return


    files = [Path(file) for file in files]

    for f_cnt,file in enumerate(files,start=1):
        total_files = len(files)
        created = datetime.fromtimestamp(file.stat().st_ctime)
        ymd = created.strftime('%Y%m%d%H%M%S')

        if fnmatch(file.name,'納入指示*.csv'):
            file_move(file,TB_folder / f'納入指示{ymd}.csv')
            continue
        elif fnmatch(file.name,'一括_*発行_納品書*.pdf'):
            file.rename(download_path / f'一括_未発行_納品書{ymd}.pdf')
            continue

        with open(file, 'rb') as f:
            doc = fitz.open('pdf', f.read())
            output_pages = defaultdict(list)

            for page_num in range(len(doc)):
                global cnt
                cnt += 1

                # combined_doc = fitz.open()
                page = doc.load_page(page_num)

                # ページの回転角を元に戻す
                rotation = page.rotation
                if rotation == 90:
                    page.set_rotation(page.rotation + 90)

                # width, height = page.rect.width, page.rect.height

                text = page.get_text()
                lines = text.split('\n')

                if '便チケット' in text:
                    output_file_name = f'{extract_ticket(lines)}{cnt:04}.pdf'
                    group_name = 'かんばん'

                elif '仕切りかんばん' in text:
                    output_file_name = f'{extract_sikiri(lines)}{cnt:04}.pdf'
                    group_name = 'かんばん'

                elif '受　注　明　細' in text:
                    output_file_name = f'{extract_meisai(lines)}{cnt:04}.pdf'
                    group_name = '明細'

                else:
                    pix = page.get_pixmap(matrix=fitz.Matrix(4, 4))
                    img = Image.open(io.BytesIO(pix.tobytes("png")))

                    # QRコード検出
                    qr_code_data = detect_qr_code_from_image(img)

                    if qr_code_data:
                        output_file_name = f'{extract_kanban(lines)}{cnt:04}.pdf'
                        group_name = 'かんばん'
                    else:
                        output_file_name = f'不明{cnt:04}.pdf'
                        group_name = '不明'

                output_pages[group_name].append(output_file_name,page_num)
                # new_page = combined_doc.new_page(width=width, height=height)
                # new_page.show_pdf_page(new_page.rect, doc, page_num)

                # # 更に回転角を元に戻す
                # if rotation == 90:
                #     page.set_rotation(page.rotation + 90)
                #     new_page.set_rotation(new_page.rotation + 90)
                #
                # output_path = os.path.join(temp_dir,output_file_name)
                # combined_doc.save(output_path)
                # combined_doc.close()

                label_text = f'工程1-3 ファイル分割 {f_cnt} / {total_files} ファイル : '
                update_progress( update_progress, page_num, len(doc), label_text)

    # file_move(download_path, files)
    # file_delete()
    generate_new_pdf(update_progress,callback,MsgBox,download_path,output_pages)

if __name__ == '__main__':
    files = []

    import tkinter as tk
    from tkinter.ttk import Progressbar

    root = tk.Tk()
    root.title('PDF Progress')
    root.geometry('300x100')

    progress_bar = Progressbar(root, orient=tk.HORIZONTAL, length=200, mode='determinate')
    running_label = tk.Label(root, text='処理中')

    progress_bar.pack(pady=10)
    running_label.pack(pady=5)

    def update_progress(step, max_steps, progress_text):
        running_label.config(text=f'{progress_text} {step}/{max_steps} ページ完了')
        progress_bar['value'] = (step / max_steps) * 100
        root.update_idletasks()

    def callback():
        print('完了')

    execute_task(progress_bar, update_progress, callback)
    root.mainloop()
