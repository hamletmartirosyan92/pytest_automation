import os
import re
from pprint import pprint

import PyPDF2
import fitz
import pytest


def detect_pdf_files(dir_name: str = '') -> [str]:
    """
    Функция читает сразу из текуюей директории (если не задана конкретная другая) все '.pdf' файлы
    и возвращает в массиве их абсалютные пути. (Не зависимо от операционной системы).

    :param dir_name: Имя директории, откуда надо читать файлы.
    """

    base_dir = os.getcwd()
    pdf_files = list(filter(lambda x: ".pdf" in x, os.listdir(os.path.join(base_dir, dir_name))))
    if not pdf_files:
        raise FileNotFoundError("PDF file does not exist in the current folder!")

    file_paths = []
    for file_name in pdf_files:
        file_paths.append(os.path.join(os.getcwd(), file_name))

    return file_paths


@pytest.mark.parametrize("pdf_path", detect_pdf_files())
def test_read_from_pdf(pdf_path):
    """
    Тест параметризированый, который получает на вход абс. пути файлов.
    :param: pdf_path: str -> example: 'E:\\python\\example_1.pdf'
    """
    date_pattern = r'(\d{2}.\d{2}.\d{4})'
    first_line = 'GRIFFON AVIATION SERVICES LLC'
    pattern_1 = r'PN: (\w+) SN: (\d+)'
    pattern_2 = r'DESCRIPTION: (\w+)'
    pattern_3 = r'LOCATION: (\d+) CONDITION: (\w+)'
    pattern_4 = r'RECEIVER#: (\d+) UOM: (\w+)'
    pattern_5 = fr'EXP DATE: {date_pattern} PO: (\w+)'
    pattern_6 = r'CERT SOURCE: (\w+)'
    pattern_7 = fr'REC.DATE: {date_pattern} MFG: (\w+)'
    pattern_8 = fr'BATCH# : (\d+) DOM: {date_pattern}'
    pattern_9 = r'REMARK:(\w*) LOT# : (\d+)'
    pattern_10 = r'TAGGED BY: (\w*)'
    pattern_11 = r' (\w*)'
    pattern_12 = r'Qty: (\d+)NOTES:'
    pattern_13 = r'inspection notes(\w*)'

    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        page = pdf_reader.pages[0]

        width = int(page.artbox.width)
        height = int(page.artbox.height)

        extracted_text = page.extract_text().split("\n")
        pprint(extracted_text)

        assert width == 282
        assert height == 282
        assert len(extracted_text) == 14
        assert extracted_text[0] == first_line
        assert re.match(pattern_1, extracted_text[1])
        assert re.match(pattern_2, extracted_text[2])
        assert re.match(pattern_3, extracted_text[3])
        assert re.match(pattern_4, extracted_text[4])
        assert re.match(pattern_5, extracted_text[5])
        assert re.match(pattern_6, extracted_text[6])
        assert re.match(pattern_7, extracted_text[7])
        assert re.match(pattern_8, extracted_text[8])
        assert re.match(pattern_9, extracted_text[9])
        assert re.match(pattern_10, extracted_text[10])
        assert re.match(pattern_11, extracted_text[11])
        assert re.match(pattern_12, extracted_text[12])
        assert re.match(pattern_13, extracted_text[13])

    doc = fitz.open("example_1.pdf")

    print(doc.load_page(0))
