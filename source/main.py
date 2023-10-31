"""
Графический интерфейс осуществлен с помощью встроенного графического модуля Tkinter.
Предоставляется возможность решать любые уравнения, в которых не вводятся ограничения
аргумента (допустим, если он стоит в основании или аргументе логарифма, под корнем,
в знаменателе и так далее).
"""

# Внешние импорты
import tkinter as tk
from tkinter.messagebox import showerror, askokcancel
from tkinter.scrolledtext import ScrolledText
from winsound import PlaySound, SND_FILENAME, SND_ASYNC, SND_NODEFAULT

# Внутренние импорты
from myconstants import *
from variables import Variables
from equation import raw_to_expr, find_roots, roots_output
from validation import validate_expr
from appearance import button_options

# Составная константа для привычного воспроизведения звуков
NORMAL_PLAYBACK = SND_FILENAME + SND_ASYNC + SND_NODEFAULT


def guide() -> None:
    def on_guide_exit():
        if Variables.sound_mode == 'default':
            PlaySound(R'assets\sounds\close_popup.wav', NORMAL_PLAYBACK)
        guide_window.destroy()

    guide_window = tk.Toplevel()

    # Появляется в левом верхнем углу
    guide_window.geometry(F'532x310+{root_window.winfo_rootx()}+{root_window.winfo_rooty()}')
    guide_window.configure(background=BLACK), guide_window.title('Инструкция')
    guide_window.resizable(False, False), guide_window.transient(root_window)
    guide_window.protocol('WM_DELETE_WINDOW', on_guide_exit)

    guide_scrolled_text = ScrolledText(guide_window, background=BLACK, font=('Calibri', 11), foreground=PURPLE,
                                       height=17, relief=tk.SOLID, selectbackground=BLACK,
                                       selectforeground=TURQUOISE, width=73)
    guide_scrolled_text.insert('0.0', GUIDE_MESSAGE)
    guide_scrolled_text.tag_configure('center_alignment', justify=tk.CENTER)
    guide_scrolled_text.tag_add('center_alignment', '27.0', tk.END)
    guide_scrolled_text.configure(state=tk.DISABLED)
    guide_scrolled_text.grid(row=0, column=0)

    if Variables.sound_mode == 'default':
        PlaySound(R'assets\sounds\open_popup.wav', NORMAL_PLAYBACK)


def solved() -> None:
    def on_solved_exit() -> None:
        if Variables.sound_mode == 'default':
            PlaySound(R'assets\sounds\close_popup.wav', NORMAL_PLAYBACK)
        solved_window.destroy()

    def refresh_solved() -> None:
        refresh_text(solved_scrolled_text, Variables.solved, ('center_alignment',))
        solved_scrolled_text.see(tk.END)

    solved_window = tk.Toplevel()

    # Появляется в правом верхнем углу
    solved_window.geometry(F'533x310+{root_window.winfo_rootx() + root_window.winfo_width() - 549}'
                           F'+{root_window.winfo_rooty()}')
    solved_window.configure(background=BLACK), solved_window.title('Недавно решённые')
    solved_window.resizable(False, False), solved_window.transient(root_window)
    solved_window.protocol('WM_DELETE_WINDOW', on_solved_exit)

    refresh_button = tk.Button(solved_window, activebackground=BLACK, borderwidth=0, background=BLACK,
                               command=refresh_solved, cursor='hand2', image=refresh_image)
    refresh_button.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NW)

    solved_scrolled_text = ScrolledText(solved_window, background=BLACK, font=('Calibri', 11), foreground=PURPLE,
                                        height=17, relief=tk.SOLID, selectbackground=BLACK,
                                        selectforeground=TURQUOISE, width=67, wrap=tk.WORD)
    solved_scrolled_text.insert('0.0', Variables.solved)
    solved_scrolled_text.tag_configure('center_alignment', justify=tk.CENTER)
    solved_scrolled_text.tag_add('center_alignment', '0.0', tk.END)
    solved_scrolled_text.see(tk.END), solved_scrolled_text.configure(state=tk.DISABLED)
    solved_scrolled_text.grid(row=0, column=1)

    if Variables.sound_mode == 'default':
        PlaySound(R'assets\sounds\open_popup.wav', NORMAL_PLAYBACK)


