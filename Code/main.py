import json

from character import Character
from combat_tracker import CombatTracker

PARTY_FILE = '../Resources/party.json'
ENEMY_FILE = '../Resources/enemies.json'

NEXT_TOKENS = ['n', 'next']
QUIT_TOKENS = ['q', 'quit', 'x', 'exit']
HIT_TOKENS = ['hit']
HEAL_TOKENS = ['heal']
ADD_ENEMY_TOKENS = ['add']
CONDITION_TOKENS = ['c', 'cond', 'condition']

def load_party_from_json(filename):
    # Load party info from file
    with open(filename) as f:
        party_data = json.load(f)

    # Process party data into objects
    party = []
    for pc in party_data:
        initiative = int(input('Enter initative for {}: '.format(pc['name'])))
        party.append(Character.pc(pc['name'], initiative, pc['ac'], pc['hp'], pc['max_hp'], pc['conditions']))

    return party

def load_enemy_type():
    with open(ENEMY_FILE) as f:
        enemy_types = json.load(f)

    # Get enemy info from user input
    name = input('Enter enemy name: ').strip()
    quant = int(input('Enter enemy quantity: ').strip())

    # Check if enemy is a known type
    if name.lower() in enemy_types:
        init_mod = enemy_types[name.lower()]['initiative']
        ac = enemy_types[name.lower()]['ac']
        hp_expr = enemy_types[name.lower()]['hp_expr']
    else:
        # Otherwise, get info from stdin
        init_mod = int(input('Enter enemy initiative modifier: ').strip('+ '))
        ac = int(input('Enter enemy AC: ').strip())
        hp_expr = input('Enter enemy HP expression: ').strip().lower()

    enemies = []

    if quant > 1:
        # Enumerate enemies if there are more than one
        for i in range(int(quant)):
            enemies.append(Character.enemy('{} #{}'.format(name, i+1), init_mod, ac, hp_expr))
    else:
        enemies.append(Character.enemy(name, init_mod, ac, hp_expr))

    return enemies

def load_enemies():
    enemies = []
    while True:
        enemies.extend(load_enemy_type())

        # Check if there are more enemies to add
        more_enemies = input('\nAdd more enemies? ').strip().lower()
        if more_enemies in ['n', 'no', '']:
            break

    return enemies

def start_combat(tracker):
    while True:
        tracker.print_status()

        tokens = input('\nEnter command [n]: ').strip().lower().split()

        try:
            if len(tokens) == 0 or tokens[0] in NEXT_TOKENS:
                tracker.next_turn()
            elif tokens[0] in QUIT_TOKENS:
                return
            elif tokens[0] in HIT_TOKENS:
                target, damage = tokens[1:3]
                tracker.hit(target, damage)
            elif tokens[0] in HEAL_TOKENS:
                target, amount = tokens[1:3]
                tracker.heal(target, amount)
            elif tokens[0] in ADD_ENEMY_TOKENS:
                enemies = load_enemy_type()
                tracker.add(enemies)
            elif tokens[0][:-1] in CONDITION_TOKENS:
                # Check if adding or removing a condition
                adding_cond = tokens[0][-1] == '+'
                if adding_cond:
                    tracker.add_condition(tokens[1], ' '.join(tokens[2:]))
                else:
                    tracker.remove_condition(tokens[1], ' '.join(tokens[2:]))
            else:
                print('ERROR: Unrecognized Command')
        except:
            print('ERROR: Invalid Command Syntax')

# Load party and enemies
characters = load_party_from_json(PARTY_FILE)
characters.extend(load_enemies())

# Start combat tracker
tracker = CombatTracker(characters)
start_combat(tracker)