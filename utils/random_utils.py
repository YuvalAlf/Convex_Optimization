import random
import numpy as np
from random import Random


def set_seed(random_seed: int) -> Random:
    random.seed(random_seed)
    np.random.seed(random_seed)
    return Random(random_seed)
