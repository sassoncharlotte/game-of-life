from typing import Tuple
import numpy as np

def nb_of_black_cells(all_colors: np.ndarray, coordinates: Tuple[int, int]):
    abcisses, ordinates = [], []
    width, height = all_colors.shape

    if coordinates[0]==0:
        abcisses = [coordinates[0], coordinates[0]+1]
    if coordinates[0]==width - 1:
        abcisses = [coordinates[0]-1, coordinates[0]]
    if coordinates[1]==0:
        ordinates = [coordinates[1], coordinates[1]+1]
    if coordinates[1]==height - 1:
        ordinates = [coordinates[1]-1, coordinates[1]]
    if not ordinates:
        ordinates = range(coordinates[1]-1, coordinates[1]+2)
    if not abcisses:
        abcisses = range(coordinates[0]-1, coordinates[0]+2)

    cell_colors = [all_colors[i][j] for i in abcisses for j in ordinates if (j!=coordinates[1] or i!=coordinates[0])]
    neighbours = cell_colors.count(1)
    return neighbours
