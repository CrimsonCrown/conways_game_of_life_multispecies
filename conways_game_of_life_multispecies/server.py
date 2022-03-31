from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from .portrayal import portrayCell
from .model import ConwaysGameOfLife


DATACOLORS1 = {"Dead": "white", "Species 1 Cells": "black", "Species 2 Cells": "blue"}
DATACOLORS2 = {"Species 1 Lifeforms": "green", "Species 2 Lifeforms": "yellow"}
# Make a world that is 50x50, on a 250x250 display.
canvas_element = CanvasGrid(portrayCell, 50, 50, 250, 250)
#chart1 = ChartModule(
#    [{"Label": label, "Color": color} for (label, color) in DATACOLORS1.items()]
#)
chart2 = ChartModule(
    [{"Label": label, "Color": color} for (label, color) in DATACOLORS2.items()]
)

model_params = {
    "height": 50,
    "width": 50,
    "density": UserSettableParameter("slider", "Cell density", 0.01, 0.00, 1.0, 0.01),
    "density2": UserSettableParameter("slider", "Second cell density", 0.01, 0.00, 1.0, 0.01),
}

server = ModularServer(
    ConwaysGameOfLife, [canvas_element, chart2], "Game of Life", model_params
)
