'''

Practice code for singelton methods in python

'''

def singelton(klass):
    instances={}
    def getInstance():
        if klass not in instances:
            instances[klass]=klass()
        return instances[klass]
    return getInstance


@singelton
class return_val():
    def __init__(self):
        pass

    def print_value(self):
        print "HELLO TEST 123"


print type(return_val)
print return_val() is return_val()















