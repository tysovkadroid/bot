def list_join(exe_lst, max_len=0):
    if len(exe_lst) == 1:
        out = exe_lst[0]
    elif len(exe_lst) > 1:
        exe_str = ', '.join(map(str, exe_lst))
        exe_len = len(exe_str) + 1
        if max_len and exe_len > max_len:
            prc_lst = exe_lst
            prc_len = exe_len
            for _ in range(1, exe_len + 1):
                if prc_len > max_len:
                    prc_lst = prc_lst[:-1]
                    prc_str = ', '.join(map(str, prc_lst))
                    prc_len = len(prc_str) + 1
            exc_len = len(exe_lst) - len(prc_lst)
            exc_qnt = exc_len if exc_len > 1 else 2
            exe_str = ', '.join(map(str, exe_lst[:-exc_qnt]))
            out = exe_str + f' и {exc_qnt} других'
        else:
            k = exe_str.rfind(',')
            if k > 0:
                out = exe_str[:k] + ' и' + exe_str[k + 1:]
            else:
                out = exe_str
    else:
        out = exe_lst
    return out
