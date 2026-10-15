import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from pathlib import Path
import sys

if getattr(sys, 'frozen', False):
    cur_dir = Path(sys.executable).parent
else:
    cur_dir = Path(__file__).resolve().parent

ico_path = Path(r'C:\Windows\user_icon\python_logo.ico')
bg_color = 'Khaki1'
download_path = Path.home() / 'Downloads'
TB_folder = Path(r'\\jimny\snet01\トヨタ紡織')

def MsgBox(self, title, message, icon='info'):
    self.root.attributes('-topmost', True)

    if icon == 'info':
        messagebox.showinfo(title, message, parent=root)
    elif icon == 'warning':
        messagebox.showwarning(title, message, parent=root)
    elif icon == 'error':
        messagebox.showerror(title, message, parent=root)
    else:
        messagebox.showwarning('警告', f'不明なアイコン指定です。:{icon}\n'
                                       f'{title}\n{message}', parent=root)
class App:
    def __init__(self, root):
        self.root = root
        self.root.title('TB紡織カンバン')

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 400
        window_height = 150
        x_pos = screen_width - window_width - 30
        y_pos = screen_height - window_height - 100
        self.root.geometry(f'{window_width}x{window_height}+{x_pos}+{y_pos}')

        self.root.config(bg=bg_color)
        self.root.attributes('-topmost', True)

        if ico_path.exists():
            self.root.iconbitmap(ico_path)

        self.label = tk.Label(root,text='トヨタ紡織カンバン分割・sort',bg=bg_color,pady=20,fg='blue',
                              font=('Arial',11))
        self.label.pack()

        self.start_button = tk.Button(root, text='分割・sort',bg=bg_color, command=self.start_task,
                                      padx=10,font=('Arial',11))
        self.start_button.pack(pady=(20,10))

        self.TBlink = tk.Label(root,text=f'csvファイル移動先:{TB_folder}',fg='blue',bg=bg_color,
                               cursor='hand2',font=('Arial',9,'underline'))
        self.TBlink.pack()
        self.TBlink.bind('<Button-1>',lambda _:os.startfile(str(TB_folder)))

        self.progress_label = tk.Label(root, text='Processing...', anchor='center',bg=bg_color)
        self.progress_bar = ttk.Progressbar(root, orient='horizontal', mode='determinate',length=300)

    def start_task(self):
        from worker import execute_task
        self.start_button.pack_forget()
        self.progress_label.pack(pady=10)
        self.progress_bar.pack(pady=10)
        self.progress_bar['value'] = 0

        # Execute task
        self.root.after(100, execute_task, self.update_progress, self.on_task_complete,MsgBox,
                        download_path)

    def on_task_complete(self):
        self.progress_label.pack_forget()
        self.progress_bar.pack_forget()
        self.start_button.pack(pady=20)

    def update_progress(self, step, max_steps, label_text):
        self.progress_label.config(text=f'{label_text} {step + 1} / {max_steps} 完了')
        self.progress_bar["value"] = (step / max_steps) * 100
        self.progress_bar.update()

    def callback(self):
        from generate_new_pdf import generate_new_pdf
        self.root.after(0,generate_new_pdf,self.update_progress, self.on_task_complete)

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()

