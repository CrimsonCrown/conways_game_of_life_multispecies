from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner
from mesa.space import Grid
from datetime import datetime

from .cell import Cell


class ConwaysGameOfLife(Model):
    """
    Represents the 2-dimensional array of cells in Conway's
    Game of Life.
    """
    speciesammount=1

    def __init__(self, width=50, height=50, density=0.1, density2=0.1):
        """
        Create a new playing area of (width, height) cells.
        """

        self.width=width
        self.height=height

        # Set up the grid and schedule.

        # Use SimultaneousActivation which simulates all the cells
        # computing their next state simultaneously.  This needs to
        # be done because each cell's next state depends on the current
        # state of all its neighbors -- before they've changed.
        self.schedule = SimultaneousActivation(self)

        # Use a simple grid, where edges wrap around.
        self.grid = Grid(width, height, torus=True)

        #new datacollector for agent state data
        self.datacollector = DataCollector(
            {
                #"Dead": lambda m: self.counter(0),
                #"Species 1 Cells": lambda m: self.counter(1),
                #"Species 2 Cells": lambda m: self.counter(2),
                #"All Living Cells": lambda m: (self.counter(2)+self.counter(1)),
                "Species 1 Lifeforms": lambda m: self.lifeformcounter(1),
                "Species 2 Lifeforms": lambda m: self.lifeformcounter(2),
            },
            {
                "state": lambda a: a.state,
            }
        )

        # Place a cell at each location, with some initialized to
        # ALIVE and some to DEAD.
        for (contents, x, y) in self.grid.coord_iter():
            cell = Cell((x, y), self)
            randomaux = self.random.random()
            randomaux2 = self.random.random()
            if randomaux < density:
                cell.state = cell.ALIVE1
            else:
                if randomaux2 < density2:
                    cell.state = cell.ALIVE2
            self.grid.place_agent(cell, (x, y))
            self.schedule.add(cell)

        self.datacollector.collect(self)

        self.running = True

    def step(self):
        """
        Have the scheduler advance each cell by one step
        """

        self.datacollector.collect(self)
        self.schedule.step()

    def counter(self ,state):
        count = 0
        for cell in self.schedule.agents:
            if cell.state == state:
                count += 1
        return count

    def lifeformcounter(self ,state):
        count = 0
        matrix = [[0 for x in range(self.width)] for y in range(self.height)]
        for (contents, x, y) in self.grid.coord_iter():
            matrix[x][y]=contents.state
        for y in range(self.height):
            for x in range(self.width):
                if matrix[y][x]==state:
                    count=count+1
                    self.markcluster(matrix,x,y,state)
        return count

    def markcluster(self,matrix,x,y,state):
        matrix[y][x]=0
        setcoord = {(x-1,y-1),(x,y-1),(x-1,y),(x-1,y+1),(x,y+1),(x+1,y+1),(x+1,y-1),(x+1,y)}
        while len(setcoord)>0:
            coords=setcoord.pop()
            x=coords[0]
            y=coords[1]
            if x < 0:
                x=self.width-1
            if y < 0:
                y=self.height-1
            if x >= self.width:
                x=0
            if y >= self.height:
                y=0
            if matrix[y][x]==state:
                matrix[y][x]=0
                setcoord.add((x-1,y-1))
                setcoord.add((x,y-1))
                setcoord.add((x-1,y))
                setcoord.add((x-1,y+1))
                setcoord.add((x,y+1))
                setcoord.add((x+1,y+1))
                setcoord.add((x+1,y-1))
                setcoord.add((x+1,y))
        return




def batch_run():
    #variaveis independentes
    batch_params_fixed = {"width": 50, "height": 50}
    batch_params_var = {"density": [0.5,0.3], "density2": [0.0,0.5,1.0]}
    
    batch_run = BatchRunner(
        ConwaysGameOfLife,
        batch_params_var,
        batch_params_fixed,
        iterations=100,
        max_steps=200,
        model_reporters = {
            "Species 1 Lifeforms": lambda m: m.lifeformcounter(1),
            "Species 2 Lifeforms": lambda m: m.lifeformcounter(2),
        },
        agent_reporters = {
            "state": "state",
        }
    )

    batch_run.run_all()

    run_model_data = batch_run.get_model_vars_dataframe()
    run_agent_data = batch_run.get_agent_vars_dataframe()

    now = str(datetime.now().date())
    file_name_suffix = ("_05_" + now)
    run_model_data.to_csv("model_data" + file_name_suffix + ".csv")
    run_agent_data.to_csv("agent_data" + file_name_suffix + ".csv")

