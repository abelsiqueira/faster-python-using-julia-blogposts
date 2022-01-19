from analysis import *

df, df_read, df_complete, df_rel_cpp = read_experiments_data('out/experiments.csv')

parts = {
    'pandas_read_csv': {
        'color': 'magenta',
        'label': 'Pandas - Read CSV',
    },
    'pandas_tuples_to_df': {
        'color': 'cyan',
        'label': 'Pandas - Convert to DataFrame'
    }
}

def common_info():
    plt.xlabel('Number of elements')
    plt.ylabel('Time (s)')
    plt.legend()
    plt.xscale('log')
    plt.yscale('log')

# Stacked parts
plt.figure(figsize=(10,6))
plt.stackplot(
    df['elements'],
    df['pandas_read_csv'],
    df['pandas_tuples_to_df'],
    labels=[parts['pandas_read_csv']['label'], parts['pandas_tuples_to_df']['label']],
    colors=[parts['pandas_read_csv']['color'], parts['pandas_tuples_to_df']['color']],
)
common_info()
plt.savefig('out/plots/pandas-stacked-log.png')
plt.yscale('linear')
plt.savefig('out/plots/pandas-stacked.png')
