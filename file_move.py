import shutil

def file_move(folder,files,MsgBox):
   # 元ファイルを加工済みフォルダに移動
    processed_folder = folder / '加工済'

    if not processed_folder.exists():
        processed_folder.mkdir(exist_ok=True)

    for file in files:
        src_path = file
        dest_path = processed_folder / file.name

        try:
            shutil.move(src_path,dest_path)
        except:
            MsgBox('移動エラー',f'移動に失敗しました。手動で移動してください。'
                                              f'\n{file.name}')