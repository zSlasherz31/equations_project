"""Программа предоставляет возможность находить корни уравнений.
Графический интерфейс осуществлен с помощью встроенного графического модуля Tkinter.
"""

import tkinter as tk
from tkinter import messagebox as mb
import winsound as ws

# Константы.
win_instr_massage = '''Как решить уравнение:
    1. Нажать на поле ввода (надпись «Введите уравнение...»).
    2. Ввести уравнение, используя требования ниже.
    3. Нажать кнопку «Решить уравнение» под полем ввода или клавишу enter.

При вводе уравнения заменить привычные математические действия:
    1. Умножения на «*».
    2. Деления на «/».
    3. Возведения в степень на «^».

Уравнение должно быть записано относительно строчной 
переменной x (английская буква «x») без приравнивания к 0!

Примеры: 
1. 3 * x^3 + 2 * x^2 + 12
2. (x / 76) * (12 + x) * x^3 - 21 / 3 * x^2 - 121 * 3'''

error_find_roots_massage = '''Возможно следует дописать уравнение, либо исключить
русские буквы, английские (кроме «x»), спецсимволы (кроме «*», «/», «^»), пустую строку (пробел), ДЕЛЕНИЕ
на 0, возведение в степень «x» или же повторяющиеся символы'''

recent_label_text = 'Последние решения этой сессии:\n'


def instr(_event):
    """Открывает окно с инструкцией ввода (сама закрывает через 60 с.)."""
    # Дочернее окно.
    win_instr = tk.Toplevel()
    win_instr.geometry(f'530x300+{win.winfo_rootx()}+{win.winfo_rooty()}')
    win_instr.config(bg='black')
    win_instr.title('Инструкция')
    win_instr.resizable(False, False)
    win_instr.transient(win)

    # Виджет с инструкцией.

    tk.Label(win_instr, text=win_instr_massage, bg='black', fg='purple',
             font=('Calibri', 11), justify=tk.LEFT).pack()
    ws.PlaySound('sounds/windows_startup.wav', ws.SND_FILENAME)
    win_instr.after(60000, lambda: win_instr.destroy())
    return 1


def recent_solves(_event):
    """Открывает окно с 3-мя последними решениями (сама закрывает через 60 с.)."""
    win_recent = tk.Toplevel()
    win_recent.geometry(f'530x300+{win.winfo_rootx() + win.winfo_width() - 545}+{win.winfo_rooty()}')
    win_recent.config(bg='black')
    win_recent.title('Последние решения')
    win_recent.resizable(False, False)
    win_recent.transient(win)

    # Расширяющийся виджет с последними решениями.

    tk.Label(win_recent, text=recent_label_text, bg='black',
             fg='purple', font=('Calibri', 11)).pack()
    ws.PlaySound('sounds/windows_startup.wav', ws.SND_FILENAME)
    win_recent.after(60000, lambda: win_recent.destroy())
    return 1


def check(_event):  # В качестве аргумента можно ввести что угодно, но _event не выдаёт предупреждение.
    """Проверяет на правильность ввода и выводит окно ошибки, либо найденные корни. Расширяет
    текст виджета недавних 3-х решений, который находится в дочернем окне, привязанном к кнопке
    недавние решения."""
    global recent_label_text
    main_s = entry1.get().replace('^', '**')
    try:
        final_solve = solve(main_s)
    except (ZeroDivisionError, NameError, SyntaxError):
        solve_button.config(image=incor_btn_slv_photo)
        roots_label.config(text='')
        mb.showerror('Ошибка ввода', error_find_roots_massage)
        solve_button.config(image=default_btn_slv_photo)
    else:
        win.bell()
        solve_button.config(image=cor_btn_slv_photo)
        if final_solve.count('x') > 1:
            roots_label.config(text=f'Корни вашего уравнения:\n{final_solve}')
        elif final_solve.count('x') == 1:
            roots_label.config(text=f'Корень вашего уравнения:\n{final_solve}')
        else:
            roots_label.config(text='Данное уравнение не имеет действительных корней')
        win.after(4000, lambda: solve_button.config(image=default_btn_slv_photo))
        if recent_label_text.count('⤋') == 3:
            recent_label_text = 'Последние решения этой сессии:\n'
        recent_label_text += main_s.replace('**', '^') + ':\n' + final_solve + '⤋\n'
    return 1


def solve(s_x):
    """Находит отрезки с корнями."""
    h, x1, final_roots = 1, -10000, ''
    while x1 <= 10000:
        x = x1
        y1 = eval(s_x)
        x = x1 + h
        y2 = eval(s_x)
        if y1 * y2 < 0:
            final_roots += f'x ≈ {str(root(s_x, x1, x1 + h))}\n'
        x1 += h
    return final_roots


