import os, re

LINE_REGEX = re.compile("([0-9]+) units each with ([0-9]+) hit points(?: \((weak|immune) to ((?:\w| |,)+)(?:; (weak|immune) to ((?:\w| |,)+))?\))? with an attack that does ([0-9]+) (\w+) damage at initiative ([0-9]+)")

IMMUNE = 0
INFECTION = 1

PRINT = False

def custom_print(s: str):
    if PRINT:
        print(s)

class Group:
    def __init__(self, id: int, army: int, units: int, hp: int, weaknesses: set[str], immunities: set[str], damage: int, attack_type: str, initiative: int, boost: int = 0):
        self.id = id
        self.army = army
        self.units = units
        self.hp = hp
        self.weaknesses = weaknesses
        self.immunities = immunities
        self.damage = damage
        self.attack_type = attack_type
        self.initiative = initiative
        self.boost = boost

    def effective_power(self):
        return self.units * (self.damage + self.boost)

    def damage_given_to(self, g: "Group"):
        if self.attack_type in g.immunities:
            return 0
        return (2 if self.attack_type in g.weaknesses else 1) * self.effective_power()

    def attack(self, g: "Group"):
        custom_print(f"{'Infection' if self.army == INFECTION else 'Immune System'} group {self.id} attacks defending group {g.id}, killing {min((self.damage_given_to(g) // g.hp), g.units)} units")
        g.take_damage(self.damage_given_to(g))

    def take_damage(self, damage: int):
        self.units -= (damage // self.hp)

    def __repr__(self):
        return f"""{'Immune' if self.army == IMMUNE else 'Infection'} army group:
            - units: {self.units}
            - hp: {self.hp}
            - weaknesses: {self.weaknesses if len(self.weaknesses) > 0 else "none"}
            - immunities: {self.immunities if len(self.immunities) > 0 else "none"}
            - attack: {self.damage + self.boost} {self.attack_type} damage
            - initiative: {self.initiative}
            - effective power: {self.effective_power}
            """

def solution_part1(fname: str = f"inputs/{os.path.basename(__file__)[:-3]}.txt"):
        groups, immune_groups, infection_groups = parse_input(fname)
        return simulate_combat(groups, immune_groups, infection_groups)[0]

def parse_input(fname: str):
    with open(fname, "r") as f:
        groups: set[Group] = set()
        immune_groups: set[Group] = set()
        infection_groups: set[Group] = set()
        army = -1
        count = 1
        for line in f:
            if len(line) == 1:
                continue
            elif line[:6] == "Immune":
                count = 1
                army = IMMUNE
            elif line[:9] == "Infection":
                count = 1
                army = INFECTION
            else:
                m = LINE_REGEX.match(line)
                if m:
                    units = int(m.group(1))
                    hp = int(m.group(2))
                    weaknesses: set[str] = set()
                    immunities: set[str] = set()
                    if m.group(3):
                        target = weaknesses if m.group(3) == "weak" else immunities
                        for attribute in m.group(4).split(","):
                            target.add(attribute.strip())
                    if m.group(5):
                        target = weaknesses if m.group(5) == "weak" else immunities
                        for attribute in m.group(6).split(","):
                            target.add(attribute.strip())
                    damage = int(m.group(7))
                    attack_type = m.group(8)
                    initiative = int(m.group(9))
                    g = Group(count, army, units, hp, weaknesses, immunities, damage, attack_type, initiative)
                    groups.add(g)
                    [immune_groups, infection_groups][army].add(g)
                    count += 1
                else:
                    custom_print(f"NO MATCH: {line}")
        return groups, immune_groups, infection_groups


def simulate_combat(groups: set[Group], immune_groups: set[Group], infection_groups: set[Group]):
    seen_states: set[tuple] = set()

    while len(immune_groups) > 0 and len(infection_groups) > 0:
        sorted_immune_groups = list(immune_groups)
        sorted_immune_groups.sort(key=lambda g: g.id)
        sorted_infection_groups = list(infection_groups)
        sorted_infection_groups.sort(key=lambda g: g.id)

        custom_print("Immune System:")
        for g in sorted_immune_groups:
            custom_print(f"Group {g.id} contains {g.units} units")

        custom_print("Infection:")
        for g in sorted_infection_groups:
            custom_print(f"Group {g.id} contains {g.units} units")
        custom_print("")


        # target selection phase
        sorted_groups = list(groups)
        sorted_groups.sort(key=lambda g: (g.effective_power(), g.initiative), reverse=True)

        attacks: dict[tuple[int, int], Group] = {}
        remaining_immune_defenders: set[Group] = set([g for g in immune_groups])
        remaining_infection_defenders: set[Group] = set([g for g in infection_groups])

        for attacker in sorted_groups:
            sorted_enemy_army = list([remaining_immune_defenders, remaining_infection_defenders][(attacker.army + 1) % 2])
            if len(sorted_enemy_army) == 0:
                continue
            sorted_enemy_army.sort(key=lambda g: (attacker.damage_given_to(g), g.effective_power(), g.initiative), reverse=True)

            target = sorted_enemy_army[0]
            if attacker.damage_given_to(target) == 0:
                continue
            [remaining_immune_defenders, remaining_infection_defenders][(attacker.army + 1) % 2].remove(target)
            custom_print(f"{'Infection' if attacker.army == INFECTION else 'Immune System'} group {attacker.id} would deal defending group {target.id} {attacker.damage_given_to(target)} damage")
            attacks[(attacker.army, attacker.id)] = target

        # attack phase
        custom_print("")
        sorted_groups.sort(key=lambda g: g.initiative, reverse=True)
        for attacker in sorted_groups:
            if (attacker.army, attacker.id) not in attacks:
                continue
            defender = attacks[(attacker.army, attacker.id)]
            if attacker not in groups or defender not in groups:
                continue
            attacker.attack(defender)
            if defender.units <= 0:
                groups.remove(defender)
                [immune_groups, infection_groups][defender.army].remove(defender)
        custom_print("")

        state = tuple([(g.army, g.id, g.units) for g in groups])
        if state in seen_states:
            return -1, None
        seen_states.add(state)

    winning_army_name = IMMUNE if len(immune_groups) > 0 else INFECTION
    winning_army = immune_groups if len(immune_groups) > 0 else infection_groups
    return sum([g.units for g in winning_army]), winning_army_name


def solution_part2(fname: str = f"inputs/{os.path.basename(__file__)[:-3]}.txt"):
    original_groups, original_immune_groups, original_infection_groups = parse_input(fname)
    boost_bounds = (0, 2)

    finding_upper_bound = True

    while True:
        boost = (boost_bounds[0] + boost_bounds[1]) // 2
        custom_print(f"testing boost {boost}")

        groups: set[Group] = set()
        immune_groups: set[Group] = set()
        infection_groups: set[Group] = set()

        for og in original_groups:
            g = Group(og.id, og.army, og.units, og.hp, og.weaknesses, og.immunities, og.damage, og.attack_type, og.initiative, boost if og.army == IMMUNE else 0)
            groups.add(g)
            [immune_groups, infection_groups][g.army].add(g)

        combat_result, winner = simulate_combat(groups, immune_groups, infection_groups)

        if finding_upper_bound:
            if winner == IMMUNE:
                boost_bounds = (boost // 2 + 1, boost)
                finding_upper_bound = False
            else:
                boost_bounds = (0, boost * 4)
            continue

        if boost_bounds[0] == boost_bounds[1]:
            if winner == IMMUNE:
                return combat_result
            else:
                boost_bounds = (boost_bounds[0] + 1, boost_bounds[0] + 1)
                continue

        if winner == IMMUNE:
            if boost == boost_bounds[1] - 1:
                return combat_result
            boost_bounds = (boost_bounds[0], boost - 1)
        else:
            boost_bounds = (boost + 1, boost_bounds[1])


print(solution_part1())
print(solution_part2())
