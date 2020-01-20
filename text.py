def texttobasic(text):
    basic = ""
    down = ord('a')
    top = ord('z')
    for char in text.lower():
        code = ord(char)
        if code >= down and code <= top:
            basic += char
    return basic

def searchtext(text, elements):
    basic = texttobasic(text)
    text = ""

    encontrado = False
    i = 0

    while not encontrado and i < len(elements):
        if basic == texttobasic(elements[i]):
            text = elements[i]
            encontrado = True
        i += 1

    return text