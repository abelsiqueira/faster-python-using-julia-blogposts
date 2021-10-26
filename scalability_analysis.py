#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('scalability_test.csv')
plt.figure(figsize=(10,6))
gen_args = {'alpha': 0.3, 's': 20}
spc_args = {
    'python': {
        'label': 'Python',
        'color': '#1f77b4',
    },
    'cpp': {
        'label': 'Python + CPP',
        'color': '#ff7f0e',
    },
    'julia_and_c': {
        'label': 'Julia + C',
        'color': '#2ca02c',
    },
    'julia': {
        'label': 'Julia',
        'color': '#9467bd',
    }
}
all_rows = df['rows'].unique()
for (key, value) in spc_args.items():
    plt.scatter(df['rows'], df[f'{key}_time'], color=value['color'], **gen_args)
    mean = [df[df['rows'] == r][f'{key}_time'].mean() for r in all_rows]
    plt.plot(all_rows, mean, **value, marker='x', markersize=10)

plt.xscale('log')
plt.yscale('log')
plt.xlabel('Number of rows')
plt.ylabel('Time (s)')
plt.legend()
plt.savefig('scalability_time_per_row.png')
# %%
plt.figure(figsize=(10,6))
for (key, value) in spc_args.items():
    plt.scatter(df['elements'], df[f'{key}_time'], color=value['color'], **gen_args)
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Number of elements')
plt.ylabel('Time (s)')
plt.legend()
plt.savefig('scalability_time_per_element.png')
# %%
