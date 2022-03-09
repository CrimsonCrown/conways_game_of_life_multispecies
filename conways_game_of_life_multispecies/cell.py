from mesa import Agent


class Cell(Agent):
    """Represents a single ALIVE or DEAD cell in the simulation."""

    DEAD = 0
    ALIVE1 = 1
    ALIVE2 = 2

    def __init__(self, pos, model, init_state=DEAD):
        """
        Create a cell, in the given state, at the given x, y position.
        """
        super().__init__(pos, model)
        self.x, self.y = pos
        self.state = init_state
        self._nextState = None

    @property
    def isAlive1(self):
        return self.state == self.ALIVE1

    @property
    def isAlive2(self):
        return self.state == self.ALIVE2

    @property
    def neighbors(self):
        return self.model.grid.neighbor_iter((self.x, self.y), True)

    def step(self):
        """
        Compute if the cell will be dead or alive at the next tick.  This is
        based on the number of alive or dead neighbors.  The state is not
        changed here, but is just computed and stored in self._nextState,
        because our current state may still be necessary for our neighbors
        to calculate their next state.
        """

        # Get the neighbors and apply the rules on whether to be alive or dead
        # at the next tick.
        live1_neighbors = sum(neighbor.isAlive1 for neighbor in self.neighbors)
        live2_neighbors = sum(neighbor.isAlive2 for neighbor in self.neighbors)

        # Assume nextState is unchanged, unless changed below.
        self._nextState = self.state
        if self.isAlive1:
            if live1_neighbors < 2 or live1_neighbors > 3:
                if live2_neighbors == 3:
                    self._nextState = self.ALIVE2
                else:
                    self._nextState = self.DEAD
        else:
            if self.isAlive2:
                if live2_neighbors < 2 or live2_neighbors > 3:
                    if live1_neighbors == 3:
                        self._nextState = self.ALIVE1
                    else:
                        self._nextState = self.DEAD
            else:
                if live1_neighbors == 3 and live2_neighbors != 3:
                    self._nextState = self.ALIVE1
                else:
                    if live2_neighbors == 3 and live1_neighbors != 3:
                        self._nextState = self.ALIVE2

    def advance(self):
        """
        Set the state to the new computed state -- computed in step().
        """
        self.state = self._nextState
