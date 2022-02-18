from os import stat
from typing import Tuple, List
import tkinter as tk
from tkinter import Button, Grid, ttk
import numpy as np
from utils import nb_of_black_cells


class Grid(tk.Canvas):
    CELL_WIDTH = 25
    CELL_HEIGHT = 25
    NB_CASES_WIDTH = 19
    NB_CASES_HEIGHT = 19

    def __init__(self, container):
        super().__init__(container, height=600, width=1000)
        self.cells = []
        self.colors = np.empty((Grid.NB_CASES_WIDTH, Grid.NB_CASES_HEIGHT))
        self.neighbours = np.empty((Grid.NB_CASES_WIDTH, Grid.NB_CASES_HEIGHT))
        self.reproduction = None

        self.__game_setup()

    def __game_setup(self):
        self.button_start = Button(self, text="Start", command=self.start_life, state="disabled")
        _ = self.create_window(10, 550, anchor="nw", window=self.button_start)
        self.button_stop = Button(self, text="Stop", command=self.stop_life, state="disabled")
        _ = self.create_window(100, 550, anchor="nw", window=self.button_stop)
        self.button_restart = Button(self, text="Restart", command=self.restart, state="disabled")
        _ = self.create_window(190, 550, anchor="nw", window=self.button_restart)
        self.pack()

        self.create_grid()

    def __change_color(self, coordinates):
        """ Changes the color of the cell """
        self.button_start['state']="normal"
        x, y = coordinates
        if self.colors[x][y]==1:
            self.itemconfig(self.cells[x][y], fill="white")
            self.colors[x][y]=0
        else:
            self.itemconfig(self.cells[x][y], fill="black")
            self.colors[x][y]=1

    def __binds_grid(self):
        for j in range(Grid.NB_CASES_HEIGHT):
            for i in range(Grid.NB_CASES_WIDTH):
                self.tag_bind(self.cells[i][j], '<Button>', lambda event, coordinates=(i, j): self.__change_color(coordinates))

    def __unbinds_grid(self):
        for j in range(Grid.NB_CASES_HEIGHT):
            for i in range(Grid.NB_CASES_WIDTH):
                self.tag_unbind(self.cells[i][j], '<Button>')
    
    def __compute_all_neighbours(self):
        for i in range(Grid.NB_CASES_WIDTH):
            for j in range(Grid.NB_CASES_HEIGHT):
                self.neighbours[i][j] = nb_of_black_cells(self.colors, (i, j))

    def create_grid(self):
        """
        Creates the grid on the canvas
        Binds the cells with the click button to set the initial population
        """
        for j in range(Grid.NB_CASES_HEIGHT):
            ordinate = (j + 1) * Grid.CELL_HEIGHT
            row = []
            for i in range(Grid.NB_CASES_WIDTH):
                abciss = (i + 1) * Grid.CELL_WIDTH
                row += [self.create_rectangle(
                    abciss,
                    ordinate,
                    abciss + Grid.CELL_WIDTH,
                    ordinate + Grid.CELL_HEIGHT,
                    fill="white"
                )]
                self.colors[i][j] = 0
            self.cells += [row]
        self.__binds_grid()
    
    def not_extinct(self):
        """ Checks if the population not extinct """
        cell_colors = [self.colors[i][j] for j in range(Grid.NB_CASES_HEIGHT) for i in range(Grid.NB_CASES_WIDTH)]
        if cell_colors.count(1)!=0:
            return True
        return False

    def one_generation(self):
        """
        Computes the neighbours of all cells
        Displays the next generation of cells
        """
        self.__compute_all_neighbours()

        for i in range(Grid.NB_CASES_WIDTH):
            for j in range(Grid.NB_CASES_HEIGHT):
                cell, neighbours = self.cells[i][j], self.neighbours[i][j]

                if self.colors[i][j]==0 and neighbours == 3:
                    self.colors[i][j]=1
                    self.itemconfig(cell, fill = "black")
                if self.colors[i][j]==1:
                    if neighbours not in (2, 3):
                        self.colors[i][j]=0
                        self.itemconfig(cell, fill = "white")

    def start_life(self):
        """ Start the life processus """
        self.button_stop['command']=self.stop_life
        self.button_restart['state']="disabled"
        self.button_start['state']="disabled"
        self.button_stop['state']="normal"
        self.button_stop['text']="Stop"
        self.__unbinds_grid()
        if not self.not_extinct():
            return
        self.one_generation()
        self.reproduction = self.after(1000, self.start_life)
    
    def stop_life(self):
        """ Stops the life processus """
        self.button_restart['state']="normal"
        self.button_stop['text']="Continue"
        self.button_stop['command']=self.start_life
        self.after_cancel(self.reproduction)
    
    def restart(self):
        """
        Empties the grid
        Binds the cells with the click button to set the initial population
        """
        self.button_stop['state']="disabled"
        self.button_restart['state']="disabled"
        self.button_stop['text']="Stop"
        self.colors = self.colors * 0
        for i in range(Grid.NB_CASES_WIDTH):
            for j in range(Grid.NB_CASES_HEIGHT):
                self.itemconfig(self.cells[i][j], fill="white")
        self.__binds_grid()


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
