"""Програма - таймер для тренування"""

DEFAULT_TIME: int = 60


def training_session(rounds: int) -> None:
    """Функція, яка симулює тренувальну сесію з можливістю
    змінювати час кожного раунду.
    """
    time_per_round: int = DEFAULT_TIME


    def adjust_time(decrease: int) -> None:
        """Вкладена функція для коригування часу"""
        nonlocal time_per_round
        time_per_round -= decrease


    for i in range(1, rounds + 1):
        if i == 1:
            print(f"Раунд {i}: {time_per_round} хвилин")
        else:
            adjust_time(5)
            print(f"Раунд {i}: {time_per_round} хвилин (після коригування часу)")


training_session(3)
