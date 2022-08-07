from dataclasses import dataclass, asdict
from typing import Union, Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Функция вывода сообщения о тренировке."""

        message = ("Тип тренировки: {}; "
                   "Длительность: {:.3f} ч.; "
                   "Дистанция: {:.3f} км; "
                   "Ср. скорость: {:.3f} км/ч; "
                   "Потрачено ккал: {:.3f}.")
        return message.format(*asdict(self).values())
    pass


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000
    action: int
    duration: float
    weight: float

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:

        self.action = action
        self.duration = duration
        self.weight = weight

        pass

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Определите show_training_info в %s.'
                                  % (self.__class__.__name__))

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage("Training",
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        COEFF_CALORIE_1: float = 18
        COEFF_CALORIE_2: float = 20

        return ((COEFF_CALORIE_1 * self.get_mean_speed()
                 - COEFF_CALORIE_2) * self.weight / self.M_IN_KM
                * (self.duration * 60))

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage("Running",
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    action: int
    duration: float
    weight: float
    height: Union[int, float]

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: Union[int, float]
                 ) -> None:

        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        COEFF_CALORIE_1: float = 0.035
        COEFF_CALORIE_2: float = 0.029
        COEFF_CALORIE_3: float = 60

        return ((COEFF_CALORIE_1 * self.weight
                 + (self.get_mean_speed()**2 // self.height)
                 * COEFF_CALORIE_2 * self.weight)
                * (self.duration * COEFF_CALORIE_3))

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage("SportsWalking",
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    action: int
    duration: float
    weight: float
    length_pool: float
    count_pool: int

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:

        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        COEFF_CALORIE_1: float = 1.1

        return ((self.get_mean_speed()
                 + COEFF_CALORIE_1) * 2 * self.weight)

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage("Swimming",
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    SPORTS_DICTIONARY: Dict[str, Type[Training]] = {
        "SWM": Swimming,
        "RUN": Running,
        "WLK": SportsWalking,
    }

    if workout_type not in SPORTS_DICTIONARY:
        return KeyError
    else:
        return SPORTS_DICTIONARY[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info()
    print(info.get_message())
    pass


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
