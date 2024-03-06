

def count_symbols_in_string():
    """
    Funtion for counting number of symbols between 'f' and 'y'
    """
    print("Enter string:")
    return len([i for i in input() if ord('f') < ord(i) < ord('y')])
