from analysis import *

df, df_read, df_complete, df_rel_cpp, df_rel_opt = read_experiments_data('out/experiments.csv')
Path("out/plots").mkdir(parents=True, exist_ok=True)

# Data analysis
style = {
    "x": "elements",
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
sns.scatterplot(df.elements, df.rows)
plt.savefig("out/plots/rows-vs-elements.png")

# These plots compare the language time over the number of elements.
plots_langs_per_element(
    df_complete,
    subset=['python', 'cpp'],
    suffix='original',
    loglog=False
)
plots_langs_per_element(df_complete, subset=['python', 'cpp'], suffix='original')
plots_langs_per_element(df_rel_cpp, subset=['python', 'cpp'], suffix='original-relative', yscale=False, ylabel='Time relative to "C++" time')

subset_count = 1
subset = ['cpp', 'python']
for key in ['julia_basic', 'julia_prealloc', 'julia_c', 'julia_opt']:
    subset.append(key)
    plots_langs_per_element(
        df_complete,
        subset=subset,
        suffix='subset-{}'.format(subset_count),
    )
    plots_langs_per_element(
        df_rel_cpp,
        subset=subset,
        suffix='subset-{}-relative'.format(subset_count),
        ylabel='Time relative to "C++" time',
    )
    subset_count += 1

plots_langs_per_element(
    df_rel_opt,
    subset=subset,
    suffix='subset-relative-opt',
    ylabel='Time relative to "Optimized Julia" time',
)

plots_langs_per_element(
    df_complete,
    subset=['cpp', 'julia_opt'],
    suffix='julia_opt',
)
plots_langs_per_element(
    df_rel_cpp,
    subset=['cpp', 'julia_opt'],
    suffix='julia_opt_relative',
    ylabel='Time relative to "C++" time',
)
plots_langs_per_element(
    df_rel_opt,
    subset=['cpp', 'julia_opt'],
    suffix='julia_opt_relative',
    ylabel='Time relative to "Optimized Julia" time',
)
plots_langs_per_element(
    df_read,
    subset=['cpp', 'julia_opt'],
    suffix='read_only'
)

plots_langs_per_element(
    df_complete,
    subset=['cpp', 'julia_opt'],
    suffix='ignore'
)
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