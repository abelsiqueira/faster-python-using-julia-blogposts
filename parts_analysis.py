#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('parts_test.csv')
for key in ['julia_and_c_time', 'pure_julia_time']:
    summed_time = df['load_jl_time'] + df[key]
    df[f'rel_load_{key}'] = df['load_jl_time'] / summed_time
    df[f'rel_{key}'] = df[key] / summed_time
df_mean = df.groupby('rows').mean()
df.sort_values('elements', inplace=True)

spc_args = {
    'julia_and_c': {
        'color': '#2ca02c',
    },
    'pure_julia': {
        'color': '#9467bd',
    },
    'load_jl': {
        'color': '#d62728',
    }
}
args = {'marker': 'x', 'markersize': 10}
plt.figure(figsize=(10,6))
for (key, value) in spc_args.items():
    plt.scatter(df['rows'], df[f'{key}_time'], c=value['color'], alpha=0.3)
    plt.plot(df_mean[f'{key}_time'], c=value['color'], label=key, **args)

plt.xscale('log')
plt.yscale('log')
plt.xlabel('Number of rows')
plt.ylabel('Time (s)')
plt.legend()
plt.savefig('parts_time_per_row.png')

# %%
plt.figure(figsize=(10,6))
for (key, value) in spc_args.items():
    plt.scatter(df['elements'], df[f'{key}_time'], c=value['color'], alpha=0.5, label=key, s=20)

plt.xscale('log')
plt.yscale('log')
plt.xlabel('Number of elements')
plt.ylabel('Time (s)')
plt.legend()
plt.savefig('parts_time_per_element.png')
# %%
plt.figure(figsize=(10,6))
cols = ['rel_pure_julia_time', 'rel_load_pure_julia_time', 'rel_load_julia_and_c_time', 'rel_julia_and_c_time']
plt.stackplot(
    df['elements'],
    df[cols].values.T,
    labels = ["Pure Julia indexes", "Pure Julia load", "Julia+C load", "Julia+C indexes"],
    colors = ["#2ca02c", "#c61718", "#e63738", "#9467bd"],
)
plt.xscale('log')
plt.xlabel('Number of elements')
plt.ylabel('Relative time')
plt.savefig('parts_stacked.png')
plt.legend()
# %%
