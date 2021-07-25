import eikon as ek
import pandas as pd

ek.set_app_key('704b9a7d4c834f9ca3dc573767c59f3de985a9a8')

stocks = ek.get_data('.SPX', ['TR.IndexConstituentRIC'])[0]['Constituent RIC']

list = stocks.to_list()
print(list)

price = ek.get_data(list, ['TR.CLOSEPRICE.date', "TR.PriceClose"], {'SDate':'-1Y', 'EDate':'0D'})[0]
# price = ek.get_timeseries(list[0:300], 'close', start_date="2020-03-01", end_date="2021-03-01",interval="daily")

price.to_csv(r'data.csv')
print(price)