def settings() -> None:
    def on_settings_exit() -> None:
        if Variables.sound_mode == 'default':
            PlaySound(R'assets\sounds\close_popup.wav', NORMAL_PLAYBACK)
        settings_window.destroy()

    def set_frames_delay(delay: str) -> None:
        Variables.frames_delay = delay

    settings_window = tk.Toplevel()

    # Появляется по центру
    settings_window.geometry(F'444x88+{root_window.winfo_rootx() + root_window.winfo_width() // 2 - 222}'
                             F'+{root_window.winfo_rooty() + root_window.winfo_height() // 2 - 44}')
    settings_window.configure(background=BLACK), settings_window.title('Настройки')
    settings_window.resizable(False, False), settings_window.transient(root_window)
    settings_window.protocol('WM_DELETE_WINDOW', on_settings_exit)

    speed_scale = tk.Scale(settings_window, activebackground=BLACK, background=BLACK, borderwidth=0,
                           command=set_frames_delay, font=('Calibri', 11), foreground=PURPLE, from_=1,
                           highlightbackground=BLACK, label=38 * ' ' + 'Изменение скорости GIF', length=400,
                           orient=tk.HORIZONTAL, sliderlength=40, sliderrelief=tk.RIDGE, to=1_000,
                           troughcolor=GREY)
    speed_scale.set(Variables.frames_delay)
    speed_scale.grid(row=0, column=0, padx=20, pady=10)

    if Variables.sound_mode == 'default':
        PlaySound(R'assets\sounds\open_popup', NORMAL_PLAYBACK)


def analyze_raw(_event=None) -> None:
    raw = equation_entry.get()
    expression = raw_to_expr(raw)
    if validate_expr(expression):
        solve = roots_output(find_roots(expression))
        solve_button.configure(image=solve_button_correct_image)
        refresh_text(solve_text, solve, ('center_alignment',))
        # Если включено звуковое сопровождение, воспроизвести звук
        if Variables.sound_mode == 'default':
            PlaySound(FR'assets\sounds\{'roots' if solve.count('x') else 'no_roots'}.wav', NORMAL_PLAYBACK)
        solve_button.after(2000, lambda: solve_button.configure(image=solve_button_default_image))
        # Добавить текущее решение в недавно решённые
        Variables.solved += F'⤥      {raw + (' = 0' if '=' not in raw else '')}      ⤦\n{solve}\n\n\n'
    else:
        refresh_text(solve_text, '')
        solve_button.configure(image=solve_button_incorrect_image)
        showerror('Неверный ввод', SOLVE_FAILED_ERROR_MESSAGE)
        solve_button.configure(image=solve_button_default_image)


def switch_sound_mode() -> None:
    if Variables.sound_mode == 'default':
        PlaySound(R'assets\sounds\mute.wav', NORMAL_PLAYBACK)
        sound_mode_button.configure(image=silent_sound_mode_image)
        Variables.sound_mode = 'silent'
    else:
        PlaySound(R'assets\sounds\unmute.wav', NORMAL_PLAYBACK)
        sound_mode_button.configure(image=default_sound_mode_image)
        Variables.sound_mode = 'default'


def hide_temp_entry_value(entry, which_value: str) -> None:
    entry.configure(state=tk.NORMAL)
    if entry.get() == which_value:
        entry.configure(foreground=TURQUOISE)
        entry.delete(0, tk.END)


def show_temp_entry_value(entry, which_value: str) -> None:
    if entry.get() == '':
        entry.configure(foreground=GREY)
        entry.insert(0, which_value)
        entry.configure(state=tk.DISABLED)


def on_exit() -> None:
    if askokcancel('Выход из приложения', 'Хотите выйти из приложения?'):
        open('settings.txt', 'w').write(F'{Variables.frames_delay}\n{Variables.sound_mode}')
        if Variables.sound_mode == 'default':
            PlaySound(R'assets\sounds\exit.wav', NORMAL_PLAYBACK)
        root_window.after(850, root_window.destroy())


def gif_frames_updater(widget_using_gif, gif_frames: list, init_frame: int = 0) -> None:
    if init_frame == len(gif_frames):
        init_frame = 0
    frame = gif_frames[init_frame]
    widget_using_gif.configure(image=frame)
    widget_using_gif.after(Variables.frames_delay, gif_frames_updater, widget_using_gif, gif_frames, init_frame + 1)


def refresh_text(text, new_value: str, tags: tuple = None) -> None:
    text.configure(state=tk.NORMAL), text.delete('0.0', tk.END)
    if tags is None:
        text.insert('0.0', new_value)
    else:
        text.insert('0.0', new_value, tags)
    text.configure(state=tk.DISABLED)


########################################################################################################################


# Создание главного окна
root_window = tk.Tk()

