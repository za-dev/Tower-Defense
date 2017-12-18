#!/usr/bin/env python

import pdb
import cmd
import sys

import units
import engine
import scenarios
import map


intro_text = """Pyrgoi:  Turn-Based Tower Defense.

Every turn, play a gun tower with `play [row] [column]`.  `play` can be
abbreviated to `p`.  Gun towers will automatically fire upon the nearest enemy
once per turn.  The hit points of each unit are shown; all attacks deal 1 point
of damage.

Other commands:  `look` and `help`.
"""


class PyrgoiCLI(cmd.Cmd):
    """Simple command line for golf.

    Instantiate then call cmdloop() as per python's cmd.Cmd class."""
    ### standard features of a CLI
    prompt = '(pyrgoi) '
    def do_quit(self, line):
        """Quit the game."""
        return True

    def do_EOF(self, line):
        """Another way of quitting the game, to follow *nix convention."""
        print()
        return True

    def do_shell(self, line):
        """Launch a python debugger from inside the game."""
        pdb.set_trace()

    def do_intro(self, line):
        """Print the intro text."""
        print(intro_text)

    ### gameplay commands; player actions really
    def do_place(self, line):
        """Place a tower on the board; it will be active immediately.

        For this demo it's like this:         `place [row] [column]`
        For the real game it'll be more like: `place [type] [row] [column]`
        """
        #(unit_type, row, column) = line.split()
        #print('unit_type', unit_type)
        (row, column) = [int(token) for token in line.split()]
        if row not in range(0, 5) or column not in range(0, 10):
            print('Invalid input; ({}, {}) is out of bounds.'.format(row, column))
            return
        if (row, column) in self.game.field:
            print('Invalid input; ({}, {}) is occupied.'.format(row, column))
            return
        self.game.compute_turn((row, column), units.GunTower)
        print(map.render_game_state(self.game))

    def do_look(self, line):
        """Look at the state of the game.  No arguments."""
        print(map.render_game_state(self.game))

    ### short commands
    do_p = do_place
    do_q = do_quit
    do_l = do_look

def notificant(event, *details):
    if event is None:
        return
    if event is 'end':
        message = 'YOU WIN!'
        if details[0] == units.Invader:
            message = 'YOU LOSE!'
        print("========================")
        print("GAME OVER,", message)
        print("========================")
        sys.exit(0)
    print(event, *details)


if __name__ == '__main__':
    # tell people how to play, then start the command line interface.
    print(intro_text)
    cli = PyrgoiCLI()
    # have to instantiate the field
    scenario = scenarios.demo
    field = {k: v() for k, v in scenario['field'].items()}
    cli.game = engine.Game(field=field, win_cond=scenario['win-cond'])
    cli.game.add_notificant(notificant)
    print(map.render_game_state(cli.game))
    cli.cmdloop() # GLHF
