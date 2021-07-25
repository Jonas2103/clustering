# Import Necessary Packages
import pandas as pd
from sklearn.cluster import KMeans
import statsmodels.formula.api as sm
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.distance import cdist

# Import Data
data = pd.read_csv(r'return_data.csv', index_col=0)
data.columns = [x for x in data.columns.str.split('.').str[0]]
print(data.columns)

# Linear Regression of Stock returns on Index, Gas, Oil and Gold

def regression(stock):
    """
    :param stock: stock ticker
    :return: regression coefficients
    """
    model = sm.ols(formula=stock+" ~ SP500_chg + Gas_chg + Oil_chg + Gold_chg", data=data).fit()
    return pd.DataFrame(model.params[model.pvalues < 0.05], columns=[stock])

betas = pd.DataFrame()

# Run Regressions to get regression coefficients as input to clustering
for i in data.columns[:-4]:
    reg = regression(i)
    betas = pd.concat([betas, reg], axis=1, sort=True)
# Transpose to make coefficients columns
betas = betas.T
betas = betas.fillna(0)

# Cluster Analysis
inertia = []
distortions = []
K = range(1, 10)
# Generate Elbow Diagrams with Inertia and Distortion to decide on number of clusters
for k in K:
    model = KMeans(n_clusters = k)
    model.fit(betas)
    distortions.append(sum(np.min(cdist(betas, model.cluster_centers_,
                                        'euclidean'), axis=1)) / betas.shape[0])
    inertia.append(model.inertia_)

# Plot
plt.plot(K, inertia)
plt.xlabel("k")
plt.ylabel("Inertia")
plt.show()

plt.plot(K, distortions)
plt.xlabel("k")
plt.ylabel("Distortion")
plt.show()

# Run Cluster
cluster = KMeans(n_clusters=4)
cluster.fit(betas)

# Save labels to "betas" dataset
betas['labels'] = cluster.labels_

# Merge labels and Industry Classifications
industry = pd.read_csv(r'industry.csv', index_col=0)
industry.index = [x for x in industry.index.str.split('.').str[0]]
industry.sort_index(inplace=True)
results = pd.concat([betas, industry], axis=1)

# Group by labels and look at distribution of industries among labels
groups = results
groups = groups.groupby("labels")["TRBC Economic Sector Name"].value_counts()
print(groups)

# Get mean coefficients by label
data_mean = results.groupby("labels").mean()
print(data_mean)

# Plot mean coefficients by label -> SP500 is market value weighted, larger companies have higher coefficient
data_mean.plot(kind='bar', by='Group')
plt.show()

# Create plot without SP500 coefficient
data_mean[["Gas_chg", "Gold_chg", "Oil_chg"]].plot(kind='bar', by='Group')
plt.show()

# Plot pieplot for each label to look at sector distribution
for x in results["TRBC Economic Sector Name"].unique():
    frame = results[results["TRBC Economic Sector Name"]==x]
    frame["labels"].value_counts().plot(kind='pie',legend=True,title=x)
    plt.show()

