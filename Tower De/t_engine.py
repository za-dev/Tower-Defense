import pytest

import engine, units

I = units.Invader
T = units.Tower
std_field = { (1, 4): I(), (1, 7): I(),
              (2, 2): T(), (2, 5): T() }

def t_game_activate_units(mocker):
    # mocking on this is crazy:  Have to record the order in which the
    # effect calls happen on the various units, then assert it was done
    # correctly.  Sheesh.
    effect_calls = []
    def closure(u):
        def inner(*args):
            effect_calls.append(u)
            return None, None, None
        return inner
    for u in std_field.values():
        u.effect = mocker.Mock()
        u.effect.side_effect = closure(u)
    game = engine.Game(field=std_field)

    game.activate_units()

    assert (isinstance(effect_calls[0], T)
            and isinstance(effect_calls[1], T)
            and isinstance(effect_calls[2], I)
            and isinstance(effect_calls[3], I))

def t_game_activate_units_kill(mocker):
    # set up to kill the defender
    defender = units.MeleeInvader()
    defender.health = 1
    attacker = units.GunTower()
    field = {(1, 1): defender, (1, 2): attacker}
    m_roll_pct = mocker.patch('units.roll_pct')
    m_roll_pct.return_value = True
    game = engine.Game(field=field)

    game.activate_units()

    assert ({(1, 2): attacker} == game.field # defender dead
            and attacker.health == 3)        # defender didn't shoot back

def t_notify(mocker):
    notificants = [mocker.Mock() for _ in range(3)]
    game = engine.Game()
    [game.add_notificant(n) for n in notificants]
    args = ('you', 'been', 'served')

    game.notify(*args)

    [n.assert_called_once_with(*args) for n in notificants]

@pytest.mark.parametrize('place, success', [
        ((2, 4), True),  # successful placement
        ((2, 2), False), # failure:  square occupied
        ((6, 9), False), # failure:  square out of bounds
        ])
def t_place(place, success):
    game = engine.Game(field=std_field)
    if success:
        game.place(place, T)
        assert type(game.field[place]) == T
    else:
        with pytest.raises(KeyError):
            game.place(place, T)

def t_move_units_order(mocker):
    # assemble an ordering for move() calls
    il = [I() for _ in range(4)]
    test_field = {(2, 2): il[0], (2, 3): il[1], (2, 5): il[2], (1, 7): il[3]}
    move_calls = []
    def closure(u):
        def inner(*args):
            move_calls.append(u)
        return inner
    for u in test_field.values():
        u.move = mocker.Mock()
        u.move.side_effect = closure(u)
    game = engine.Game(field=test_field)

    game.move_units()

    assert il == move_calls

def t_move_units_accuracy(mocker):
    il = [I() for _ in range(4)]
    test_field = {(2, 2): il[0], (2, 3): il[1], (2, 5): il[2], (1, 7): il[3]}
    expected_field = {(2, 1): il[0], (2, 2): il[1], (2, 4): il[2], (1, 6): il[3]}
    game = engine.Game(field=test_field)

    game.move_units()

    assert expected_field == game.field
