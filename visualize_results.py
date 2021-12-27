import os
from statistics import mean

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
import seaborn as sns
from numpy import ndarray

from poly_basis_main import error_entry, base_num_polys, sum_num_polys_entry


def moving_average(array: ndarray) -> ndarray:
    def get_value(index: int) -> float:
        values = []
        for x in range(-5, 6):
            ind = index + x
            if 0 <= ind < len(array):
                values.append(array[ind])
        return mean(values)
    return np.array([get_value(i) for i in range(len(array))])


def main():
    alg_column = 'Algorithm'
    danny_alg = pd.read_csv(f'results/danny_alg.csv', sep='\t')
    random_alg = pd.read_csv(f'results/random.csv', sep='\t')
    random_alg['Mean(Average Error)'] = moving_average(random_alg['Average Error'])
    danny_alg['Mean(Average Error)'] = moving_average(danny_alg['Average Error'])
    danny_alg[alg_column] = 'Danny'
    random_alg[alg_column] = 'Random'
    df = pd.concat([danny_alg, random_alg], ignore_index=True, axis=0)
    mpl.rcParams['font.size'] = 8
    mpl.rcParams['font.family'] = 'Segoe UI'
    sns.lineplot(data=df, x='Basis Size', y='Average Error', hue=alg_column, alpha=0.85, linewidth=0.75)
    # sns.lineplot(data=df, x='Basis Size', y='Mean(Average Error)', hue=alg_column, alpha=0.85, linewidth=0.75)
    plt.xlabel('SoS Basis Size')
    plt.ylabel('Average Approximation Error [Log]')
    plt.yscale('log')
    plt.yticks([1, 0.1, 0.01])
    plt.legend(title='# Polys in Basis', loc='upper left', bbox_to_anchor=(1.0, 1.0))
    plt.savefig('results/figure.png', dpi=300, bbox_inches='tight')
    os.system('results\\figure.png')


if __name__ == '__main__':
    main()
