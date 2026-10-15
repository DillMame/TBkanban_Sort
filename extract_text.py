import re


def extract_ticket(lines):
    extracted_info = {
        '納品書№': '',
        '受入': '',
        '便': '',
        '納入指示日': ''
    }

    for i, line in enumerate(lines):
        if '納品書No.' in line:
            extracted_info['納品書№'] = lines[i + 1].strip()
        elif '受入' in line:
            extracted_info['受入'] = lines[i + 1].strip()
        elif '便' in line:
            extracted_info['便'] = str(lines[i + 2].strip()).zfill(2)
        elif '納入指示日' in line:
            extracted_info['納入指示日'] = lines[i + 1].strip()[-9:]

    if extracted_info['受入'] == '02':
        file_name = 'osakabe0'
    else:
        file_name = f'{extracted_info['受入']}{extracted_info['納入指示日']}{extracted_info['便']}便{extracted_info['納品書№']}A'

    return file_name

def extract_kanban(lines):
    extracted_info = {
        '納品書№': '',
        '受入': '',
        '便': '',
        '納入指示日': ''
    }

    for i, line in enumerate(lines):
        if 'RVH' in line:
            file_name = 'osakabe'
            break
        else:
            if '納番:' in line:
                extracted_info['納品書№'] = line[-5:]
            elif '受入' in line:
                if lines[i + 3].strip() == '0':
                    extracted_info['受入'] = '00'
                else:
                    extracted_info['受入'] = lines[i + 3].strip()

            elif re.search(r'\d{2} 年\d{2}月\d{2}日\d+便', line):
                match = re.search(r'(\d{2}) 年(\d{2}月\d{2}日)(\d+)便', line)
                if match:
                    extracted_info['納入指示日'] = f'{match.group(1)}年{match.group(2)}'
                    extracted_info['便'] = str(match.group(3)).zfill(2)

            elif '便' in line:
                match = re.search(r'(\d+)\s*便', line)
                if match:
                    extracted_info['便'] = str(match.group(1)).zfill(2)

            elif re.search(r'\d{2} 年\d{2}月\d{2}日', line):
                date_match = re.search(r'(\d{2}) 年(\d{2}月\d{2}日)', line)
                if date_match:
                    extracted_info['納入指示日'] = f'{date_match.group(1)}年{date_match.group(2)}'

            file_name = f'{extracted_info['受入']}{extracted_info['納入指示日']}{extracted_info['便']}便{extracted_info['納品書№']}B'
    return file_name

def extract_sikiri(lines):
    extracted_info = {
        '納品書№': '',
        '受入': '',
        '便': '',
        '納入指示日': ''
    }

    for i, line in enumerate(lines):
        if '納入番号' in line:
            extracted_info['納品書№'] = lines[i + 1].strip()
        elif '納入先' in line:
            if lines[i + 1].strip()[-2:] == '-0':
                extracted_info['受入'] = '00'
            else:
                extracted_info['受入'] = lines[i + 1].strip()[-2:]

        # elif '便' in line:
        #     match = re.search(r'(\d+)便', line)
        #     if match:
        #         extracted_info['便'] = str(int(match.group(1))).zfill(2)
        elif '便' in line:
            match = re.search(r'(\d+)\s*便', line)
            if match:
                extracted_info['便'] = str(int(match.group(1))).zfill(2)

        elif re.search(r'\d{4}年\d{2}月\d{2}日', line):
            date_match = re.search(r'(\d{4})年(\d{2}月\d{2}日)', line)
            if date_match:
                year = date_match.group(1)[-2:]  # 年の末尾2桁を取得
                extracted_info['納入指示日'] = f'{year}年{date_match.group(2)}'

    file_name = f'{extracted_info['受入']}{extracted_info['納入指示日']}{extracted_info['便']}便{extracted_info['納品書№']}C'
    return file_name

def extract_meisai(lines):
    extracted_info = {
        '納品書№': '',
        '受入': '',
        '便': '',
        '納入指示日': ''
    }


    for i, line in enumerate(lines):
        if '納入番号' in line:
            extracted_info['納品書No.'] = lines[i + 2].strip()
        elif '納入先受入' in line:
            if lines[i + 7].strip() == '0':
                extracted_info['受入'] = '00'
            else:
                extracted_info['受入'] = lines[i + 7].strip()
        elif '便' in line:
            match = re.search(r'(\d+) 便', line)
            if match:
                extracted_info['便'] = str(int(match.group(1))).zfill(2)

        elif '納入指示日' in line:
            extracted_info['納入指示日'] = lines[i - 1].strip()



    file_name = f'meisai{extracted_info['受入']}{extracted_info['納入指示日']}{extracted_info['便']}便{extracted_info['納品書№']}'
    return file_name