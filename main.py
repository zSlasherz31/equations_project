"""Программа предоставляет возможность находить корни уравнений.
Графический интерфейс осуществлен с помощью встроенного графического модуля Tkinter.
"""

import tkinter as tk
from tkinter import messagebox as mb
from tkinter import scrolledtext as st
import winsound as ws

# Константы.
# NORMAL_SOUND_PLAY_BREAK создается сразу для удобства, т.к. используется часто.
NORMAL_SOUND_PLAY_BREAK = ws.SND_FILENAME + ws.SND_ASYNC + ws.SND_NODEFAULT

instr_text_string = '''(1) Как решить уравнение:
    • Нажать на поле ввода (надпись «Введите уравнение...»);
    • Ввести уравнение, используя требования в пункте (2) и (3);
    • Нажать кнопку «Решить уравнение» под полем ввода или клавишу enter.

(2) При вводе уравнения заменить привычные математические действия:
    • Умножения на «*»;
    • Деления на «/»;
    • Возведения в степень на «^».

(3) Уравнение должно быть записано относительно строчной 
переменной x (английская буква «x») с приравниванием к 0 или без.

Примеры: 
3 ^ 8 * x ^ 3 + 2 * x ^ 2 + 12 = 0
(-x / 7.6 + 2) * (12 + x) * x ^ 3 - 21 ^ 2 / (3 * x - 4) ^ 2 - 12,1 * 3 ^ 21'''

check_error_find_roots_string = '''Возможно следует дописать уравнение, либо исключить
русские буквы, английские (кроме «x»), спецсимволы (кроме «*», «/», «^» и скобок), пустую строку, ДЕЛЕНИЕ
на 0 или же повторяющиеся символы.'''

recent_solves_scrolled_text_string = 'Последние решения этой сессии.\n\n'


def instr():
    """Открывает окно с инструкцией ввода (сама закрывает через 200 с.)."""
    # Дочернее окно.
    win_instr = tk.Toplevel()
    # Появляется в левом верхнем углу.
    win_instr.geometry(f'530x295+{win_main.winfo_rootx()}+{win_main.winfo_rooty()}')
    win_instr.config(bg='black')
    win_instr.title('Инструкция')
    win_instr.resizable(False, False)
    win_instr.transient(win_main)
    win_instr.protocol('WM_DELETE_WINDOW',
                       lambda: (win_instr.destroy(), ws.PlaySound('sounds/pong.wav', NORMAL_SOUND_PLAY_BREAK)))
    # Для инструкции используется Text.
    instr_text = tk.Text(win_instr, background='black', foreground='purple', font=('Calibri', 11),
                         relief='solid', selectforeground='#00fee9', selectbackground='black')
    instr_text.delete('1.0', '1111.1111')
    instr_text.insert('1.0', instr_text_string)
    instr_text.config(state='disabled')
    instr_text.pack()
    # Звук открытия, затем вызов автоматического закрытия через 200 с.
    ws.PlaySound('sounds/ping.wav', NORMAL_SOUND_PLAY_BREAK)
    win_instr.after(200000, lambda: win_instr.destroy())
    return 1


