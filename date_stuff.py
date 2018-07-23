from datetime import datetime, timedelta

'''
Practice code to create dates between a start and endtime using yield
'''


f = "%d/%m/%Y %H:%M:%S.%f"
start_time= '13/12/2017 00:00:00.1234'
end_time= '13/12/2017 01:00:00.1234'

a= datetime.strptime(start_time,f)
b=datetime.strptime(end_time,f)

# while(a < b):
#     a  = a + timedelta(seconds=1)
#     print a

def perdelta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta


for result in  perdelta(a,b,delta=timedelta(seconds=1)):
    print result