# Шаблоны для кастомизации отдельных групп виджетов в конструкторе

from tkinter.constants import CENTER, SOLID, RIDGE
from myconstants import BLACK, PURPLE, TURQUOISE, GREY


button_options = {
    'activebackground': BLACK,
    'borderwidth': 0,
    'background': BLACK
}

entry_options = {
    'background': BLACK,
    'borderwidth': 1,
    'disabledbackground': BLACK,
    'disabledforeground': GREY,
    'foreground': TURQUOISE,
    'insertbackground': GREY,
    'insertwidth': 1,
    'justify': CENTER,
    'selectbackground': BLACK,
    'selectforeground': GREY
}

label_options = {
    'background': BLACK
}

text_options = {
    'background': BLACK,
    'foreground': PURPLE,
    'relief': SOLID,
    'selectbackground': BLACK,
    'selectforeground': TURQUOISE
}

scale_options = {
    'activebackground': BLACK,
    'background': BLACK,
    'borderwidth': 0,
    'foreground': PURPLE,
    'highlightbackground': BLACK,
    'sliderrelief': RIDGE,
    'troughcolor': GREY
}


__all__ = ['button_options', 'entry_options', 'label_options', 'text_options', 'scale_options']
