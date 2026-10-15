import sys
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta

def file_delete():
    today = datetime.today()
    one_month_ago = today - relativedelta(months=1)

    if getattr(sys, 'frozen', False):
        cur_dir = os.path.dirname(sys.executable)
    else:
        cur_dir = os.path.dirname(os.path.abspath(__file__))

    processed_folder = os.path.join(cur_dir, '加工済')
    file_list = os.listdir(processed_folder)

    for file_name in file_list:
        file_path = os.path.join(processed_folder,file_name)
        last_modified = datetime.fromtimestamp(os.path.getmtime(file_path))

        if last_modified < one_month_ago:
            try:
                os.remove(file_path)
            except:
                pass


if __name__ == '__main__':
    file_delete()