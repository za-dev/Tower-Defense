import random

def roll_pct(chance):
    """Sort of d% roll; pass in 0.9 for a "90% chance something happens.

    Returns True on success, False otherwise."""
    return 0 < (chance - random.uniform(0.0, 1.0))

def closest_enemy_loc(location, field, enemy_class):
    """Find the closest enemy location to the given location.

    Returns the found location and the distance to it.  In case of ties,
    random.choice between the tied enemy locations.
    """
    loc_r, loc_c = location
    best_dist = 999 # hack but it works
    best_loc = [] # have to break ties later
    enemy_field = [l for l, u in field.items() if isinstance(u, enemy_class)]
    for row, col in enemy_field:
        dist = ((row - loc_r)**2 + (col - loc_c)**2)**0.5
        if dist < best_dist:
            best_dist = dist
            best_loc = [(row, col)]
        elif dist == best_dist:
            best_loc.append((row, col))

    if len(best_loc) == 0: # no targets
        return None, None

    # break ties if any - note random.choice([item]) == item
    return random.choice(best_loc), best_dist

class Unit:
    def __init__(self):
        self.health = 3

    def effect(*args, **kwargs):
        """Called for all units when that part of the turn comes."""
        return None, None, None

    def hit(self):
        """Called when the unit is successfully attacked."""
        self.health -= 1

    def move(self, location, field):
        pass


class Tower(Unit):
    pass


class Wall(Tower):
    pass


class Invader(Unit):
    def move(self, location, field):
        """Returns None if didn't move, or (new_row, new_col) if it did."""
        row, col = location
        if (row, col - 1) in field:
            return None
        field.pop(location)
        field[(row, col - 1)] = self
        return (row, col - 1)


class GunTower(Tower):
    """Most basic tower, is just a simple gun emplacement."""
    def range_penalty(self, dist):
        return 0.1 * dist

    def base_hit_prob(self):
        return 0.6

    def effect(self, location, field):
        (tgt_loc, dist) = closest_enemy_loc(location, field, Invader)
        if tgt_loc is None:
            return None, None, None
        # compute probability of hitting
        p_hit = self.base_hit_prob() - self.range_penalty(dist) 
        target = field[tgt_loc]
        if roll_pct(p_hit):
            target.hit()
            return 'hit', tgt_loc, target
        return 'miss', tgt_loc, target


class MeleeInvader(Invader):
    """Moves 1/turn, and can attack adjacent foes, including diagonals."""
    def effect(self, location, field):
        (tgt_loc, dist) = closest_enemy_loc(location, field, Tower)
        if tgt_loc is None or dist > 1.5:
            return None, None, None
        target = field[tgt_loc]
        if roll_pct(0.5):
            target.hit()
            return 'hit', tgt_loc, target
        return 'miss', tgt_loc, target

    def move(self, location, field):
        row, col = location
        new_col = col - 1
        if new_col < 0 or (row, new_col) in field.keys():
            return
        field.pop(location)
        field[row, new_col] = self
