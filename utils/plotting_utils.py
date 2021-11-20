import os
from dataclasses import dataclass
from typing import Tuple

import matplotlib.pyplot as plt

from utils.iterable_utils import map_list


@dataclass
class Plot:
    name: str
    fig_size: Tuple[float, float]
    x_lim: Tuple[float, float]
    y_lim: Tuple[float, float]

    def __enter__(self):
        plt.figure(figsize=self.fig_size)
        return self

    def plot_function(self, func):
        xs = self.x_lim
        ys = map_list(func, xs)
        plt.plot(xs, ys, '-')

    def __exit__(self, exc_type, exc_val, exc_tb):
        plt.xlim(self.x_lim)
        plt.xlim(self.y_lim)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.savefig(f'{self.name}.pdf', bbox_inches='tight')
        os.system(f'{self.name}.pdf')

