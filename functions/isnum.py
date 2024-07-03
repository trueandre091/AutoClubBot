def isnum(string):
    try:
        int(string)
    except ValueError:
        return False
    return True
