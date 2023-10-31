# Решение уравнения


# Преобразование сырой строки в выражение
def raw_to_expr(raw: str) -> str:
    # Первоначальные преобразования (согласно требованиям ввода для юзера)
    raw = raw.replace(' ', '').replace(',', '.').replace('^', '**')
    # Убрать приравнивание к 0 (если есть)
    eqs_indx = raw.find('=')
    expr = raw[:eqs_indx] if eqs_indx != -1 else raw
    return expr


# Нахождение корней по корректному выражению
def find_roots(valid_expr: str, *, from_x: int = -100, to_x: int = 100, eps: float = 1e-10) -> tuple[int | float, ...]:
    # Чем меньше эпсилон, тем точнее нецелый корень (но в зависимости от уравнения
    # возможно вычислить такой корень только до определенного эпсилона)
    roots = ()  # корни всегда в порядке возрастания
    eval_namespace = {'x': ...}
    x = from_x

    # Поиск корней
    while x <= to_x:
        eval_namespace['x'] = x
        y1 = eval(valid_expr, eval_namespace)
        if y1 == 0:
            roots += (x,)  # целый корень сразу в ответ
        x += 1
        eval_namespace['x'] = x
        y2 = eval(valid_expr, eval_namespace)
        if y1 * y2 < 0:
            # Поиск нецелого корня (с точностью до текущего эпсилона)
            (a, b) = x - 1, x
            while b - a > eps:
                eval_namespace['x'] = a
                y1 = eval(valid_expr, eval_namespace)
                c = (a + b) / 2
                eval_namespace['x'] = c
                y3 = eval(valid_expr, eval_namespace)
                if y1 * y3 < 0:
                    b = c
                else:
                    a = c
            # Добавление нецелого корня в ответ
            roots += ((a + b) / 2,)

    return roots


# Вывод корней
def roots_output(roots: tuple, *, prec: int = 5) -> str:
    # Если нет корней
    if len(roots) == 0:
        return 'Уравнение не имеет действительных корней'

    # Если есть хотя бы один корень

    subscripts = list('₀₁₂₃₄₅₆₇₈₉')  # набор подстрочных индексов
    # Два отображения корней
    view1 = ''
    view2 = 'x ∈ {'

    for [root_num, root] in enumerate(roots, 1):

        # Формирование подстрочного индекса
        subscript = ''
        while root_num:
            subscript = subscripts[root_num % 10] + subscript
            root_num //= 10

        # Формирование знака почти равный / равный
        eqs = '≈' if isinstance(root, float) else '='

        # Формирование корня
        root = str(round(root, prec)).replace('.', ',')  # целый корень не изменится

        # Наполнение отображения корней по отдельности
        view1 += F'x{subscript} {eqs} {root}\n'
        # Наполнение множества из этих корней
        view2 += F'{root}; '

    # Убрать лишний перенос строки
    view1 = view1[:-1]
    # Убрать лишние ';' и ' ', закрыть скобку множества
    view2 = view2[:-2] + '}'

    # Префикс
    prefix = 'Корень уравнения:' if len(roots) == 1 else 'Корни уравнения:'

    # Конечный вывод
    output = prefix + '\n' + view1 + '\n\n' + view2

    return output


if __name__ == '__main__':
    print(roots_output(find_roots(raw_to_expr('3 ^ 8 * x ^ 3 + 2 * x ^ 2 + 12.5'))))

__all__ = ['raw_to_expr', 'find_roots', 'roots_output']
