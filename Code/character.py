import random

class Character:
    def __init__(self, name, initiative, ac, hp, max_hp, conditions):
        self.name = name
        self.initiative = initiative
        self.hp = hp
        self.max_hp = max_hp
        self.ac = ac
        self.conditions = conditions

    def adjust_hp(self, delta):
        self.hp += delta
        self.hp = min(self.hp, self.max_hp)
        return self.hp

    def add_condition(self, condition):
        self.conditions.append(condition)

    def remove_condition(self, condition):
        self.conditions.remove(condition)

    @staticmethod
    def pc(name, initiative, ac, hp, max_hp, conditions):
        return Character(name, initiative, ac, hp, max_hp, conditions)

    @staticmethod
    def enemy(name, initiative_mod, ac, hp_expr):
        initiative = Character.roll_initiative(initiative_mod)
        hp = Character.roll_health(hp_expr)
        return Character(name, initiative, ac, hp, hp, [])

    @staticmethod
    def roll_initiative(initiative_mod):
        return random.randint(1, 20) + initiative_mod

    @staticmethod
    def roll_health(hp_expr):
        terms = hp_expr.split('+')
        if len(terms) > 1:
            hit_dice, mod = terms
        else:
            hit_dice, mod = terms[0], 0
        dice_quant, dice_faces = map(int, hit_dice.split('d'))
        return sum([random.randint(1, dice_faces) for i in range(dice_quant)]) + int(mod)