def string_escape(string, chars):
    for char in chars:
        if char in string:
            string = string.replace(char, '\\' + char)
    return string
