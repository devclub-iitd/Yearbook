import requests
from bs4 import BeautifulSoup
import json
import logging

logger = logging.getLogger(__name__)

listOfUrls=[
"http://ldap1.iitd.ernet.in/LDAP/chemical/ch116.shtml",
"http://ldap1.iitd.ernet.in/LDAP/chemical/ch716.shtml",
"http://ldap1.iitd.ernet.in/LDAP/civil/ce116.shtml",
"http://ldap1.iitd.ernet.in/LDAP/cse/cs116.shtml",
"http://ldap1.iitd.ernet.in/LDAP/cse/cs516.shtml",
"http://ldap1.iitd.ernet.in/LDAP/dbeb/bb116.shtml",
"http://ldap1.iitd.ernet.in/LDAP/dbeb/bb516.shtml",
"http://ldap1.iitd.ernet.in/LDAP/ee/ee116.shtml",
"http://ldap1.iitd.ernet.in/LDAP/ee/ee316.shtml",
"http://ldap1.iitd.ernet.in/LDAP/maths/mt116.shtml",
"http://ldap1.iitd.ernet.in/LDAP/maths/mt616.shtml",
"http://ldap1.iitd.ernet.in/LDAP/mech/me116.shtml",
"http://ldap1.iitd.ernet.in/LDAP/mech/me216.shtml",
"http://ldap1.iitd.ernet.in/LDAP/physics/ph116.shtml",
"http://ldap1.iitd.ernet.in/LDAP/textile/tt116.shtml"
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


with open('fileName.csv', 'w') as f:
    for line in totalDic:
        f.write(";".join(line)+"\n");

