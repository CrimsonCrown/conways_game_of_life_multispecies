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

    def __init__(self, width=50, height=50, density=0.1, multispecies=False):
        """
        Create a new playing area of (width, height) cells.
        """

        # Set up the grid and schedule.

        # Use SimultaneousActivation which simulates all the cells
        # computing their next state simultaneously.  This needs to
        # be done because each cell's next state depends on the current
        # state of all its neighbors -- before they've changed.
        if multispecies==True:
            self.speciesammount=2
        self.schedule = SimultaneousActivation(self)

        # Use a simple grid, where edges wrap around.
        self.grid = Grid(width, height, torus=True)

        #new datacollector for agent state data
        self.datacollector = DataCollector(
            {
                "Dead": lambda m: self.counter(m, 0),
                "Species 1": lambda m: self.counter(m, 1),
                "Species 2": lambda m: self.counter(m, 2),
                "All Living": lambda m: (self.counter(m, 2)+self.counter(m, 1)),
                "Living By Species": lambda m: ((self.counter(m, 2)+self.counter(m, 1))/self.speciesammount),
            },
            {
                "state": lambda a: a.state,
            }
        )

        # Place a cell at each location, with some initialized to
        # ALIVE and some to DEAD.
        for (contents, x, y) in self.grid.coord_iter():
            cell = Cell((x, y), self)
            if multispecies==True:
                randomaux = self.random.random()
                if randomaux < (density/2):
                    cell.state = cell.ALIVE1
                else:
                    if randomaux < density:
                        cell.state = cell.ALIVE2
            else:
                if self.random.random() < density:
                    cell.state = cell.ALIVE1
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

    @staticmethod
    def counter(model, state):
        count = 0
        for cell in model.schedule.agents:
            if cell.state == state:
                count += 1
        return count



def batch_run():
    batch_params_fixed = {"width": 50, "height": 50}
    batch_params_var = {"density": [0.5,1.0], "multispecies": [True,False]}
    batch_params_var2 = {"density": [0.1,0.2], "multispecies": [True,False]}
    batch_params_var3 = {"density": [0.3,0.6], "multispecies": [True,False]}
    
    batch_run = BatchRunner(
        ConwaysGameOfLife,
        batch_params_var,
        batch_params_fixed,
        iterations=1,
        max_steps=100,
        model_reporters = {
            "Dead": lambda m: m.counter(m, 0),
            "Species 1": lambda m: m.counter(m, 1),
            "Species 2": lambda m: m.counter(m, 2),
            "All Living": lambda m: (m.counter(m, 2)+m.counter(m, 1)),
            "Living By Species": lambda m: ((m.counter(m, 2)+m.counter(m, 1))/m.speciesammount),
        },
        agent_reporters = {
            "state": "state",
        }
    )
    
    batch_run2 = BatchRunner(
        ConwaysGameOfLife,
        batch_params_var2,
        batch_params_fixed,
        iterations=1,
        max_steps=100,
        model_reporters = {
            "Dead": lambda m: m.counter(m, 0),
            "Species 1": lambda m: m.counter(m, 1),
            "Species 2": lambda m: m.counter(m, 2),
            "All Living": lambda m: (m.counter(m, 2)+m.counter(m, 1)),
            "Living By Species": lambda m: ((m.counter(m, 2)+m.counter(m, 1))/m.speciesammount),
        },
        agent_reporters = {
            "state": "state",
        }
    )
    
    batch_run3 = BatchRunner(
        ConwaysGameOfLife,
        batch_params_var3,
        batch_params_fixed,
        iterations=1,
        max_steps=100,
        model_reporters = {
            "Dead": lambda m: m.counter(m, 0),
            "Species 1": lambda m: m.counter(m, 1),
            "Species 2": lambda m: m.counter(m, 2),
            "All Living": lambda m: (m.counter(m, 2)+m.counter(m, 1)),
            "Living By Species": lambda m: ((m.counter(m, 2)+m.counter(m, 1))/m.speciesammount),
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

    batch_run2.run_all()

    run_model_data = batch_run2.get_model_vars_dataframe()
    run_agent_data = batch_run2.get_agent_vars_dataframe()

    now = str(datetime.now().date())
    file_name_suffix = ("_01_" + now)
    run_model_data.to_csv("model_data" + file_name_suffix + ".csv")
    run_agent_data.to_csv("agent_data" + file_name_suffix + ".csv")

    batch_run3.run_all()

    run_model_data = batch_run3.get_model_vars_dataframe()
    run_agent_data = batch_run3.get_agent_vars_dataframe()

    now = str(datetime.now().date())
    file_name_suffix = ("_03_" + now)
    run_model_data.to_csv("model_data" + file_name_suffix + ".csv")
    run_agent_data.to_csv("agent_data" + file_name_suffix + ".csv")

