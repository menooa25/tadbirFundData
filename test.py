from pprint import pprint
import uuid

from bs4 import BeautifulSoup
import pandas as pd

import requests

html_doc = requests.get('https://fund.sabaamc.ir/Reports/FundNAVList').text
soup = BeautifulSoup(html_doc)
excel_link = soup.find(id='btnExportToExcel').get('href')
excel_link = f'https://fund.sabaamc.ir{excel_link}'
response = requests.get(excel_link)
excel_file_name = f'FundNAVList_{uuid.uuid4()}.xlsx'
with open(excel_file_name, 'wb') as f:
    f.write(response.content)

import xlwings as xw
wb = xw.Book("11233.xlsx") # this will open a new workbook
sheet1 = wb.sheets[0].used_range.value
df = pd.DataFrame(sheet1)