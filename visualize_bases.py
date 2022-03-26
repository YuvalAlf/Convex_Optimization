import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from utils.os_utils import iterate_inner_directories
import seaborn as sns


def main() -> None:
    base_directory = 'results'

    dfs = pd.DataFrame()
    for alg_name, directory_path in iterate_inner_directories(base_directory):
        basis_quality_path = os.path.join(directory_path, 'quality.csv')
        df = pd.read_csv(basis_quality_path)
        df['Algorithm'] = alg_name
        dfs = pd.concat([df, dfs], ignore_index=True)
    plt.figure(figsize=(10, 8))
    sns.lineplot(data=dfs, x='Basis Size', y='Average Error', hue='Algorithm', alpha=0.8, markers=True)
    plt.xlim((0, 55))
    plt.ylim((0, 1.0))
    plt.yticks(np.arange(0, 1.0001, 0.05))
    plt.grid()
    plt.savefig(os.path.join(base_directory, 'errors.png'), dpi=300, bbox_inches='tight')
    os.system(os.path.join(base_directory, 'errors.png'))


if __name__ == '__main__':
    main()
