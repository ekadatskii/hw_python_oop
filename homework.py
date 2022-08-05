from typing import Union

class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type,
                 duration,
                 distance,
                 speed,
                 calories
                ) -> None:

        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

        pass

    def get_message(self) -> str:
        """Функция вывода сообщения о тренировке."""

        message = (f'Тип тренировки: {self.training_type}; '
                   f'Длительность: {self.duration:.3f} ч.; '
                   f'Дистанция: {self.distance:.3f} км; '
                   f'Ср. скорость: {self.speed:.3f} км/ч; '
                   f'Потрачено ккал: {self.calories:.3f}.')
        return message

        
    pass


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000

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

        return self.get_distance()/self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage("Training", 
                            self.duration, 
                            self.get_distance(),
                            self.get_mean_speed(), 
                            self.get_spent_calories())

        pass


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        coeff_calorie_1 = 18
        coeff_calorie_2 = 20

        return ((coeff_calorie_1 * self.get_mean_speed()
        - coeff_calorie_2) * self.weight / self.M_IN_KM 
        * (self.duration * 60))

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        
        return InfoMessage("Running", 
                            self.duration, 
                            self.get_distance(),
                            self.get_mean_speed(), 
                            self.get_spent_calories())

    pass


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: Union[int, float]
                 ) -> None:

        super().__init__(action, duration, weight)
        self.height = height

        pass

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        coeff_calorie_1 = 0.035
        coeff_calorie_2 = 0.029

        return ((coeff_calorie_1 * self.weight 
        + (self.get_mean_speed()**2 // self.height) 
        * coeff_calorie_2 * self.weight) 
        * (self.duration * 60)) 

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        
        return InfoMessage("SportsWalking", 
                            self.duration, 
                            self.get_distance(),
                            self.get_mean_speed(),
                            self.get_spent_calories())
    pass


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38

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

        pass

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return (self.length_pool * self.count_pool 
        / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        coeff_calorie_1 = 1.1

        return ((self.get_mean_speed() 
        + coeff_calorie_1) * 2 * self.weight)  

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        
        return InfoMessage("Swimming", 
                            self.duration, 
                            self.get_distance(),
                            self.get_mean_speed(), 
                            self.get_spent_calories())

    pass


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    
    """Не совсем понятно, зачем нужен словарь? 
    Не нашел информации, как в словаре задать и применить класс"""

    try:
        if workout_type == "SWM" and len(data) >= 4:
            return Swimming(data[0], data[1], data[2], data[3], data[4])
        elif workout_type == "RUN" and len(data) >= 3:
            return Running(data[0], data[1], data[2])
        elif workout_type == "WLK" and len(data) >= 4:
            return SportsWalking(data[0], data[1], data[2], data[3])
        elif len(data) >= 3:
            return Training(data[0], data[1], data[2])
        else:
            raise Exception
    except:
            print("Объект не подходит по параметрам")
            return Training(1, 0, 0)

    pass


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
