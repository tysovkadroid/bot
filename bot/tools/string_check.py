def string_check(string, chars):
    if any([string.count(x) % 2 for x in chars]):
        return False
    return True
