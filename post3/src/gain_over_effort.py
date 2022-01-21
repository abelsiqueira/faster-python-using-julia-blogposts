from analysis import *
import pandas as pd
import matplotlib.pyplot as plt

df, df_read, df_complete, df_rel_cpp, df_rel_opt = read_experiments_data('out/experiments.csv')
labels = ['python', 'julia_basic', 'julia_prealloc', 'julia_c', 'cpp', 'julia_opt']
idx = df['elements'] > 1e6
gain = [
    (df_complete['python'][idx] / df_complete[x][idx]).mean()
    for x in labels
]

x = [0, 0.2, 0.4, 0.8, 1, 1]
xl = [xi + 0.025 for xi in x]
xl[-3] = x[-3] - 0.32
xl[-2] = x[-2] - 0.07
xl[-1] = x[-1] - 0.29
with plt.xkcd():
    plt.figure(figsize=[8, 6])
    for i in range(0, len(x)):
        plt.scatter(x[i], gain[i], c=spc_args[labels[i]]["color"], s=80)
        plt.annotate(spc_args[labels[i]]["label"], (xl[i], gain[i]))
    plt.xticks([0, 1], ['Small','High'])
    plt.yticks([1, 10, 20, 30, 40])
    plt.xlabel('Effort')
    plt.ylabel('Average speedup over pure Python')
    plt.title('Average speedup for files with over 1 million elements')
    # plt.legend()
    plt.savefig("out/plots/gain-over-effort.png")


threshold = [1e1, 1e6]

for wrt in ['python', 'cpp']:
    print(f'Speedup over {wrt}')
    speedup = {x: [] for x in labels}
    for th in threshold:
        idx = df['elements'] > th
        for x in labels:
            gain = round((df_complete[wrt][idx] / df_complete[x][idx]).mean(), 2)
            speedup[x].append(gain)

    print('| ' + ' ' * 12 + ''.join([f'| {x:>14} ' for x in labels]) + ' |')
    for i in range(0, len(threshold)):
        th = threshold[i]
        out = f'| {th:12}'
        for x in labels:
            v = speedup[x][i]
            if v > 1:
                out += f'| {v:14.2f} '
            else:
                out += f'| 1 / {1 / v:10.2f} '
        print(out + ' |')