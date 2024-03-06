
TEXT = "So she was considering in her own mind, as well as she could, for the hot day made her feel very sleepy and stupid,\
whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the\
daisies, when suddenly a White Rabbit with pink eyes ran close by her"


def count_parameters_of_text():
    """
    Funtion counts some parameters of the text
    """
    text = TEXT.lower()
    number_words = text.count(' ') - 1
    
    set_letters = set(text)
    set_letters.discard(".")
    set_letters.discard(",")
    set_letters.discard(" ")
    set_letters.discard("-")
    gen = (i for i in set_letters)
    dct_res = dict()
    for i in gen:
        dct_res[i] = text.count(i)
    
    lst_res = text.split(',')
    lst_res.pop(0)
    lst_res.pop()
    lst_res.sort()

    return number_words, dct_res, lst_res