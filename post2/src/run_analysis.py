from analysis import *

df, df_read, df_complete, df_rel_cpp = read_experiments_data('out/experiments.csv')
Path("out/plots").mkdir(parents=True, exist_ok=True)

# Python only
plots_langs_per_element(df_complete, subset=['python'], suffix='python-only')

# These plots compare the language time over the number of elements.
plots_langs_per_element(
    df_complete,
    subset=['python', 'cpp'],
    suffix='original',
    loglog=False
)
plots_langs_per_element(df_complete, subset=['python', 'cpp'], suffix='original')
plots_langs_per_element(df_rel_cpp, subset=['python', 'cpp'], suffix='original-relative', yscale=False, ylabel='Time relative to "C++" time')

def subset_plot(subset, count):
    plots_langs_per_element(
        df_complete,
        subset=subset,
        suffix='subset-{}'.format(count),
    )
    plots_langs_per_element(
        df_rel_cpp,
        subset=subset,
        suffix='subset-{}-relative'.format(count),
        ylabel='Time relative to "C++" time',
    )
subset_plot(['python', 'cpp'], 0)
subset_plot(['python', 'julia_basic', 'cpp'], 1)
subset_plot(['python', 'julia_basic', 'julia_prealloc', 'cpp'], 2)
fullset = ['python', 'julia_basic', 'julia_prealloc', 'cpp']

plt.scatter(df['elements'], df['load_external'], color='black', **gen_args)
plt.plot(df['elements'], df['load_external'], label="Python DataFrame call", color='black')
plt.savefig('out/plots/stacked_time_load_read.png')


# Just the load-into-dataframe time of python
plt.figure(figsize=(10, 6))
plt.scatter(df['elements'], df['load_external'], color='black', **gen_args)
plt.plot(df['elements'], df['load_external'], label="Python DataFrame call", color='black')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Number of elements')
plt.ylabel('Time (s)')
plt.legend()
plt.savefig(f'out/plots/time_to_load_into_dataframe.png')