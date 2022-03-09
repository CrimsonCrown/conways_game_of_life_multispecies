from conways_game_of_life.server import server
from conways_game_of_life.model import ConwaysGameOfLife
from conways_game_of_life.model import batch_run
import pandas as pd
from datetime import datetime

#batch_params = {"width": 50, "height": 50, "density": [0.5,1.0], "multispecies": [True,False]}

#experiments = batch_run(
#    ConwaysGameOfLife,
#    parameters=batch_params,
#    iterations=1,
#    max_steps=100,
#    number_processes=None,
#    data_collection_period=1,
#    display_progress=True,
#)

#dataframe = pd.DataFrame(experiments)
#print(dataframe.keys())

batch_run()
server.launch()
