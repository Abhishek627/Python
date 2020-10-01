def parseInt(st):
    if (isinstance(st, str)):
        return int(input(st))
    else:
        print('Expected <class \'str\', ' + str(type(st)) + ' passed.')
