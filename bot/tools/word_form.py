import pymorphy2


def word_form(word=None, gender=None, integer=None):
    if word:
        morph = pymorphy2.MorphAnalyzer().parse(word)[0]
        if gender:
            word = morph.inflect({f"{'masc' if gender == 'm' else 'femn'}"}).word
        elif integer:
            word = f'{integer} {morph.make_agree_with_number(integer).word}'
    return word
