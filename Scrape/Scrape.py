import requests
from bs4 import BeautifulSoup
import json

listOfUrls=[
"http://ldap1.iitd.ernet.in/LDAP/chemical/ch114.shtml",
"http://ldap1.iitd.ernet.in/LDAP/chemical/ch714.shtml",
"http://ldap1.iitd.ernet.in/LDAP/civil/ce114.shtml",
"http://ldap1.iitd.ernet.in/LDAP/cse/cs114.shtml",
"http://ldap1.iitd.ernet.in/LDAP/cse/cs514.shtml",
"http://ldap1.iitd.ernet.in/LDAP/dbeb/bb114.shtml",
"http://ldap1.iitd.ernet.in/LDAP/dbeb/bb514.shtml",
"http://ldap1.iitd.ernet.in/LDAP/ee/ee114.shtml",
"http://ldap1.iitd.ernet.in/LDAP/ee/ee314.shtml",
"http://ldap1.iitd.ernet.in/LDAP/maths/mt114.shtml",
"http://ldap1.iitd.ernet.in/LDAP/maths/mt614.shtml",
"http://ldap1.iitd.ernet.in/LDAP/mech/me114.shtml",
"http://ldap1.iitd.ernet.in/LDAP/mech/me214.shtml",
"http://ldap1.iitd.ernet.in/LDAP/physics/ph114.shtml",
"http://ldap1.iitd.ernet.in/LDAP/textile/tt114.shtml"
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
	print(url)
		
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

