"""2048 grid state — spawn and (later) moves."""

from __future__ import annotations

import random
from copy import deepcopy

SIZE = 4


class Game2048:
    def __init__(self) -> None:
        self.grid: list[list[int]] = [[0] * SIZE for _ in range(SIZE)]
        self.history_grid: list[list[int]] = None
        self.new_game()
        self.any_move = False

    def new_game(self) -> None:
        """Empty board, then two random tiles with value 2."""
        self.grid = [[0] * SIZE for _ in range(SIZE)]
        self.spawn_tile()
        self.spawn_tile()

    def spawn_tile(self) -> None:
        """Place a 2 on a random empty cell."""
        empty = [
            (r, c)
            for r in range(SIZE)
            for c in range(SIZE)
            if self.grid[r][c] == 0
        ]
        if not empty:
            return
        r, c = random.choice(empty)
        self.grid[r][c] = 2
    def move(self, direction: Direction) -> None:
        """Move all tiles in the given direction.
        If two tiles of the same value touch, they merge into one with the
        value of the first tile multiplied by two.
        The resulting tile cannot merge with another tile again in this move.
        """
        # todo : check if any move is available 
        self.history_grid = deepcopy(self.grid)

        self.any_move = False
        if direction == "up":
            self.move_up()
        elif direction == "down":
            self.move_down()
        elif direction == "left":
            self.move_left()
        elif direction == "right":
            self.move_right()

        if self.any_move:
            self.spawn_tile()
    
    def move_up(self) -> None:
        """Move all tiles up."""
        for c in range(SIZE):
            for r in range(SIZE-1):
                for rr in range(r+1, SIZE):
                    if self.grid[r][c] == self.grid[rr][c] and self.grid[r][c] != 0:
                        self.grid[r][c] = self.grid[r][c] * 2
                        self.grid[rr][c] = 0
                        self.any_move = True
                        break
                    elif self.grid[rr][c]!= 0:
                        break
        
        for repeat in range(SIZE-1):
            for c in range(SIZE):
                for r in range(SIZE-1):
                    if self.grid[r][c] == 0 and self.grid[r+1][c]!=0:
                        self.grid[r][c] = self.grid[r+1][c]
                        self.grid[r+1][c] = 0
                        self.any_move = True

    def move_down(self) -> None:
        """Move all tiles down."""

        for c in range(SIZE):
            for r in range(SIZE-1,0,-1):
                for rr in range(r-1,-1,-1):
                    if self.grid[r][c] == self.grid[rr][c] and self.grid[r][c] != 0:
                        self.grid[r][c] = self.grid[r][c] * 2
                        self.grid[rr][c] = 0
                        self.any_move = True
                        break
                    elif self.grid[rr][c] != 0:
                        break
        
        for repeat in range(SIZE-1):
            for c in range(SIZE):
                for r in range(SIZE-1,0,-1):
                    if self.grid[r][c] == 0 and self.grid[r-1][c] !=0:
                        self.grid[r][c] = self.grid[r-1][c]
                        self.grid[r-1][c] = 0
                        self.any_move = True

    def move_left(self) -> None:
        """Move all tiles left."""

        for r in range(SIZE):
            for c in range(0,SIZE-1):
                for cc in range(c+1,SIZE):
                    if self.grid[r][c] == self.grid[r][cc] and self.grid[r][c] != 0:
                        self.grid[r][c] = self.grid[r][c] * 2
                        self.grid[r][cc] = 0
                        self.any_move = True
                        break
                    elif self.grid[r][cc] !=0:
                        break

        for repeat in range(SIZE-1):
            for r in range(SIZE):
                for c in range(SIZE-1):
                    if self.grid[r][c] == 0 and self.grid[r][c+1] !=0:
                        self.grid[r][c] = self.grid[r][c+1]
                        self.grid[r][c+1] = 0
                        self.any_move = True

    def move_right(self) -> None:
        """Move all tiles right."""

        for r in range(SIZE):
            for c in range(SIZE-1,0,-1):
                for cc in range(c-1,-1,-1):
                    if self.grid[r][c] == self.grid[r][cc] and self.grid[r][c] != 0:
                        self.grid[r][c] = self.grid[r][c] * 2
                        self.grid[r][cc] = 0
                        self.any_move = True
                        break
                    elif self.grid[r][cc] != 0:
                        break

        for repeat in range(SIZE-1):
            for r in range(SIZE):
                for c in range(SIZE-1,0,-1):
                    if self.grid[r][c] == 0 and self.grid[r][c-1]!=0:
                        self.grid[r][c] = self.grid[r][c-1]
                        self.grid[r][c-1] = 0
                        self.any_move = True
                    
    def undo(self) -> None:
        if self.history_grid:
            self.grid = deepcopy(self.history_grid)
            self.history_grid = None