def root(s, a, b):
    """Уточняет корень на отрезке."""
    eps = 0.00001
    while b - a > eps:
        x = a
        y1 = eval(s)
        c = (a + b) / 2
        x = c
        y3 = eval(s)
        if y1 * y3 < 0:
            b = c
        else:
            a = c
    return round((a + b) / 2, 4)


def hide_temp_text(_event):
    """Скрывает временный текст в поле ввода."""
    if entry1.get() == 'Введите уравнение...':
        entry1.delete(0, tk.END)
    entry1.config(fg='#00fee9')
    return 1


def on_exit():
    """Выводит диалоговое окно при закрытии главного окна."""
    if mb.askokcancel('Выход из приложения', 'Хотите выйти из приложения?'):
        win.destroy()
        ws.PlaySound('sounds/windows_balloon.wav', ws.SND_FILENAME)
    return 1


def neon_gif_update(indx):
    """Переключает кадры GIF-ки, находящиеся в neon_bg."""
    frame = neon_bg[indx]
    indx += 1
    if indx == gif_frame_cnt:
        indx = 0
    neon_label.config(image=frame)
    win.after(140, neon_gif_update, indx)
    return 1


# Главное окно.
win = tk.Tk()
main_photo = tk.PhotoImage(file='resources/ico_image.png')
win.iconphoto(True, main_photo)
win.title('Equations')
win.state('zoomed')
win.minsize(950, 950)
win.config(bg='black')
win.protocol('WM_DELETE_WINDOW', on_exit)

# Все последующие элементы расположены в правильном порядке 'прилипания' друг к другу (на это указывает 'side='
# (по умолчанию tk.TOP - константа), либо 'anchor='); файл с функционалом .pack() оставил в проекте с задачами
# Кнопка помощи.

help_button_photo = tk.PhotoImage(file='resources/instr_image.png')
help_button = tk.Button(win, image=help_button_photo, background='black',
                        borderwidth=0, activebackground='black')
help_button.pack(anchor=tk.NW, side=tk.LEFT, padx=15)

# Кнопка включения фонового звука.

# turn_bg_sound = True
recent_button_photo = tk.PhotoImage(file='resources/recent_button_image.png')
recent_button = tk.Button(win, image=recent_button_photo, background='black',
                          borderwidth=0, activebackground='black')
recent_button.pack(anchor=tk.NE, side=tk.RIGHT, padx=15, pady=40)

# Вспомогательный виджет, между кнопкой помощи и кнопкой включения фонового звука.
supportive_label = tk.Label(background='black')
supportive_label.pack(pady=35)

# Поле ввода.

entry1 = tk.Entry(win, font=('Segoe UI Variable Text Light', 50),
                  bg='black', fg='#626262', width=25, justify=tk.CENTER,
                  cursor='tcross',  # Курсоры: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html
                  insertbackground='#626262')
entry1.insert(0, 'Введите уравнение...')
entry1.pack(pady=30)

# Кнопка решения уравнения.

default_btn_slv_photo = tk.PhotoImage(file='resources/default_btn_slv_image.png')
incor_btn_slv_photo = tk.PhotoImage(file='resources/incor_btn_slv_image.png')
cor_btn_slv_photo = tk.PhotoImage(file='resources/cor_btn_slv_image.png')
solve_button = tk.Button(win, image=default_btn_slv_photo, background='black',
                         borderwidth=0, activebackground='black')
solve_button.pack(pady=30)

# Виджет неонового GIFa.

gif_frame_cnt = 52
neon_bg = [tk.PhotoImage(file='resources/neon_bg.gif', format=f'gif -index {i}') for i in range(gif_frame_cnt)]
neon_label = tk.Label(win, bg='black')
neon_label.pack(pady=40)
neon_gif_update(0)

# Виджет корней.

roots_label = tk.Label(win, text='', bg='black', fg='purple',
                       font=('Segoe UI Variable Text Light', 20))
roots_label.pack(pady=20)

# Виджет кривой полосы снизу.

bottom_curve_line_photo = tk.PhotoImage(file='resources/bottom_curve_line_image.png')
bottom_curve_line_label = tk.Label(image=bottom_curve_line_photo, background='black', activebackground='black')
bottom_curve_line_label.pack(side=tk.BOTTOM, pady=20)

# Все события (клавиатура, мышь) и их описание: https://stackoverflow.com/questions/32289175/list-of-all-tkinter-events
#                      |
help_button.bind('<Button-1>', instr)
recent_button.bind('<Button-1>', recent_solves)
solve_button.bind('<Button-1>', check)
entry1.bind('<Button-1>', hide_temp_text)
entry1.bind('<Return>', check)

win.mainloop()
