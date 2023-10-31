# Валидация полей ввода


# Валидация поля ввода уравнения
def validate_expr(expr: str) -> bool:
    eval_namespace = {'x': 1}  # любое значение x
    try:
        eval(expr, eval_namespace)  # x нужен для проверки корректности
    except (ZeroDivisionError, NameError, SyntaxError, TypeError):
        return False
    return True


__all__ = ['validate_expr']
