import requests
from bs4 import BeautifulSoup
import json

listOfUrls=[
# "http://ldap1.iitd.ernet.in/LDAP/chemical/ch115.shtml",
"http://ldap1.iitd.ernet.in/LDAP/cse/cs516.shtml",
"http://ldap1.iitd.ernet.in/LDAP/cse/cs116.shtml",
# "http://ldap1.iitd.ernet.in/LDAP/chemical/ch715.shtml",
# "http://ldap1.iitd.ernet.in/LDAP/civil/ce115.shtml",
# "http://ldap1.iitd.ernet.in/LDAP/cse/cs115.shtml",
# "http://ldap1.iitd.ernet.in/LDAP/cse/cs515.shtml",
# "http://ldap1.iitd.ernet.in/LDAP/dbeb/bb115.shtml",
# "http://ldap1.iitd.ernet.in/LDAP/dbeb/bb515.shtml",
# "http://ldap1.iitd.ernet.in/LDAP/ee/ee115.shtml",
# "http://ldap1.iitd.ernet.in/LDAP/ee/ee315.shtml",
# "http://ldap1.iitd.ernet.in/LDAP/maths/mt115.shtml",
# "http://ldap1.iitd.ernet.in/LDAP/maths/mt615.shtml",
# "http://ldap1.iitd.ernet.in/LDAP/mech/me115.shtml",
# "http://ldap1.iitd.ernet.in/LDAP/mech/me215.shtml",
# "http://ldap1.iitd.ernet.in/LDAP/physics/ph115.shtml",
# "http://ldap1.iitd.ernet.in/LDAP/textile/tt115.shtml"
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

