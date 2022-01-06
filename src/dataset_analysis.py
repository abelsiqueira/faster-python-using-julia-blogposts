import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Data analysis
df = pd.read_csv('dataset/info.csv')
style = {
    "x": "nelements",
    "shrink": 0.9,
    "bins": 10,
}
plt.figure()
sns.histplot(df, log_scale=True, **style)
plt.savefig("out/plots/histogram-log.png")

plt.figure()
sns.histplot(df, **style)
plt.savefig("out/plots/histogram.png")

plt.figure()
sns.scatterplot(df.nelements, df.nrows)
plt.xscale('log')
plt.savefig("out/plots/rows-vs-elements.png")