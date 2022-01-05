from analysis import *
import pandas as pd
import matplotlib.pyplot as plt

df, df_read, df_complete, df_rel_cpp, df_rel_opt = read_experiments_data('out/experiments.csv')
labels = ['python', 'julia_basic', 'julia_prealloc', 'julia_c', 'cpp', 'julia_opt']
gain = [
    (df_complete['python'] / df_complete[x]).mean()
    for x in labels
]
print(gain)

x = [0, 0.2, 0.4, 0.8, 1, 1]
with plt.xkcd():
    plt.figure(figsize=[8, 6])
    for i in range(0, len(x)):
        plt.scatter(x[i], gain[i], c=spc_args[labels[i]]["color"], label=spc_args[labels[i]]["label"])
    plt.xticks([0, 1], ['Small','High'])
    plt.yticks([1, 10, 20, 30, 40])
    plt.xlabel('Effort')
    plt.ylabel('Average speedup over pure Python')
    plt.legend()
    plt.savefig("out/plots/gain-over-effort.png")
