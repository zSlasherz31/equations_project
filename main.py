"""
Графический интерфейс осуществлен с помощью встроенного графического модуля Tkinter.
Предоставляется возможность находить корни уравнений.
Полезные ссылки:
https://www.figma.com
https://www.colorspire.com
https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/index.html
"""

import tkinter as tk
import winsound as ws
from tkinter import (messagebox as mb,
                     scrolledtext as st)

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
x ^ 3 + 1 = 0
3 ^ 8 * x ^ 3 + 2 * x ^ 2 + 12 = 0
(-x / 7.6 + 2) * (12 + x) * x ^ 3 - 21 ^ 2 / (3 * x - 4) ^ 21 * 3 ^ 21

Любой текст можно копировать с помощью выделения, а затем нажатия
сочетания клавиш ctrl + c. Копировать можно примеры, найденные корни
последние решения и т.д. Найденные корни можно пролистывать, если
их слишком много. Также, можно включать или выключать
дополнительные звуки.'''

check_error_find_roots_string = '''Возможно следует дописать уравнение, либо исключить
русские буквы, английские (кроме «x»), спецсимволы (кроме «*», «/», «^» и скобок), пустую строку, ДЕЛЕНИЕ
на 0, повторяющиеся символы и т.д.'''

recent_solves_scrolled_text_string = 'Последние решения этой сессии.\n\n'


def instr() -> None:
    """Открывает окно с инструкцией ввода (сама закрывает через 200 с.)."""
    # Дочернее окно.
    win_instr = tk.Toplevel()
    # Появляется в левом верхнем углу.
    win_instr.geometry(f'530x295+{win_main.winfo_rootx()}+{win_main.winfo_rooty()}')
    win_instr.config(bg='black')
    win_instr.title('Инструкция')
    win_instr.resizable(False, False)
    win_instr.transient(win_main)
    win_instr.protocol('WM_DELETE_WINDOW', lambda:
                       (win_instr.destroy(), ws.PlaySound('sounds/pong.wav', NORMAL_SOUND_PLAY_BREAK))
                       if sounds_on else win_instr.destroy())
    # Для инструкции используется Text.
    instr_scrolled_text = st.ScrolledText(win_instr, background='black', foreground='purple', font=('Calibri', 11),
                                          relief='solid', selectforeground='#00fee9', selectbackground='black')
    instr_scrolled_text.delete('0.0', 'end')
    instr_scrolled_text.insert('0.0', instr_text_string)
    instr_scrolled_text.tag_config('tag', font=('Calibri', 11, 'italic', 'bold'), justify='center')
    instr_scrolled_text.tag_add('tag', '19.0', 'end')
    instr_scrolled_text.config(state='disabled')
    instr_scrolled_text.pack()
    # Звук открытия при выключенном бесшумном режиме, затем вызов автоматического закрытия через 200 с.
    if sounds_on:
        ws.PlaySound('sounds/ping.wav', NORMAL_SOUND_PLAY_BREAK)
    win_instr.after(200000, lambda: win_instr.destroy())


def recent_solves() -> None:
    """Открывает окно с последними решениями (сама закрывает через 200 с.)."""
    # Дочернее окно.
    win_recent = tk.Toplevel()
    # Появляется в правом верхнем углу.
    win_recent.geometry(f'530x295+{win_main.winfo_rootx() + win_main.winfo_width() - 545}+{win_main.winfo_rooty()}')
    win_recent.config(bg='black')
    win_recent.title('Последние решения')
    win_recent.resizable(False, False)
    win_recent.transient(win_main)
    win_recent.protocol('WM_DELETE_WINDOW', lambda:
                        (win_recent.destroy(), ws.PlaySound('sounds/pong.wav', NORMAL_SOUND_PLAY_BREAK))
                        if sounds_on else win_recent.destroy())
    # Для недавних решений используется ScrolledText.
    recent_solves_scrolled_text = st.ScrolledText(win_recent, background='black', foreground='purple', relief='solid',
                                                  font=('Calibri', 11), selectforeground='#00fee9',
                                                  selectbackground='black')
    recent_solves_scrolled_text.delete('0.0', 'end')
    recent_solves_scrolled_text.insert('0.0', recent_solves_scrolled_text_string)
    recent_solves_scrolled_text.tag_config('tag', justify='center')
    recent_solves_scrolled_text.tag_add('tag', '0.0', 'end')
    recent_solves_scrolled_text.config(state='disabled')
    recent_solves_scrolled_text.pack()
    # Звук открытия при выключенном бесшумном режиме, затем вызов автоматического закрытия через 200 с.
    if sounds_on:
        ws.PlaySound('sounds/ping.wav', NORMAL_SOUND_PLAY_BREAK)
    win_recent.after(200000, lambda: win_recent.destroy())


def check(_event) -> None:
    """Проверяет на правильность ввода и выводит окно ошибки, либо найденные корни.
    В случае корректного ввода добавляет уравнение и найденные корни в recent_solves_scrolled_text_string."""
    # _event необходим для работы из-за нажатия enter (в bind) для решения, без него можно
    # просто назначить command кнопке, как сделано в остальных случаях и не указывать _event.
    global recent_solves_scrolled_text_string
    main_s = entry_center.get().replace('^', '**').replace(',', '.').replace(' ', '')
    equal_sign = main_s.rfind('=')
    if equal_sign != -1 and main_s[equal_sign:] == '=0':
        main_s = main_s[:equal_sign]
    try:
        final_solve = solve(main_s)
    except (ZeroDivisionError, NameError, SyntaxError, TypeError):
        text_bottom.config(state='normal')
        text_bottom.delete('0.0', 'end')
        text_bottom.config(state='disabled')
        button_center.config(image=button_center_incorrect_photo)
        mb.showerror('Ошибка ввода', check_error_find_roots_string)
        button_center.config(image=button_center_default_photo)
    else:
        button_center.config(image=button_center_correct_photo)
        count_x = final_solve.count('x')
        # Операции с Text.
        text_bottom.config(state='normal')
        text_bottom.delete('0.0', 'end')
        if count_x > 0:
            if sounds_on:
                ws.PlaySound('sounds/funky.wav', NORMAL_SOUND_PLAY_BREAK)
            if count_x > 1:
                text_bottom.insert('0.0', f'Корни вашего уравнения:\n{final_solve}')
            else:
                text_bottom.insert('0.0', f'Корень вашего уравнения:\n{final_solve}')
        else:
            if sounds_on:
                ws.PlaySound('sounds/boop.wav', NORMAL_SOUND_PLAY_BREAK)
            text_bottom.insert('1.0', 'Данное уравнение не имеет действительных корней')
        text_bottom.tag_config('tag', justify='center')
        text_bottom.tag_add('tag', '0.0', 'end')
        text_bottom.config(state='disabled')
        win_main.after(4000, lambda: button_center.config(image=button_center_default_photo))
        # Добавление решений.
        recent_solves_scrolled_text_string += f"Решение уравнения:\n{main_s.replace('**', '^')}=0\n⤋\n{final_solve}\n"


def solve(s_x) -> str:
    """Находит отрезки с корнями."""
    # Здесь eval использует глобальную и локальную
    # области видимости, находя x в локальной.
    step, x, final_roots = 1, -10000, ''
    while x <= 10000:
        y1 = eval(s_x)
        x += step
        y2 = eval(s_x)
        if y1 * y2 < 0:
            final_roots += F'x ≈ {root(s_x, x - 1, x):.4}\n'
    return final_roots


def root(s, a, b) -> float:
    """Уточняет корень на отрезке."""
    scope, eps = {'x': ...}, 1e-5  # .00001
    while b - a > eps:
        scope['x'] = a
        y1 = eval(s, scope)
        c = (a + b) / 2
        scope['x'] = c
        y3 = eval(s, scope)
        if y1 * y3 < 0:
            b = c
        else:
            a = c
    return (a + b) / 2


def turn_off_on_sounds() -> None:
    """Выключает/включает бесшумный режим."""
    global sounds_on
    if sounds_on:
        ws.PlaySound('sounds/mute.wav', NORMAL_SOUND_PLAY_BREAK)
        button_right2.config(image=button_right2_silent_photo)
        sounds_on = False
    else:
        ws.PlaySound('sounds/unmute.wav', NORMAL_SOUND_PLAY_BREAK)
        button_right2.config(image=button_right2_normal_photo)
        sounds_on = True


def hide_temp_text(_event) -> None:
    """Скрывает временный текст в поле ввода."""
    entry_center.config(state='normal')
    if entry_center.get() == 'Введите уравнение...':
        entry_center.config(foreground='#00fee9')
        entry_center.delete(0, 'end')


def show_temp_text(_event) -> None:
    """Показывает временный текст в поле ввода."""
    if entry_center.get() == '':
        entry_center.config(foreground='#626262')
        entry_center.insert(0, 'Введите уравнение...')
        entry_center.config(state='disabled')


def on_exit() -> None:
    """Выводит диалоговое окно при закрытии главного окна."""
    if mb.askokcancel('Выход из приложения', 'Хотите выйти из приложения?'):
        if sounds_on:
            ws.PlaySound('sounds/balloon.wav', NORMAL_SOUND_PLAY_BREAK)
        win_main.after(850, win_main.destroy())


def neon_gif_update(indx) -> None:
    """Переключает кадры GIF-ки, находящиеся в label_center_photos."""
    frame = label_center_photos[indx]
    indx += 1
    if indx == 52:
        indx = 0
    label_center.config(image=frame)
    win_main.after(140, neon_gif_update, indx)


# Главное окно.
win_main = tk.Tk()
main_photo = tk.PhotoImage(file='resources/ico.png')
win_main.iconphoto(True, main_photo)
win_main.title('Equations')
win_main.state('zoomed')
win_main.minsize(840, 700)
win_main.config(bg='black')
win_main.protocol('WM_DELETE_WINDOW', on_exit)

# Кнопка помощи.

button_left_photo = tk.PhotoImage(file='resources/lamp.png')
button_left = tk.Button(win_main, image=button_left_photo, background='black', command=instr,
                        borderwidth=0, activebackground='black')
button_left.grid(row=0, column=0, padx=3, sticky='nw')

# Кнопка недавних.

button_right1_photo = tk.PhotoImage(file='resources/recent.png')
button_right1 = tk.Button(win_main, image=button_right1_photo, background='black', command=recent_solves,
                          borderwidth=0, activebackground='black')
button_right1.grid(row=0, column=2, padx=10, pady=10, sticky='ne')

# Кнопка переключения режимов звука.

sounds_on = True
button_right2_normal_photo = tk.PhotoImage(file='resources/normal.png')
button_right2_silent_photo = tk.PhotoImage(file='resources/silent.png')
button_right2 = tk.Button(win_main, image=button_right2_normal_photo, background='black', command=turn_off_on_sounds,
                          borderwidth=0, activebackground='black')
button_right2.grid(row=0, column=2, padx=14, pady=10, sticky='se')

# Поле ввода.
# Курсоры для поля ввода: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html

entry_center = tk.Entry(win_main, font=('Segoe UI Variable Text Light', 50), width=20, justify='center',
                        background='black', foreground='#626262', borderwidth=1, cursor='tcross',
                        selectforeground='#626262', selectbackground='black', disabledbackground='black',
                        insertbackground='#626262', insertwidth=1)  # Конфигурация мигающей каретки.
entry_center.insert(0, 'Введите уравнение...')
entry_center.grid(row=1, column=1, sticky='we')

# Кнопка решения уравнения.

button_center_default_photo = tk.PhotoImage(file='resources/default.png')
button_center_incorrect_photo = tk.PhotoImage(file='resources/incorrect.png')
button_center_correct_photo = tk.PhotoImage(file='resources/correct.png')
button_center = tk.Button(win_main, image=button_center_default_photo, background='black',
                          borderwidth=0, activebackground='black')
button_center.grid(row=2, column=1)

# Виджет (Label) неонового GIFa.

label_center_photos = [tk.PhotoImage(file='resources/neon.gif', format=f'gif -index {i}') for i in range(52)]
label_center = tk.Label(win_main, background='black')
label_center.grid(row=3, column=1)
neon_gif_update(0)

# Виджет (Text) корней.

text_bottom = tk.Text(win_main, width=45, height=4, background='black', foreground='purple',
                      font=('Segoe UI Variable Text Light', 20), relief='solid',
                      selectforeground='#00fee9', selectbackground='black')
text_bottom.grid(row=4, column=1)

# Виджет (Label) кривой полосы снизу.

label_bottom_photo = tk.PhotoImage(file='resources/curve_line.png')
label_bottom = tk.Label(image=label_bottom_photo, background='black')
label_bottom.grid(row=5, column=1)

# Позволяем всем использующимся колонкам и строкам увеличиваться, если есть доп. место.
# Именованный аргумент weight=1 означает, что при растяжении сетки строки и колонки
# распределят место поровну, т.к. везде стоит единица.
[win_main.columnconfigure(column, weight=1) for column in range(3)]
[win_main.rowconfigure(row, weight=1) for row in range(1, 6)]

# Все события (клавиатура, мышь) и их описание: https://stackoverflow.com/questions/32289175/list-of-all-tkinter-events
#                       |
button_center.bind('<Button-1>', check)
entry_center.bind('<Return>', check)
entry_center.bind('<Button-1>', hide_temp_text)
entry_center.bind('<BackSpace>', show_temp_text)

win_main.mainloop()
