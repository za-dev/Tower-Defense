
import units

grid_templ = \
"""      0      1      2      3      4      5      6      7      8      9
  -----------------------------------------------------------------------
0 |      |      |      |      |      |      |      |      |      |      |
  |      |      |      |      |      |      |      |      |      |      |
  -----------------------------------------------------------------------
1 |      |      |      |      |      |      |      |      |      |      |
  |      |      |      |      |      |      |      |      |      |      |
  -----------------------------------------------------------------------
2 |      |      |      |      |      |      |      |      |      |      |
  |      |      |      |      |      |      |      |      |      |      |
  -----------------------------------------------------------------------
3 |      |      |      |      |      |      |      |      |      |      |
  |      |      |      |      |      |      |      |      |      |      |
  -----------------------------------------------------------------------
4 |      |      |      |      |      |      |      |      |      |      |
  |      |      |      |      |      |      |      |      |      |      |
  -----------------------------------------------------------------------"""

"""
"counter" for a pod:
    pattern
        type 
        damage (normal, damaged, critical, ruined)
    examples
        --------------------------------------------------
        |  gun |wreck |mortar|rocket|shield| wall |reinf |
        |   3  |      |   0  |      |      |      |      |
        --------------------------------------------------
"""


def render_map(string, row, col, cell_line='first', cur_map=grid_templ):
    if cell_line not in ('first', 'second'):
        raise ValueError(
                "Only 'first' and 'second' are valid for cell_line; got {}".format(cell_line))
    cell_line_offset = 74 if cell_line == 'second' else 0
    row_offset = 71 + 74 + (74 * 3)*row + cell_line_offset
    col_offset = 3 + 7*col
    offset = row_offset + col_offset
    list_grid = list(cur_map)
    list_grid[offset:offset + len(string)] = string
    final_grid = ''.join(list_grid)
    return final_grid

def center_in_6(string):
    s = str(string)
    if len(s) > 6:
        raise ValueError("String max length is 6 but got {} for '{}'".format(len(s), s))
    return ' ' * int((6 - len(s))/2) + s

unit_short_strings = {
        units.Tower:        'tower',
        units.GunTower:     'gun',
        units.MeleeInvader: 'melee',
        units.Wall:         'wall',
        }

def render_game_state(game):
    rendered_map = grid_templ
    for (row, col), unit in game.field.items():
        #--------
        #|  gun | <-- unit type
        #|   2  | <-- current health
        #--------
        s = center_in_6(unit_short_strings[type(unit)])
        h = center_in_6(unit.health)
        rendered_map = render_map(s, row, col, 'first', rendered_map)
        rendered_map = render_map(h, row, col, 'second', rendered_map)
    return rendered_map
