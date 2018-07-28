# Bot written to play the game using what seems to be the best strategy according to the authors. 

import MLModifiedSpaceShooter as game
import numpy as np


def playGame():
    game_state = game.GameState()
    todo = 0
    counter = 0

    while True:
        if counter > 12:
            counter = 0
            if todo == 0:
                todo = 1
            else:
                todo = 0
        counter = counter + 1
        # shoot
        action = np.zeros(4)
        action[2] = 1
        game_state.frame_step(action)

        # shoot
        action = np.zeros(4)
        action[2] = 1
        game_state.frame_step(action)

        # move
        action = np.zeros(4)
        action[todo] = 1
        game_state.frame_step(action)

        # shoot
        action = np.zeros(4)
        action[2] = 1
        game_state.frame_step(action)

        # shoot
        action = np.zeros(4)
        action[2] = 1
        game_state.frame_step(action)


def main():
    playGame()

if __name__ == "__main__":
    main()