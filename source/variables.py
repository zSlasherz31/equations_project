# Меняющиеся в процессе выполнения программы переменные


class Variables:
    try:
        settings = open(R'logs/settings.txt')
    except FileNotFoundError:
        frames_delay: str = '500'
        sound_mode: str = 'default'
    else:
        frames_delay, sound_mode = (setting.strip() for setting in settings)
        settings.close()
    solved: str = 'Недавно решённые.\n\n'


if __name__ == '__main__':
    print(Variables.__dict__)

__all__ = ['Variables']
