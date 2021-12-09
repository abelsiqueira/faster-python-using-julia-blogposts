import colorsys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mc
from pathlib import Path

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
    'julia_basic': {
        'label': 'Python + Basic Julia',
        'color': '#9467bd',
    },
    'julia_opt': {
        'label': 'Python + Optimized Julia',
        'color': '#d62728',
    }
}

def read_experiments_data(filename='out/experiments.csv'):
    df = pd.read_csv(filename)
    df.sort_values('elements', inplace=True)
    df_complete = pd.DataFrame({
        'elements': df['elements'],
        'python': df['pure_python'],
    })
    df_load = pd.DataFrame({
        'elements': df['elements'],
    })
    for key in ['julia_c', 'julia_basic', 'julia_opt', 'cpp']:
        df_load[key] = df[key]
        df_complete[key] = df[key] + df['load_external']

    return df, df_load, df_complete

def plots_langs_per_element(
        df,
        subset=None,
        suffix='all',
        add_y_limits=False,
        output_dir='out/plots',
        loglog=True,
    ):
    if subset is None:
        subset = [c for c in df.columns if c != 'elements']
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    plt.rcParams.update(white_colors)
    plt.figure(figsize=(10, 6))
    for key in subset:
        value = spc_args[key]
        lbl = value['label']

        plt.scatter(df['elements'], df[key], color=value['color'], **gen_args)
        plt.plot(df['elements'], df[key], label=lbl, color=value['color'])

    plt.xlabel('Number of elements')
    plt.ylabel('Time (s)')
    if add_y_limits:
        plt.ylim(bottom=3e-5, top=20)
    plt.legend()
    if loglog:
        plt.xscale('log')
        plt.yscale('log')
        plt.savefig(f'{output_dir}/time_{suffix}_loglog.png')
    else:
        plt.savefig(f'{output_dir}/time_{suffix}.png')