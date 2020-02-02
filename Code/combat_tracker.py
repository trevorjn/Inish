class InvalidCommandError(Exception):
    pass

class CombatTracker:
    def __init__(self, characters):
        self.characters = sorted(characters, key=lambda x: -x.initiative)
        self.current_turn = 0

    def next_turn(self):
        self.current_turn = (self.current_turn + 1) % len(self.characters)

    def print_status(self):
        print()
        # Get length of longest name for adaptive formatting
        max_name_len = max(len(c.name) for c in self.characters)
        for i, c in enumerate(self.characters):
            print('{}{:>2d}) {:{}} | {:>3d} HP | {:>2d} AC | {}'.format(
                '->' if self.current_turn == i else '  ', i, c.name, max_name_len, c.hp, c.ac, ', '.join(c.conditions)))

    def hit(self, target, damage):
        i = self._index_from_target_str(target)
        self.characters[i].adjust_hp(-int(damage))

    def heal(self, target, amount):
        i = self._index_from_target_str(target)
        self.characters[i].adjust_hp(int(amount))

    def add(self, characters):
        # Save current character
        current_char = self.characters[self.current_turn]

        # Add new characters to initiative tracker
        self.characters.extend(characters)
        self.characters.sort(key=lambda x: -x.initiative)

        # Adjust current turn to account for newly added characters
        self.current_turn = self.characters.index(current_char)

    def add_condition(self, target, condition):
        i = self._index_from_target_str(target)
        self.characters[i].add_condition(condition)

    def remove_condition(self, target, condition):
        i = self._index_from_target_str(target)
        self.characters[i].remove_condition(condition)

    def _index_from_target_str(self, target):
        if target.isdigit():
            i = int(target)
        else:
            i = self._find_char_by_prefix(target)
        return i

    def _call_func_on_char(self, target, func, *args):
        # Get index of target character in self.characters
        if target.isdigit():
            i = int(target)
        else:
            i = self._find_char_by_prefix(target)

        # Call function on target character
        self.characters[i].func(*args)
        

    def _find_char_by_prefix(self, pref):
        possible_chars = [i for i, c in enumerate(self.characters) if c.name.lower().startswith(pref.lower())]
        if len(possible_chars) == 1:
            return possible_chars[0]
        else:
            return -1