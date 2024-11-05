import pandas as pd

class DataModel:
    def __init__(self):
        self.data = pd.read_csv('./sales_data_sample.csv', encoding='ISO-8859-1')
        self.clean_data()

    def clean_data(self):
        self.data = self.data.dropna()
        self.data['Revenue'] = self.data['QUANTITYORDERED'] * self.data['PRICEEACH']
        self.data['ORDERDATE'] = pd.to_datetime(self.data['ORDERDATE'])
        self.data['Month'] = self.data['ORDERDATE'].dt.month
        self.data['Year'] = self.data['ORDERDATE'].dt.year
        self.data['City'] = self.data['CITY']
