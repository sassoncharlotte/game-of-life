from turtle import width
from typing import Tuple, List
import tkinter as tk
from tkinter import Button, Grid, ttk
import random as rd
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

class Grid(tk.Canvas):
    CELL_WIDTH = 25
    CELL_HEIGHT = 25
    NB_CASES_WIDTH = 19
    NB_CASES_HEIGHT = 19

    def __init__(self, container):
        super().__init__(container, height=600, width=1000)
        self.pack()
        self.cells = []
        self.colors = np.empty((Grid.NB_CASES_WIDTH, Grid.NB_CASES_HEIGHT))
        self.neighbours = np.empty((Grid.NB_CASES_WIDTH, Grid.NB_CASES_HEIGHT))

        self.create_grid()
        self.initial_configuration([
            (5, 5),
            (6, 5),
            (7, 6)
        ])
        button_start = Button(self, text="Start", command=self.start_life)
        button_window = self.create_window(10, 550, anchor="nw", window=button_start)

    def create_grid(self):
        for j in range(Grid.NB_CASES_HEIGHT):
            ordinate = (j + 1) * Grid.CELL_HEIGHT
            row = []
            for i in range(Grid.NB_CASES_WIDTH):
                abciss = (i + 1) * Grid.CELL_WIDTH
                row += [self.create_rectangle(
                    abciss,
                    ordinate,
                    abciss + Grid.CELL_WIDTH,
                    ordinate + Grid.CELL_HEIGHT
                )]
                self.colors[i][j] = 0
            self.cells += [row]
    
    def initial_configuration(self, cells_coordinates: List[Tuple[int, int]]):
        for x, y in cells_coordinates:
            self.itemconfig(self.cells[x][y], fill = "black")
            self.colors[x][y] = 1
    
    def not_extinct(self):
        cell_colors = [self.colors[i][j] for j in range(Grid.NB_CASES_HEIGHT) for i in range(Grid.NB_CASES_WIDTH)]
        if cell_colors.count(1)!=0:
            return True
        return False

    def __compute_all_neighbours(self):
        for i in range(Grid.NB_CASES_WIDTH):
            for j in range(Grid.NB_CASES_HEIGHT):
                self.neighbours[i][j] = nb_of_black_cells(self.colors, (i, j))

    def one_generation(self):
        self.__compute_all_neighbours()

        for i in range(Grid.NB_CASES_WIDTH):
            for j in range(Grid.NB_CASES_HEIGHT):
                cell, color, neighbours = self.cells[i][j], self.colors[i][j], self.neighbours[i][j]

                if color==0 and neighbours == 3:
                    color=1
                    self.itemconfig(cell, fill = "black")
                if color==1:
                    if neighbours not in (2, 3):
                        color=0
                        self.itemconfig(cell, fill = "white")

    def start_life(self):
        if self.not_extinct():
            self.one_generation()


class GameLife(ttk.Frame):
    def __init__(self, container)-> None:
        super().__init__(container)
        self.pack()


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Game of Life")
        self.geometry(str(self.winfo_screenwidth()) + 'x' + str(self.winfo_screenheight()))


if __name__ == "__main__":
    app = App()
    frame = GameLife(app)
    Grid(frame)
    app.mainloop()
