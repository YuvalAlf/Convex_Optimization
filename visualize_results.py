import os

import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import seaborn as sns

from poly_basis_main import error_entry, base_num_polys, sum_num_polys_entry


def main():
    mpl.rcParams['font.size'] = 8
    mpl.rcParams['font.family'] = 'Segoe UI'
    df = pd.read_csv('results.csv')
    palette = sns.color_palette("blend:yellow,darkgreen", df[base_num_polys].nunique())
    sns.stripplot(data=df, x=sum_num_polys_entry, y=error_entry, hue=base_num_polys, alpha=0.7, palette=palette, edgecolor='black', linewidth=0.5)
    plt.xlabel('# Polys in Sum')
    plt.ylabel('Error [Log]')
    plt.yscale('log')
    plt.legend(title='# Polys in Basis')
    plt.savefig('figure.png', dpi=300, bbox_inches='tight')
    os.system('figure.png')


if __name__ == '__main__':
    main()
