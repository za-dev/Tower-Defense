import random

from units import Tower, Invader

class Game:
    def __init__(self, field_row_cnt=5, field_col_cnt=10, field=None, win_cond=None):
        self.field_row_cnt = field_row_cnt
        self.field_col_cnt = field_col_cnt
        if field is None:
            self.field = dict()
        else:
            self.field = dict(field)
        self.win_cond = win_cond
        self.notificants = []
        self.winner = None

    def add_notificant(self, notificant):
        self.notificants.append(notificant)

    def notify(self, *args):
        [n(*args) for n in self.notificants]

    def compute_turn(self, placement_loc, placement_type):
        """Perform user's placement & compute remainder of turn."""
        if self.winner is not None:
            raise ValueError('No turns possible as the game is already over.')
        self.place(placement_loc, placement_type)
        self.activate_units()
        self.move_units()
        self.check_for_game_end()

    def place(self, placement_loc, placement_type):
        if placement_loc in self.field.keys():
            msg = "Can't place unit at {}, cell occupied."
            raise KeyError(msg.format(placement_loc))
        row, col = placement_loc
        if row not in range(0, 5) or col not in range(0, 10):
            msg = "Can't place unit at {}, cell out of bounds."
            raise KeyError(msg.format(placement_loc))
        unit = placement_type()
        self.field[placement_loc] = unit
        self.notify('place', placement_loc, unit)

    def activate_units(self):
        """Calls every unit.effect() in the field, one by one, in this order:

        1. Towers, in random order
        2. Invaders, in random order
        """
        for attackers in Tower, Invader:
            locs_and_units = [(l, u) for l, u in self.field.items() if isinstance(u, attackers)]
            random.shuffle(locs_and_units)
            for l, u in locs_and_units:
                outcome, loc, unit = u.effect(l, self.field)
                if outcome == 'hit' and unit.health <= 0:
                    self.notify('kill', l, u, loc, unit)
                    self.kill(loc)
                else:
                    self.notify(outcome, l, u, loc, unit)

    def check_for_game_end(self):
        self.winner = self.win_cond(self)
        if self.winner is not None:
            self.notify('end', self.winner)

    def kill(self, loc):
        self.field.pop(loc)

    def move_units(self):
        s_locs = sorted(self.field.keys(), key=(lambda i: i[1]), reverse=False)
        for loc in s_locs:
            unit = self.field[loc]
            new_loc = unit.move(loc, self.field)
            if new_loc is not None:
                self.notify('move', new_loc, unit)
