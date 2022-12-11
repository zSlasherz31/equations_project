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
    win_instr.geometry(f'530x250+{win.winfo_rootx()}+{win.winfo_rooty()}')
    win_instr.config(bg='black')
    win_instr.title('Инструкция')
    win_instr.resizable(False, False)
    win_instr.transient(win)

    # Виджет с инструкцией

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
    win_instr.after(60000, lambda: win_instr.destroy())


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
        c = (a + b) / 2
        x = c
        y3 = eval(s)
        if y1 * y3 < 0:
            b = c
        else:
            a = c
    return round((a + b) / 2, 4)


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


def check(_event):  # В качестве аргумента можно ввести что угодно, но _event не выдаёт предупреждение.
    """Проверяет на правильность ввода и выводит окно ошибки, либо найденные корни."""
    main_s = entry1.get().replace('^', '**')
    try:
        final_solve = solve(main_s)
    except (ZeroDivisionError, NameError, SyntaxError):
        button_solve.config(image=incor_btn_slv_photo)
        label_roots.config(text='')
        mb.showerror('Ошибка ввода', '''Возможно следует дописать уравнение, либо исключить
русские буквы, английские (кроме «x»), спецсимволы (кроме «*», «/», «^»), пустую строку (пробел), ДЕЛЕНИЕ
на 0, возведение в степень «x» или же повторяющиеся символы''')
        button_solve.config(image=default_btn_slv_photo)
    else:
        button_solve.config(image=cor_btn_slv_photo)
        if final_solve.count('x') > 1:
            label_roots.config(text=f'Корни вашего уравнения:\n{final_solve}')
        elif final_solve.count('x') == 1:
            label_roots.config(text=f'Корень вашего уравнения:\n{final_solve}')
        else:
            label_roots.config(text='Данное уравнение не имеет действительных корней')
        win.after(4000, lambda: button_solve.config(image=default_btn_slv_photo))


# Главное окно
win = tk.Tk()
main_photo = tk.PhotoImage(file='resources/ico_image.png')
win.iconphoto(True, main_photo)
win.title('Equations')
win.state('zoomed')
win.minsize(875, 855)
win.config(bg='black')
win.protocol('WM_DELETE_WINDOW', on_exit)

# Все последующие элементы расположены в правильном порядке 'прилипания' друг к другу (на это указывает 'side='
# (по умолчанию tk.TOP - константа), либо 'anchor='); файл с функционалом .pack() оставлю в проекте с задачами
# Кнопка помощи.

button_help_photo = tk.PhotoImage(file='resources/instr_image.png')
button_help = tk.Button(win, image=button_help_photo, background='black',
                        borderwidth=0, activebackground='black')
button_help.pack(anchor=tk.NW)

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
button_solve = tk.Button(win, image=default_btn_slv_photo, background='black',
                         borderwidth=0, activebackground='black')
button_solve.pack(pady=30)

# Виджет неонового GIFa.

gif_frame_cnt = 52
neon_bg = [tk.PhotoImage(file='resources/neon_bg.gif', format=f'gif -index {i}') for i in range(gif_frame_cnt)]
label_neon = tk.Label(win, bg='black')
label_neon.pack(pady=40)
neon_gif_update(0)

# Виджет корней.

label_roots = tk.Label(win, text='', bg='black', fg='purple', font=('Segoe UI Variable Text Light', 20))
label_roots.pack(pady=20)

# Виджет кривой полосы снизу.

bottom_curve_line_photo = tk.PhotoImage(file='resources/bottom_curve_line_image.png')
bottom_curve_line = tk.Label(image=bottom_curve_line_photo, background='black', activebackground='black')
bottom_curve_line.pack(side=tk.BOTTOM, pady=20)

# Все события (клавиатура, мышь) и их описание: https://stackoverflow.com/questions/32289175/list-of-all-tkinter-events
#                      |
button_solve.bind('<Button-1>', check)
entry1.bind('<Return>', check)
button_help.bind('<Button-1>', instr)
entry1.bind('<Button-1>', hide_temp_text)

win.mainloop()