# Изображения
icon_image = tk.PhotoImage(file=R'assets\images\icon.png')
lamp_image = tk.PhotoImage(file=R'assets\images\lamp.png')
recent_image = tk.PhotoImage(file=R'assets\images\recent.png')
default_sound_mode_image = tk.PhotoImage(file=R'assets\images\default_mode.png')
silent_sound_mode_image = tk.PhotoImage(file=R'assets\images\silent_mode.png')
solve_button_default_image = tk.PhotoImage(file=R'assets\images\default_button.png')
solve_button_incorrect_image = tk.PhotoImage(file=R'assets\images\incorrect_button.png')
solve_button_correct_image = tk.PhotoImage(file=R'assets\images\correct_button.png')
# Можно использовать не все кадры гифки, изменяя n1, n2 и step; чем меньше
# используется кадров, тем быстрее запуск (n2 <= 29 - всего кадров в гиф)
n1, n2, step = 0, 29, 1
neon_gif_frames = [tk.PhotoImage(file=R'assets\images\neon.gif', format=F'gif -index {f}') for f in range(n1, n2, step)]
curve_line_image = tk.PhotoImage(file=R'assets\images\curve_line.png')
settings_image = tk.PhotoImage(file=R'assets\images\settings.png')
refresh_image = tk.PhotoImage(file=R'assets\images\refresh.png')

# Конфигурация главного окна
root_window.iconphoto(True, icon_image), root_window.title('Equations'), root_window.state('zoomed')
root_window.minsize(840, 700), root_window.configure(background=BLACK)
root_window.protocol('WM_DELETE_WINDOW', on_exit)

# Создание иерархии меню. Создание верхнего меню
menu_bar = tk.Menu(root_window)
root_window.configure(menu=menu_bar)

# Создание вложенного меню
file_menu = tk.Menu(tearoff=0)

# Размещение вложенных меню
menu_bar.add_cascade(label='Файл', menu=file_menu)
file_menu.add_command(label='Настройки...', image=settings_image, compound=tk.LEFT, command=settings)

# Кнопка помощи
guide_button = tk.Button(root_window, **button_options, command=guide, cursor='question_arrow', image=lamp_image)
guide_button.grid(row=0, column=0, padx=3, sticky=tk.NW)

# Кнопка недавних
solved_button = tk.Button(root_window, **button_options, command=solved, cursor='hand2', image=recent_image)
solved_button.grid(row=0, column=2, padx=10, pady=10, sticky=tk.NE)

# Кнопка переключения режимов звука
sound_mode_button = tk.Button(root_window, **button_options, command=switch_sound_mode, cursor='hand2')
sound_mode_button.grid(row=0, column=2, padx=14, pady=10, sticky=tk.SE)
if Variables.sound_mode == 'default':
    sound_mode_button.configure(image=default_sound_mode_image)
elif Variables.sound_mode == 'silent':
    sound_mode_button.configure(image=silent_sound_mode_image)

# Поле ввода уравнения
equation_entry = tk.Entry(root_window, font=('Segoe UI Variable Text Light', 45), width=20, justify=tk.CENTER,
                          background=BLACK, foreground=GREY, borderwidth=1, cursor='xterm',
                          selectforeground=GREY, selectbackground=BLACK, disabledbackground=BLACK,
                          insertbackground=GREY, insertwidth=1)
equation_entry.insert(0, 'Введите уравнение...')
equation_entry.grid(row=1, column=1, sticky=tk.EW)

# Кнопка решения уравнения
solve_button = tk.Button(root_window, **button_options, command=analyze_raw, cursor='hand2',
                         image=solve_button_default_image)
solve_button.grid(row=2, column=1)

# GIF
neon_gif_label = tk.Label(root_window, background=BLACK)
neon_gif_label.grid(row=3, column=1)
gif_frames_updater(neon_gif_label, neon_gif_frames)

# Вывод решения уравнения
solve_text = tk.Text(root_window, width=45, height=4, background=BLACK, foreground=PURPLE,
                     font=('Segoe UI Variable Text Light', 20), relief=tk.SOLID, selectforeground=TURQUOISE,
                     selectbackground=BLACK, wrap=tk.WORD)
solve_text.insert('0.0', 'Здесь будут отображаться решения уравнений')
solve_text.tag_configure('center_alignment', justify=tk.CENTER)
solve_text.tag_add('center_alignment', '0.0', tk.END)
solve_text.grid(row=4, column=1)

# Виджет кривой полосы снизу
curve_line_label = tk.Label(image=curve_line_image, background=BLACK)
curve_line_label.grid(row=5, column=1)

# Позволяем всем использующимся колонкам и строкам распределят доп. место поровну при увеличении
[root_window.columnconfigure(column, weight=1) for column in range(3)]
[root_window.rowconfigure(row, weight=1) for row in range(1, 6)]

# События
equation_entry.bind('<Return>', analyze_raw)
equation_entry.bind('<Button-1>', lambda event: hide_temp_entry_value(equation_entry, 'Введите уравнение...'))
equation_entry.bind('<BackSpace>', lambda event: (show_temp_entry_value(equation_entry, 'Введите уравнение...'),
                                                  refresh_text(solve_text, ''),
                                                  solve_button.configure(image=solve_button_default_image))
                    if equation_entry.get() == '' else ...)

# Начало программы. Прорисовка всех виджетов, реагирование на
# ввод пользователя до тех пор, пока программа не завершится
root_window.mainloop()
