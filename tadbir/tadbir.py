import abc
from bs4 import BeautifulSoup
import pandas as pd
import uuid
import requests
import xlwings as xw


class TadbirAbc(abc.ABC):

    @classmethod
    def __init__(cls, whole_data: bool, base_url: str):
        pass

    @classmethod
    def get_historical_units(cls):
        pass

    @classmethod
    def get_Portfolio_Industries(cls):
        pass

    @classmethod
    def get_fund_asset_type(cls):
        pass

    @classmethod
    def get_returns(cls):
        pass


class Tadbir(TadbirAbc):

    def __init__(self, base_url: str, whole_data=False):
        self.base_url = base_url
        self.whole_data = whole_data

    def get_historical_units(self):
        if self.whole_data:
            html_doc = requests.get('https://fund.sabaamc.ir/Reports/FundNAVList').text
            soup = BeautifulSoup(html_doc)
            excel_link = soup.find(id='btnExportToExcel').get('href')
            excel_link = f'https://fund.sabaamc.ir{excel_link}'
            response = requests.get(excel_link)
            excel_file_name = f'FundNAVList_{uuid.uuid4()}.xlsx'
            with open(excel_file_name, 'wb') as f:
                f.write(response.content)
            wb = xw.Book(excel_file_name)  # this will open a new workbook
            sheet1 = wb.sheets[0].used_range.value
            df = pd.DataFrame(sheet1)
            return df

        html_doc = requests.get(f'{self.base_url}/Reports/FundNAVList').text
        soup = BeautifulSoup(html_doc, 'html.parser')
        table = str(soup.find(class_='table'))
        df = pd.read_html(table)[0]
        df.drop(df.index[-1], inplace=True)
        return df

    def get_Portfolio_Industries(self):
        response = requests.get(f'{self.base_url}/Chart/IndustryCompositions?type=getnavtotal')
        industry_list = response.json()[0].get('List')
        cleaned_industry_list = [{'name': d['x'], 'value': d['y']} for d in industry_list]
        df = pd.DataFrame(cleaned_industry_list)
        return df

    def get_fund_asset_type(self):
        html_doc = requests.get(f'{self.base_url}/Reports/FundDailyAssetDistribution').text
        soup = BeautifulSoup(html_doc)
        table = soup.find(class_='table')
        df = pd.read_html(str(table))[0]
        df.drop(df.index[-1], inplace=True)
        first_row = df.iloc[0]
        return first_row

    def get_returns(self):
        html_doc = requests.get(f'{self.base_url}/Reports/FundEfficiencyForDifferentPeriods').text
        soup = BeautifulSoup(html_doc)
        table = soup.find(class_='table')
        df = pd.read_html(str(table))[0]
        return df
