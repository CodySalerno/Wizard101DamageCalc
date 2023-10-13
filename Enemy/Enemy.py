class Enemy:
    enemy_list = []

    def __init__(self, name: str, health: int, resists: dict[str, int] = None, weaknesses: dict[str, int] = None):
        self.name = name
        self.health = health
        self.resists = resists
        self.weaknesses = weaknesses
        Enemy.enemy_list.append(self)

    def __repr__(self):
        return f"Name: {self.name}\nHealth: {self.health}\nResists: {self.resists}\nWeaknesses: {self.weaknesses}"
