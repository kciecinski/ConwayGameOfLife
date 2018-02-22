import numpy as np
from tkinter import *


class ConwayGameOfLife:
    def __init__(self, n=10):
        self.n = n
        self.grid = np.zeros((n, n), dtype=np.int8)
        self.old_grid = np.zeros((n,n), dtype=np.int8)

    play = True
    colors = {1: "black", 0: "white"}

    def zero_grids(self):
        self.grid = np.zeros((self.n, self.n), dtype=np.int8)
        self.old_grid = np.zeros((self.n, self.n), dtype=np.int8)

    def generate_random(self):
        self.grid = np.random.randint(2, size=(self.n, self.n))
        self.old_grid = np.copy(self.grid)

    def toad(self):
        self.create_elem([[4, 5], [5, 4], [4, 4], [5, 3], [4, 3], [5, 2]])

    def blinker(self):
        self.create_elem([[4, 4], [6, 4], [5, 4]])

    def create_elem(self, indecies):
        self.zero_grids()
        for x in indecies:
            self.grid[x[0],x[1]] = 1
        self.old_grid = np.copy(self.grid)
        self.update()

    def update(self):
        for index, cell in np.ndenumerate(self.old_grid):
            flat_grid = self.old_grid.flatten()
            flat_neighbours2 = flat_grid[self.n * (index[0] - 1) + index[1] - 1:self.n * (index[0] - 1) + index[1] + 2]
            flat_neighbours1 = flat_grid[self.n * (index[0] + 1) + index[1] - 1:self.n * (index[0] + 1) + index[1] + 2]
            flat_neighbours3 = flat_grid[self.n * index[0] + index[1] - 1:self.n * index[0] + index[1] + 2]
            flat_neighbours = np.concatenate([flat_neighbours2, flat_neighbours3, flat_neighbours1])
            if index[0] in range(1, self.n-1) and index != (1,0):
                if index[1] == 0:
                    flat_neighbours = flat_neighbours.take([1, 2, 4, 5, 7, 8])
                if index[1] == (self.n-1):
                    flat_neighbours = flat_neighbours.take([0, 1, 3, 4, 6, 7])
            if index[0] == 0:
                flat_neighbours = flat_neighbours[3:]
                if index == (0, 0):
                    flat_neighbours[0] = flat_grid[1]
                    flat_neighbours = np.append(flat_neighbours, flat_grid[0])
            if cell == 1:
                if np.sum(flat_neighbours) not in range(3,5):
                    self.grid[index[0]][index[1]] = 0
            else:
                if np.sum(flat_neighbours) == 3:
                    self.grid[index[0]][index[1]] = 1

            master.update()
        self.old_grid = np.copy(self.grid)

        for index, tile in np.ndenumerate(game.grid):
            canvas.create_rectangle(game.n * 10, game.n * 10, index[0] * 10, index[1] * 10, fill=game.colors[tile])

    def stop(self):
        self.play = not self.play


master = Tk()
screen_width = master.winfo_screenwidth()
screen_height = master.winfo_screenheight()
canvas = Canvas(master, width=screen_width, height=screen_height)
canvas.pack()


def configure_button(button,color,position):
    button.configure(width=10, activebackground=color, relief=FLAT)
    canvas.create_window(position, anchor=NW, window=button)


if __name__ == "__main__":
    game = ConwayGameOfLife()
    game.generate_random()

    stop_button = Button(text="Stop", command=game.stop, anchor=W)
    configure_button(stop_button,'red',(300,300))

    blinker_button = Button(text="Blinker", command=game.blinker, anchor=W)
    configure_button(blinker_button,'lightblue',(300,330))

    toad_button = Button(text="Toad", command=game.toad, anchor=W)
    configure_button(toad_button,'lightblue',(300,360))
    while game.play:
        master.after(5, game.update())
