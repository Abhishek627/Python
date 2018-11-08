'''

Unnecessary code to check whether a word exists in english dict or not. Can do other fun stuff like checking it's meaning,
synonyms, antonyms and similar words too. But ain't nobody got time for that.

'''
import sys
import subprocess

character_list = [chr(i) for i in xrange(ord('A'),ord('Z')+1)]
# print character_list

#another way of doing the same thing
#import string
# print list(string.ascii_uppercase)

def import_or_install(package):
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        __import__(package)

def check_meaning_exists(word):
    dictionary = PyDictionary.PyDictionary()
    try:
        meaning= dictionary.meaning(word)
        if meaning is None:
            return 0
        else:
            return 1
    except:
        pass

def check_work_exists(word):
    dictionary= enchant.Dict("en_US")
    if dictionary.check(word):
        print word
        # print dictionary.suggest(word)

if __name__ == '__main__':
    # Install these library before running this
    import_or_install('PyDictionary')
    import_or_install('pyenchant')
    for i in character_list:
        temp= i+'OPE'
        check_work_exists(temp)

