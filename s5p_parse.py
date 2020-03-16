from xml.dom import minidom
import xml.etree.ElementTree as ET
import requests
from requests.auth import HTTPBasicAuth
import time


url = 'https://s5phub.copernicus.eu/dhus/odata/v1/Products?$filter=substringof(%27S5P%27,Name)&$skip=50' # TODO: Add order by and NO2 clause
crendentials = ('USERNAME' , 'PASSWORD')# Enter crendentials to log into https://s5phub.copernicus.eu/dhus/odata/v1/
s5purl_list = [] # placeholder for URLs
skip_value = 50 # value for which values to start pagination

# TODO: add logic to check if results list is 50, else break.
# TODO: change from range to while loop
for i in range(2):
    url = 'https://s5phub.copernicus.eu/dhus/odata/v1/Products?$filter=substringof(%27S5P%27,Name)&$skip={}'.format(skip_value)
    skip_value += 50
    print(url)
    r = requests.get(url, auth=crendentials)
    res = ET.fromstring(r.content)
    print(res)
    mydoc = minidom.parseString(r.content)
    items = mydoc.getElementsByTagName('entry')
    print(len(items))
    for elem in items:
        s5purl = elem.getElementsByTagName('id')[0].firstChild.nodeValue+"/$value"
        s5purl_list.append(s5purl)

    time.sleep(0.5) #Give the Server a break

print(s5purl_list)

print('saving to file')
with open('sp5urlfile.txt', 'w') as filehandle:
    for listitem in s5purl_list:
        filehandle.write('%s\n' % listitem)
print('saved')
quit()
