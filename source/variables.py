# Меняющиеся в процессе выполнения программы переменные


class Variables:
    with open('settings.txt') as settings:
        frames_delay: int = int(next(settings))
        sound_mode: str = next(settings)
    solved: str = 'Недавно решённые.\n\n'


if __name__ == '__main__':
    print(Variables.__dict__)

__all__ = ['Variables']
