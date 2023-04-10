def strike(text):
    STRIKE_CHARACTER = '\u0336' 
    new_text = ''
    for letter in text:
        new_text = new_text + letter + STRIKE_CHARACTER
    return new_text