def recent_solves():
    """Открывает окно с последними решениями (сама закрывает через 200 с.)."""
    # Дочернее окно.
    win_recent = tk.Toplevel()
    # Появляется в правом верхнем углу.
    win_recent.geometry(f'530x295+{win_main.winfo_rootx() + win_main.winfo_width() - 545}+{win_main.winfo_rooty()}')
    win_recent.config(bg='black')
    win_recent.title('Последние решения')
    win_recent.resizable(False, False)
    win_recent.transient(win_main)
    win_recent.protocol('WM_DELETE_WINDOW',
                        lambda: (win_recent.destroy(), ws.PlaySound('sounds/pong.wav', NORMAL_SOUND_PLAY_BREAK)))
    # Для недавних решений используется ScrolledText.
    recent_solves_scrolled_text = st.ScrolledText(win_recent, background='black', foreground='purple',
                                                  relief='solid', font=('Calibri', 11), selectforeground='#00fee9',
                                                  selectbackground='black')
    recent_solves_scrolled_text.delete('1.0', '111.1111')
    recent_solves_scrolled_text.insert('1.0', recent_solves_scrolled_text_string)
    recent_solves_scrolled_text.tag_config('tag', justify='center')
    recent_solves_scrolled_text.tag_add('tag', '1.0', '1111.1111')
    recent_solves_scrolled_text.config(state='disabled')
    recent_solves_scrolled_text.pack()
    # Звук открытия, затем вызов автоматического закрытия через 200 с.
    ws.PlaySound('sounds/ping.wav', NORMAL_SOUND_PLAY_BREAK)
    win_recent.after(200000, lambda: win_recent.destroy())
    return 1


def check(_event):
    """Проверяет на правильность ввода и выводит окно ошибки, либо найденные корни.
    В случае корректного ввода добавляет уравнение и найденные корни в recent_solves_scrolled_text_string."""
    # _event необходим для работы из-за нажатия enter (в bind) для решения, без него можно
    # просто назначить command кнопке, как сделано в остальных случаях и не указывать _event).
    global recent_solves_scrolled_text_string
    main_s = entry_center.get().replace('^', '**').replace(',', '.').replace(' ', '')
    equal_sign = main_s.rfind('=')
    if equal_sign != -1 and main_s[equal_sign:] == '=0':
        main_s = main_s[:equal_sign]
    try:
        final_solve = solve(main_s)
    except (ZeroDivisionError, NameError, SyntaxError, TypeError):
        text_bottom.config(state='normal')
        text_bottom.delete('1.0', '1111.1111')
        text_bottom.config(state='disabled')
        button_center.config(image=button_center_incorrect_photo)
        mb.showerror('Ошибка ввода', check_error_find_roots_string)
        button_center.config(image=button_center_default_photo)
    else:
        button_center.config(image=button_center_correct_photo)
        win_main.after(4000, lambda: button_center.config(image=button_center_default_photo))
        if final_solve.count('x') > 1:
            ws.PlaySound('sounds/funky.wav', NORMAL_SOUND_PLAY_BREAK)
            # Операции с Text.
            text_bottom.config(state='normal')
            text_bottom.delete('1.0', '1111.1111')
            text_bottom.insert('1.0', f'Корни вашего уравнения:\n{final_solve}')
            text_bottom.tag_config('tag', justify='center')
            text_bottom.tag_add('tag', '1.0', '1111.1111')
            text_bottom.config(state='disabled')
        elif final_solve.count('x') == 1:
            ws.PlaySound('sounds/funky.wav', NORMAL_SOUND_PLAY_BREAK)
            # Операции с Text.
            text_bottom.config(state='normal')
            text_bottom.delete('1.0', '1111.1001')
            text_bottom.insert('1.0', f'Корень вашего уравнения:\n{final_solve}')
            text_bottom.tag_config('tag', justify='center')
            text_bottom.tag_add('tag', '1.0', '1111.1001')
            text_bottom.config(state='disabled')
        else:
            ws.PlaySound('sounds/boop.wav', NORMAL_SOUND_PLAY_BREAK)
            # Операции с Text.
            text_bottom.config(state='normal')
            text_bottom.delete('1.0', '1111.1111')
            text_bottom.insert('1.0', 'Данное уравнение не имеет действительных корней')
            text_bottom.tag_config('tag', justify='center')
            text_bottom.tag_add('tag', '1.0', '1111.1111')
            text_bottom.config(state='disabled')
        # Добавление решений.
        recent_solves_scrolled_text_string += f"Решение уравнения:\n{main_s.replace('**', '^')}=0\n⤋\n{final_solve}\n"
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
    if entry_center.get() == 'Введите уравнение...':
        entry_center.delete(0, 'end')
        entry_center.config(foreground='#00fee9')
    return 1


