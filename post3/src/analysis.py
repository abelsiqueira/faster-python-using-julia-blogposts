import colorsys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mc
from pathlib import Path
import seaborn as sns

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
        'label': 'C++',
        'color': '#1f77b4',
    },
    'julia_c': {
        'label': 'Julia + C parsing',
        'color': '#97881e',
    },
    'julia_basic': {
        'label': 'Basic Julia',
        'color': '#9467bd',
    },
    'julia_prealloc': {
        'label': 'Prealloc Julia',
        'color': '#70a3a9',
    },
    'julia_opt': {
        'label': 'Optimized Julia',
        'color': '#d62728',
    }
}

def read_experiments_data(filename='out/experiments.csv'):
    df = pd.read_csv(filename)
    df.sort_values('elements', inplace=True)
    df_complete = pd.DataFrame({
        'elements': df['elements'],
        'python': df['python'],
    })
    df_read = pd.DataFrame({
        'elements': df['elements'],
    })
    df_relative_cpp = pd.DataFrame({
        'elements': df['elements'],
        'python': df['python'] / (df['load_external'] + df['cpp'])
    })
    df_relative_opt = pd.DataFrame({
        'elements': df['elements'],
        'python': df['python'] / (df['load_external'] + df['julia_opt'])
    })
    for key in spc_args.keys() - 'python':
        df_read[key] = df[key]
        df_complete[key] = df[key] + df['load_external']
        df_relative_cpp[key] = df_complete[key] / (df['load_external'] + df['cpp'])
        df_relative_opt[key] = df_complete[key] / (df['load_external'] + df['julia_opt'])

    return df, df_read, df_complete, df_relative_cpp, df_relative_opt

def plots_langs_per_element(
        df,
        subset=None,
        suffix='all',
        add_y_limits=False,
        output_dir='out/plots',
        loglog=True,
        yscale=True,
        ylabel='Time (s)',
        use_white=False,
    ):
    if subset is None:
        subset = [c for c in df.columns if c != 'elements']
    if use_white:
        plt.rcParams.update(white_colors)
    plt.figure(figsize=(10, 6))
    for key in subset:
        value = spc_args[key]
        lbl = value['label']

        plt.scatter(df['elements'], df[key], color=value['color'], **gen_args)
        plt.plot(df['elements'], df[key], label=lbl, color=value['color'])

    plt.xlabel('Number of elements')
    plt.ylabel(ylabel)
    if add_y_limits:
        plt.ylim(bottom=3e-5, top=20)
    plt.legend()
    if loglog:
        plt.xscale('log')
        if yscale:
            plt.yscale('log')
        plt.savefig(f'{output_dir}/time_{suffix}_loglog.png')
    else:
        plt.savefig(f'{output_dir}/time_{suffix}.png')