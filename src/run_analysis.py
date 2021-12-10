from analysis import *

df, df_read, df_complete = read_experiments_data('out/experiments.csv')

# These plots compare the language time over the number of elements.
plots_langs_per_element(
    df_complete,
    subset=['python', 'cpp'],
    suffix='original',
    loglog=False
)
plots_langs_per_element(df_complete, subset=['python', 'cpp'], suffix='original')
plots_langs_per_element(
    df_complete,
    subset=['python', 'cpp', 'julia_basic'],
    suffix='julia_basic_w_python'
)
plots_langs_per_element(
    df_complete,
    subset=['cpp', 'julia_basic', 'julia_opt'],
    suffix='julia_opt'
)
plots_langs_per_element(
    df_load,
    subset=['cpp', 'julia_basic', 'julia_opt'],
    suffix='read_only'
)

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