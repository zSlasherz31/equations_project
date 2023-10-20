# Меняющиеся в процессе выполнения программы переменные хранятся как атрибуты класса Vars


class Vars:
    sounds_on: bool = True
    from_x: int = -1000
    to_x: int = 1000
    recent_solves_scrolled_text_string: str = 'Последние решения этой сессии.\n\n'


__all__ = ['Vars']
