from xml.dom import minidom
import xml.etree.ElementTree as ET
import requests
from requests.auth import HTTPBasicAuth
import time

# TODO: Make the basequery URL more modular to allow for one source that feeds into count and skipvalue queries
# TODO: Save reults as CSV instead of one column .txt file (requires the addition of ""$format=text/csv" to query)
# TODO: Confirm if download URL names change. After the first attempts, URLs saved in file were no longer valid the following day.


#Get count of results
count_url = 'https://s5phub.copernicus.eu/dhus/odata/v1/Products/$count?$filter=substringof(%27L2__NO2%27,Name)%20and%20year(ContentDate/End)%20eq%202020%20and%20month(ContentDate/End)%20le%203&$orderby=ContentDate/End%20desc'
crendentials = ('USERNAME' , 'PASSWORD')# Enter s5pguest crendentials to log into https://s5phub.copernicus.eu/dhus/odata/v1/
s5purl_list = [] # placeholder for URLs
skip_value = 0 # value for which values to start pagination

count_response = requests.get(count_url, auth=crendentials)
count_number = count_response.text
pages_needed = int(count_number)/50
print("Pages needed: "+str(pages_needed))
# quit()
# TODO: add logic to check if results list is 50, else break.
# TODO: change from range to while loop {maybe fixed}
for i in range(pages_needed):
    url = 'https://s5phub.copernicus.eu/dhus/odata/v1/Products?$filter=substringof(%27L2__NO2%27,Name)%20and%20year(ContentDate/End)%20eq%202020%20and%20month(ContentDate/End)%20le%203&$orderby=ContentDate/End%20desc&$skip={}'.format(skip_value)
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
    skip_value += 50 #Go to next 50 results
    time.sleep(1) #Give the Server a break

print(s5purl_list)

print('saving to file')
with open('sp5urlfile.txt', 'w') as filehandle:
    for listitem in s5purl_list:
        filehandle.write('%s\n' % listitem)
print('saved')
quit()
