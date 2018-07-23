from xml.etree import ElementTree as ET

'''
Sample XML parsing using ET
'''


tree = ET.parse('Matching_Result.xml')
root = tree.getroot()
for mot in root.findall('mot'):
     name = mot.get('id')
     rank = mot.find('val').text
     print name , rank
     if name == 'abc':
         val= mot.find('val')
         val.text = 'new_val'
tree.write('Matching_Result.xml')
