class Enemy:
    def __init__(self, health: int, resists: dict[str, int] = None, weaknesses: dict[str, int] = None):
        self.health = health
        self.resists = resists
        self.weaknesses = weaknesses
