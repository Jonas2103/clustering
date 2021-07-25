import eikon as ek
import pandas as pd
from pandas_datareader.fred import FredReader
import datetime

ek.set_app_key('704b9a7d4c834f9ca3dc573767c59f3de985a9a8')

start_date = (datetime.datetime.today() - datetime.timedelta(days=365)).date()
end_date = datetime.datetime.today().date()
# Get Stock names
stocks = ek.get_data('.SPX', ['TR.IndexConstituentRIC'])[0]['Constituent RIC']
list = stocks.to_list()

natural_gas = FredReader('DHHNGSP', start_date, end_date).read()
oil = FredReader('DCOILWTICO', start_date, end_date).read()
gold = FredReader('GOLDAMGBD228NLBM', start_date, end_date).read()

print(natural_gas)
print(oil)
print(gold)

# Get Stock Price Data
# price = ek.get_data(list, ['TR.CLOSEPRICE.date', "TR.PriceClose"], {'SDate':'-1Y', 'EDate':'0D'})[0]
# price = price.pivot(index='Date', columns='Instrument', values='Price Close')
# print(price)
# price.to_csv(r'data.csv')
price = pd.read_csv(r'data.csv')

# Get Industry Classification
industries = ek.get_data(list, 'TR.TRBCEconomicSector')[0]
industries.index = list
industries = industries.drop("Instrument", axis=1)




