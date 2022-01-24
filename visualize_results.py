import os

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from poly_basis_main import sum_num_polys_entry, base_num_polys, error_entry


def main():
    mpl.rcParams['font.family'] = 'Segoe UI'
    results = pd.read_csv(f'results/random.csv', sep=',')
    # palette = sns.color_palette("blend:yellow,darkgreen", results[base_num_polys].nunique())
    palette = sns.color_palette("Paired")
    sns.stripplot(data=results, x=sum_num_polys_entry, y=error_entry, hue=base_num_polys, alpha=0.7, palette=palette,
                  edgecolor='black', linewidth=0.5)
    plt.xlabel('# Polys in Sum')
    plt.ylabel('Error [Log]')
    plt.yscale('log')
    plt.legend(title='# Polys in Basis', loc='upper left', bbox_to_anchor=(1.0, 1.0))
    plt.savefig('results/figure.png', dpi=300, bbox_inches='tight')
    os.system('results\\figure.png')


if __name__ == '__main__':
    main()
