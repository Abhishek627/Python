import bs4, requests, re, time
from tabulate import tabulate
res=requests.get('http://www.mohfw.gov.in/')
ressoup=bs4.BeautifulSoup(res.text, 'lxml')
listres=ressoup.select('.bg-blue strong')
listres1=ressoup.select('.bg-green strong')
listres2=ressoup.select('.bg-red strong')
listres3=ressoup.select('.bg-orange strong')
regex=re.compile(r'\d+\s\w+\s\d+\S\s\d+\S\d+')
timestamp=regex.findall(str(ressoup))

print('COVID19 Cases in INDIA Highlights')
print('*********************************', end='')
print('\n')
print('Total Confirmed Cases: ' + str(int(listres[0].getText())+int(listres1[0].getText())+int(listres2[0].getText())))
print('Active COVID19 Cases: ' + listres[0].getText())
print('Cured/Discharged Cases: ' + listres1[0].getText())
print('Death Cases: ' + listres2[0].getText())
print('Migrated COVID19 Cases: ' + listres3[0].getText(), end='')
print('\n')
print('COVID19 Cases Statistic State-wise')
print('**********************************', end='')
print('\n')

all=ressoup.select('.table.table-striped tbody')
nameregex=re.compile(r'<td>.*</td>')
final=nameregex.findall(str(all[0]))
headers=['S.No.', 'Name of State/UT', 'Total Conf. Cases', 'Cured/Discharged/Migrated', 'Death']
body=[]
lis=['1']
i=1
while  i<165:
    finalsoup=bs4.BeautifulSoup(final[i], 'lxml')
    if i%5!=0:
        lis.append(finalsoup.getText())
    else:
        body.append(tuple(lis))
        lis=[]
        lis.append(finalsoup.getText())
    i=i+1

print(tabulate(body, headers=headers), end='')
print('\n')
print('Source: MOHFW')
print('Last Updated: ', end='')
print(timestamp[0])
print('\n')
#input('Press ENTER to Exit ')
