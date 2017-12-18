import units
from units import Wall, GunTower, MeleeInvader

def std_win(game):
    """Determine if the game has ended, and if it has, report on who won.

    Returns unit.Tower or unit.Invader.  Invaders win if one of them breaches
    (reaches column 0).  Towers win if they kill all the invaders."""
    invader_locs = [l for l, u in game.field.items() if isinstance(u, units.Invader)]
    if len(invader_locs) == 0:
        return units.Tower
    if len([c for _, c in invader_locs if c == 0]) > 0:
        return units.Invader
    return None # game continues

demo = {
        'field': {
            (0, 0): Wall,
            (1, 0): Wall,
            (2, 0): Wall,
            (3, 0): Wall,
            (4, 0): Wall,
            (0, 7): MeleeInvader,
            (0, 9): MeleeInvader,
            (1, 8): MeleeInvader,
            (2, 7): MeleeInvader,
            (3, 9): MeleeInvader,
        },
        'win-cond': std_win,
}
