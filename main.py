# Import Necessary Packages
import pandas as pd
from sklearn.cluster import KMeans
import statsmodels.formula.api as sm

# Import Data
data = pd.read_csv(r'return_data.csv', index_col=0)
print(data[])
# Linear Regression of Stock returns on Index, Gas, Oil and Gold

def reggression(stock):
    """
    :param stock: stock
    :return:
    """