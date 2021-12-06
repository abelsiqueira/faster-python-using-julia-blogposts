# %%
import colorsys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mc
from pathlib import Path

Path("out/plots").mkdir(parents=True, exist_ok=True)

def adjust_lightness(color, amount=1.4):
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])

white_colors = {
    "figure.facecolor" : (1, 1, 1, 0),
    "savefig.facecolor" : (1, 1, 1, 0),
    "ytick.color" : "w",
    "xtick.color" : "w",
    "axes.labelcolor" : "w",
    "axes.edgecolor" : "w"
}
plt.rcParams.update(white_colors)

gen_args = {'alpha': 0.2, 's': 20}
spc_args = {
    'python': {
        'label': 'Pure Python',
        'color': '#333333',
    },
    'cpp': {
        'label': 'Python + C++',
        'color': '#1f77b4',
    },
    'julia_c': {
        'label': 'Julia + C parsing',
        'color': '#2ca02c',
    },
    'julia_dict': {
        'label': 'Python + Basic Julia',
        'color': '#9467bd',
    },
    'julia_manual': {
        'label': 'Python + Optimized Julia',
        'color': '#d62728',
    }
}

def plots(
        subset=spc_args.keys(),
        suffix='all',
        add_y_limits=False,
    ):

    all_rows = df['rows'].unique()
    plt.figure(figsize=(10, 6))
    for (key, value) in spc_args.items():
        if key not in subset:
            continue
        plt.scatter(df['rows'], df[f'{key}_time'], color=value['color'], **gen_args)
        mean = [df[df['rows'] == r][f'{key}_time'].mean() for r in all_rows]
        plt.plot(all_rows, mean, **value, marker='x', markersize=10)

    plt.xlabel('Number of rows')
    plt.ylabel('Time (s)')
    plt.legend()
    plt.savefig(f'out/plots/scalability_time_per_row_{suffix}.png')
    plt.xscale('log')
    plt.yscale('log')
    plt.savefig(f'out/plots/scalability_time_per_row_{suffix}_loglog.png')

    plt.rcParams.update(white_colors)
    plt.figure(figsize=(10, 6))
    for (key, value) in spc_args.items():
        if key not in subset:
            continue
        lbl = value['label']

        plt.scatter(df['elements'], df[f'{key}_time'], color=value['color'], **gen_args)
        plt.plot(df['elements'], df[f'{key}_time'], label=lbl, color=value['color'])
    plt.xlabel('Number of elements')
    plt.ylabel('Time (s)')
    if add_y_limits:
        plt.ylim(bottom=3e-5, top=20)
    plt.legend()
    plt.savefig(f'out/plots/scalability_time_per_element_{suffix}.png')
    plt.xscale('log')
    plt.yscale('log')
    plt.savefig(f'out/plots/scalability_time_per_element_{suffix}_loglog.png')

#%%
df = pd.read_csv('out/scalability_test.csv')
df.sort_values('elements', inplace=True)

plots(subset=['python', 'cpp'], suffix='original')
plots(subset=['python', 'cpp', 'julia_dict'], suffix='julia_dict_w_python')
plots(subset=['cpp', 'julia_dict', 'julia_manual'], suffix='julia_manual')

#%%
df = pd.read_csv('out/parts_test.csv')
df.sort_values('elements', inplace=True)

plt.figure(figsize=(10, 6))
plt.scatter(df['elements'], df['load_external'], color='black', **gen_args)
plt.plot(df['elements'], df['load_external'], label="Python DataFrame call", color='black')

plt.xscale('log')
plt.yscale('log')
plt.xlabel('Number of elements')
plt.ylabel('Time (s)')
plt.legend()
plt.savefig(f'out/plots/parts_time_per_element_python.png')

plt.figure(figsize=(10, 6))
for (key, value) in spc_args.items():
    if key not in ['cpp', 'julia_dict', 'julia_manual']:
        continue
    dfkey = f'read_arrays_{key}_time'
    # if dfkey not in df.columns:
    #     continue
    plt.scatter(
        df['elements'],
        df[dfkey],
        color=value['color'],
        **gen_args
    )
    plt.plot(
        df['elements'],
        df[dfkey],
        label='Read array in ' + value['label'],
        color=value['color']
    )
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Number of elements')
plt.ylabel('Time (s)')
plt.legend()
plt.savefig(f'out/plots/parts_time_per_element.png')
# %%
for (key, value) in spc_args.items():
    dfkey = f'read_arrays_{key}_time'
    if dfkey not in df.columns:
        continue
    total_time = df['load_external'] + df[dfkey]
    plt.figure(figsize=(10, 6))
    plt.stackplot(
        df['elements'],
        df['load_external'] / total_time,
        df[dfkey] / total_time,
        labels=['load and convert to DF', 'Read array in ' + value['label']],
        colors=['gray', value['color']],
    )
    plt.xscale('log')
    plt.xlabel('Number of elements')
    plt.ylabel('Relative Time')
    plt.legend()
    plt.savefig(f'out/plots/parts_time_per_element_{key}.png')
# %%