def on_exit():
    """Выводит диалоговое окно при закрытии главного окна."""
    if mb.askokcancel('Выход из приложения', 'Хотите выйти из приложения?'):
        ws.PlaySound('sounds/balloon.wav', NORMAL_SOUND_PLAY_BREAK)
        win_main.after(850, win_main.destroy())
    return 1


def neon_gif_update(indx):
    """Переключает кадры GIF-ки, находящиеся в label_center_photos."""
    frame = label_center_photos[indx]
    indx += 1
    if indx == 52:
        indx = 0
    label_center.config(image=frame)
    win_main.after(140, neon_gif_update, indx)
    return 1


# Главное окно.
win_main = tk.Tk()
main_photo = tk.PhotoImage(file='resources/ico.png')
win_main.iconphoto(True, main_photo)
win_main.title('Equations')
win_main.state('zoomed')
win_main.minsize(950, 950)
win_main.config(bg='black')
win_main.protocol('WM_DELETE_WINDOW', on_exit)

# Все последующие элементы расположены в правильном порядке 'прилипания' друг к другу (на это указывает 'side='
# (по умолчанию tk.TOP - константа), либо 'anchor=').
# Кнопка помощи.

button_left_photo = tk.PhotoImage(file='resources/lamp.png')
button_left = tk.Button(win_main, image=button_left_photo, background='black', command=instr,
                        borderwidth=0, activebackground='black')
button_left.pack(anchor=tk.NW, side=tk.LEFT, padx=15)

# Кнопка недавних.

button_right_photo = tk.PhotoImage(file='resources/recent.png')
button_right = tk.Button(win_main, image=button_right_photo, background='black', command=recent_solves,
                         borderwidth=0, activebackground='black')
button_right.pack(anchor=tk.NE, side=tk.RIGHT, padx=15, pady=40)

# Вспомогательный виджет, между кнопкой помощи и кнопкой недавних.
label_top = tk.Label(background='black')
label_top.pack(pady=35)

# Поле ввода.

entry_center = tk.Entry(win_main, font=('Segoe UI Variable Text Light', 50),
                        bg='black', fg='#626262', width=25, justify=tk.CENTER,
                        cursor='tcross',  # Курсоры: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html
                        insertbackground='#626262')
entry_center.insert(0, 'Введите уравнение...')
entry_center.pack(pady=30)

# Кнопка решения уравнения.

button_center_default_photo = tk.PhotoImage(file='resources/default_button.png')
button_center_incorrect_photo = tk.PhotoImage(file='resources/incorrect_button.png')
button_center_correct_photo = tk.PhotoImage(file='resources/correct_button.png')
button_center = tk.Button(win_main, image=button_center_default_photo, background='black',
                          borderwidth=0, activebackground='black')
button_center.pack(pady=30)

# Виджет (Label) неонового GIFa.

label_center_photos = [tk.PhotoImage(file='resources/neon.gif', format=f'gif -index {i}') for i in range(52)]
label_center = tk.Label(win_main, bg='black')
label_center.pack(pady=40)
neon_gif_update(0)

# Виджет (Text) корней.

text_bottom = tk.Text(win_main, width=45, height=6, background='black', foreground='purple',
                      font=('Segoe UI Variable Text Light', 20), relief='solid',
                      selectforeground='#00fee9', selectbackground='black')
text_bottom.pack()

# Виджет (Label) кривой полосы снизу.

label_bottom_photo = tk.PhotoImage(file='resources/curve_line.png')
label_bottom = tk.Label(image=label_bottom_photo, background='black', activebackground='black')
label_bottom.pack(side=tk.BOTTOM, pady=20)

# Все события (клавиатура, мышь) и их описание: https://stackoverflow.com/questions/32289175/list-of-all-tkinter-events
#                       |
button_center.bind('<Button-1>', check)
entry_center.bind('<Return>', check)
entry_center.bind('<Button-1>', hide_temp_text)

win_main.mainloop()
