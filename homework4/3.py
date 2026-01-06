"""Гнучкий механізм для обробки різноманітних ігрових подій"""


class GameEventException(Exception):
    """Клас винятку для обробки ігрових подій"""

    def __init__(self, event_type: str, details: dict):
        """Ініціалізує виняток з типом події та деталями"""
        super().__init__(f"Сталася подія в грі: {event_type}")
        self.event_type = event_type
        self.details = details

    def __str__(self):
        """Повертає рядкове представлення винятку"""
        return f"[{self.event_type}] Деталі: {self.details}"


def player_death(cause: str):
    """Симуляція події смерті гравця"""
    raise GameEventException("Смерть", {"cause": cause})


def player_level_up(new_level: int, xp: int):
    """Симуляція події підняття рівня гравця"""
    raise GameEventException("levelUp", {"new_level": new_level, "xp_gained": xp})


if __name__ == "__main__":
    try:
        player_death("удар мечем")

    except GameEventException as e:
        print("⚠️ Виникла ігрова подія!")
        print(e)

        if e.event_type == "Смерть":
            print(f"Гравець загинув. Причина: {e.details['cause']}")
        elif e.event_type == "levelUp":
            print(f"Гравець досяг рівня {e.details['new_level']} "
                  f"і отримав {e.details['xp_gained']} XP")
