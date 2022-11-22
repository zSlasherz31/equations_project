"""Программа предоставляет возможность находить корни уравнений.
Графический интерфейс осуществлен с помощью встроенного графического модуля Tkinter.
"""

import tkinter as tk
from tkinter import messagebox as mb


def on_exit():
    """Выводит диалоговое окно при закрытии главного окна."""
    if mb.askokcancel('Выход из приложения', 'Хотите выйти из приложения?'):
        win.destroy()


def hide_temp_text(_event):
    """Скрывает временный текст в поле ввода."""
    if entry1.get() == 'Введите уравнение...':
        entry1.delete(0, tk.END)
    entry1.config(fg='#00fee9')


def instr(_event):
    """Открывает/закрывает окно с инструкцией ввода."""
    # Дочернее окно

    win_instr = tk.Toplevel()
    win_instr.bell()  # Проигрывает дефолтный звук windows, поведение меняется его изменением в windows
    w, h = 530, 250
    win_instr.geometry(f'{w}x{h}+{(win.winfo_width() - w) // 2}+{(win.winfo_height() - h) // 2}')
    win_instr.config(bg='black')
    win_instr.title('Инструкция')
    win_instr.resizable(False, False)

    # Виджет в новом окне с инструкцией (в переменную не сохраняется)

    tk.Label(win_instr, text='''Как решить уравнение:
    1. Нажать на поле ввода (надпись «Введите уравнение...»).
    2. Ввести уравнение, используя требования ниже.
    3. Нажать кнопку «Решить уравнение» под полем ввода или клавишу enter.

При вводе уравнения заменить привычные математические действия:
    1. Умножения на «*».
    2. Деления на «/».
    3. Возведения в степень на «^».
Уравнение должно быть записано относительно строчной 
переменной x (английская буква «x») без приравнивания к 0!
    
Это окно можно перетаскивать.''', bg='black', fg='purple',
             font=('Calibri', 11),
             justify=tk.LEFT).pack()


def neon_gif_update(indx):
    """Переключает кадры GIF-ки, находящиеся в neon_bg."""
    frame = neon_bg[indx]
    indx += 1
    if indx == gif_frame_cnt:
        indx = 0
    label_neon.config(image=frame)
    win.after(140, neon_gif_update, indx)


def root(s, a, b):
    """Уточняет корень на отрезке."""
    eps = 0.00001
    while b - a > eps:
        x = a
        y1 = eval(s)
        x = b
        y2 = eval(s)
        c = (a + b) / 2
        x = c
        y3 = eval(s)
        if y1 * y3 < 0:
            b = c
        else:
            a = c
    return round((a + b) / 2, 4)


def solve(s):
    """Находит отрезки с корнями."""
    h, x1, final_roots = 1, -10000, ''
    while x1 <= 10000:
        x = x1
        y1 = eval(s)
        x = x1 + h
        y2 = eval(s)
        if y1 * y2 < 0:
            final_roots += f'x ≈ {str(root(s, x1, x1 + h))}\n'
        x1 += h
    return final_roots


def check(_event):  # В качестве аргумента можно ввести что угодно, но _event не выдаёт предупреждение.
    """Проверяет на правильность ввода и выводит ошибку/ошибки, либо найденные корни."""
    s = entry1.get().replace('^', '**')
    check_correct, check_correct_zero = 0, 0
    if s.count('/0') > 0:
        check_correct_zero += 1
    if 0 <= len(s) <= 5 or s[-1] in '-+/*^' or s.count('--' or '++' or '****' or '**x' or '**X' or 'xx') > 0:
        check_correct += 1
    else:
        for elem in s:
            if elem in r'''abcdefghijklmnopqrstuvwyzABCDEFGHIJKLMNOPQRSTUVWXYZ
                        абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ
                        _!'"@№#$%;:&?=,.<>~`\|''':
                check_correct += 1
    if check_correct != 0 and check_correct_zero != 0:
        label_roots.config(text='')
        mb.showerror('Ошибка ввода', '''Возможно следует дописать уравнение, либо исключить
русские буквы, английские (кроме «x»), спецсимволы (кроме «*», «/», «^»), пустую строку (пробел), ДЕЛЕНИЕ
на 0, возведение в степень «x» или же повторяющиеся символы''')
    elif check_correct != 0:
        label_roots.config(text='')
        mb.showerror('Ошибка ввода', '''Возможно следует дописать уравнение, либо исключить
русские буквы, английские (кроме «x»), спецсимволы (кроме «*», «/», «^»), пустую строку (пробел), возведение 
в степень «x» или же повторяющиеся символы''')
    elif check_correct_zero != 0:
        label_roots.config(text='')
        mb.showerror('Ошибка ввода', 'Делить на ноль нельзя!')
    else:
        final_solve = solve(s)
        if final_solve.count('x') == 1:
            label_roots.config(text=f'Корень вашего уравнения:\n{final_solve}')
        elif final_solve.count('x') > 1:
            label_roots.config(text=f'Корни вашего уравнения:\n{final_solve}')
        else:
            label_roots.config(text='Данное уравнение не имеет действительных корней')


# Главное окно
win = tk.Tk()
main_photo = tk.PhotoImage(file='resources/ico_photo.png')
win.iconphoto(True, main_photo)
win.title('Equations')
win.state('zoomed')
win.minsize(884, 878)
win.config(bg='black')
win.protocol('WM_DELETE_WINDOW', on_exit)

# Все последующие элементы расположены в правильном порядке 'прилипания' друг к другу (на это указывает 'side='
# (по умолчанию tk.TOP - константа), либо 'anchor='); файл с функционалом .pack() оставлю в проекте с задачами
# Кнопка помощи.

button_help = tk.Button(win, text='Инструкция(показать/скрыть)', font=('Calibri', 11),
                        bg='black', fg='purple', relief=tk.SOLID,
                        activeforeground='purple',
                        activebackground='black')
button_help.pack(anchor=tk.NW)

# Поле ввода.

entry1 = tk.Entry(win, font=('Segoe UI Variable Text Light', 50),
                  bg='black', fg='#626262', width=25, justify=tk.CENTER,
                  cursor='tcross',  # Курсоры: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html
                  insertbackground='#626262')
entry1.insert(0, 'Введите уравнение...')
entry1.pack(pady=30)

# Кнопка решения уравнения.

button_solve = tk.Button(win, text='Решить уравнение', bg='black', fg='purple',
                         font=('Segoe UI Variable Text Light', 20),
                         activeforeground='purple',
                         activebackground='black')
button_solve.pack(pady=30)

# Виджет неонового GIFa.

gif_frame_cnt = 52
neon_bg = [tk.PhotoImage(file='resources/neon_bg.gif', format=f'gif -index {i}') for i in range(gif_frame_cnt)]
label_neon = tk.Label(win, bg='black')
label_neon.pack(pady=40)
neon_gif_update(0)

# Виджет корней.

label_roots = tk.Label(win, text='', bg='black', fg='purple',
                       font=('Segoe UI Variable Text Light', 20))
label_roots.pack(pady=20)

# Все события (клавиатура, мышь) и их описание: https://stackoverflow.com/questions/32289175/list-of-all-tkinter-events
#                      |
button_solve.bind('<Button-1>', check)
entry1.bind('<Return>', check)
button_help.bind('<Button-1>', instr)
entry1.bind('<Button-1>', hide_temp_text)

win.mainloop()
