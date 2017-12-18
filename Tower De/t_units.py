import pytest

import units

@pytest.fixture
def m_rand_uni(mocker):
    return mocker.patch('units.random.uniform')

@pytest.fixture
def m_rand_choice(mocker):
    return mocker.patch('units.random.choice')

@pytest.mark.parametrize(
        'chance, ru_ret_val, ret_val', [
        (0.9, 0.95, False),
        (0.9, 0.6, True),
        (0.3, 0.7, False),
        (0.3, 0.2, True),
])
def t_roll_pct(chance, ru_ret_val, ret_val, m_rand_uni):
    m_rand_uni.return_value = ru_ret_val
    assert units.roll_pct(chance) == ret_val

I = units.Invader
T = units.Tower
sqrt_2 = 2**0.5
dist_2x1 = (2**2 + 1)**0.5
std_field = {
    (1, 4): I(), (1, 6): I(), (1, 7): I(),
    (2, 7): I(),
    (3, 2): I(),
    (4, 5): I(),
    (5, 3): I(),
}

closest_enemy_loc_params = [
    # location  ret_val             field
    ( (1, 3),   ((1, 4), 1),        std_field ), # horiz line
    ( (3, 7),   ((2, 7), 1),        std_field ), # vert line
    ( (5, 7),   ((4, 5), dist_2x1), std_field ), # NW quadrant
    ( (4, 1),   ((3, 2), sqrt_2),   std_field ), # NE quadrant
    ( (1, 1),   ((3, 2), dist_2x1), std_field ), # SW quadrant
]

@pytest.mark.parametrize('location, ret_val, field', closest_enemy_loc_params)
def t_closest_enemy_loc(location, field, ret_val, mocker, m_rand_choice):
    m_rand_choice.side_effect = lambda x: x[0] # always pick first item
    assert units.closest_enemy_loc(location, field, units.Invader) == ret_val

def t_closest_enemy_loc_equal_dist(mocker, m_rand_choice):
    # don't bother checking on the returned loc; no way to make it deterministic
    dist = units.closest_enemy_loc((1, 5), std_field, units.Invader)[1]
    m_rand_choice.assert_called_once_with([(1, 6), (1, 4)])
    assert dist == 1

@pytest.fixture
def m_roll_pct(mocker):
    return mocker.patch('units.roll_pct')

@pytest.mark.parametrize('hit', [False, True])
def t_GunTower_effect(mocker, m_roll_pct, hit):
    """Test cases of hitting and missing a nearby target."""
    # setup
    m_roll_pct.return_value = hit
    intended_tgt = std_field[(3, 2)]
    intended_tgt.hit = mocker.Mock()
    gun = units.GunTower()
    # test
    gun.effect((1, 1), std_field)
    if hit:
        intended_tgt.hit.assert_called_once_with()
    else:
        intended_tgt.hit.assert_not_called()

@pytest.mark.parametrize('location, roll_pct_rv, hit_call', [
    ((1, 1), True,  False), 
    ((4, 2), False, False),
    ((4, 2), True,  True)
])
def t_MeleeInvader_effect(mocker, m_roll_pct, location, roll_pct_rv, hit_call):
    """Test cases of no target in range, and failing to hit, and hitting."""
    # 1,1 -> no target
    # 4,2 -> 3,2 (also want to do hit & miss here)
    # setup
    tower_field = {loc: units.Tower() for loc in std_field}
    m_roll_pct.return_value = roll_pct_rv
    intended_tgt = tower_field[(3, 2)]
    intended_tgt.hit = mocker.Mock()
    melee = units.MeleeInvader()
    # test
    melee.effect(location, tower_field)
    if hit_call:
        intended_tgt.hit.assert_called_once_with()
    else: # both False and N/A (N/A == None in python)
        intended_tgt.hit.assert_not_called()

@pytest.mark.parametrize('location, new_location, meta', [
    ((1, 0), (1, 0), "can't move off map"),
    ((3, 3), (3, 3), "can't move through other units"),
    ((2, 6), (2, 5), "can move otherwise"),
])
def t_MeleeInvader_move(location, new_location, meta):
    field = dict(std_field)
    mi = units.MeleeInvader()
    field[location] = mi
    mi.move(location, field)
    expected_field = dict(std_field)
    expected_field[new_location] = mi
    assert meta and expected_field == field
