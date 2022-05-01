import requests
from bs4 import BeautifulSoup
import json
import logging

logger = logging.getLogger(__name__)

listOfUrls=[
"http://ldap1.iitd.ernet.in/LDAP/chemical/ch118.shtml",
"http://ldap1.iitd.ernet.in/LDAP/chemical/ch718.shtml",
"http://ldap1.iitd.ernet.in/LDAP/civil/ce118.shtml",
"http://ldap1.iitd.ernet.in/LDAP/cse/cs118.shtml",
"http://ldap1.iitd.ernet.in/LDAP/cse/cs518.shtml",
"http://ldap1.iitd.ernet.in/LDAP/dbeb/bb118.shtml",
"http://ldap1.iitd.ernet.in/LDAP/dbeb/bb518.shtml",
"http://ldap1.iitd.ernet.in/LDAP/ee/ee118.shtml",
"http://ldap1.iitd.ernet.in/LDAP/ee/ee318.shtml",
"http://ldap1.iitd.ernet.in/LDAP/maths/mt118.shtml",
"http://ldap1.iitd.ernet.in/LDAP/maths/mt618.shtml",
"http://ldap1.iitd.ernet.in/LDAP/mech/me118.shtml",
"http://ldap1.iitd.ernet.in/LDAP/mech/me218.shtml",
"http://ldap1.iitd.ernet.in/LDAP/physics/ph118.shtml",
"http://ldap1.iitd.ernet.in/LDAP/textile/tt118.shtml"
]

def kerberos_to_entry_number(kerberos):
	return "20" + kerberos[3:5] + kerberos[:3].upper() + kerberos[5:]

code2dept = {
	"ce":"civil",
	"ch":"chemical",
	"cs":"cse",
	"bb":"dbeb",
	"ee":"ee",
	"mt":"maths",
	"me":"mech",
	"ph":"physics",
	"tt":"textile"
}

totalDic=[]
Dept = ""
ind=0

for url in listOfUrls:
	response = requests.get(url)
	html = response.content
	soup = BeautifulSoup(html, "html.parser")

	table_body = soup.find('table')

	rows = table_body.find_all('tr')
	logger.info(url)
		
	for row in rows:
		cols = row.find_all('td')
		if(len(cols) > 1):
			cols = [ele.text.strip() for ele in cols]
			cols.append(Dept)
			totalDic.append([ele for ele in cols if ele]) # Get rid of empty values
			totalDic[ind][0] = kerberos_to_entry_number(totalDic[ind][0])
			ind = ind+1
		else:
			cols = [ele.text.strip() for ele in cols]
			Dept = code2dept[str(cols[0][0:2])]

with open('./Scrape/fileName.csv', 'w') as f:
    for line in totalDic:
        f.write(";".join(line)+"\n")

