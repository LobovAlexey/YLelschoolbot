import string

symbols = string.ascii_letters + string.digits + string.punctuation


def code(login: str, password: str, number: int) -> tuple[str, ...]:
    k = len(symbols) + number
    c_k = 1
    c_lst = [0, 0]
    for i in login:
        c_lst[0] += symbols.index(i) * c_k
        c_k *= k
    c_k = 1
    for i in password:
        c_lst[1] += symbols.index(i) * c_k
        c_k *= k
    return tuple(map(str, c_lst))


def decode(c_login: int, c_password: int, number: int) -> tuple[str, ...]:
    k = len(symbols) + number
    d_lst = ['', '']
    while c_login:
        d_lst[0] += symbols[c_login % k]
        c_login //= k
    while c_password:
        d_lst[1] += symbols[c_password % k]
        c_password //= k
    return tuple(d_lst)
