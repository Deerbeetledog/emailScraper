import random 
import string
from googlesearch import search
import requests
import re
from bs4 import BeautifulSoup
import smtplib

#eliminate duplicates from a list
def singles(object):
    return list(dict.fromkeys(object))

query = ""

for i in range(random.randint(2, 4)):
    query += random.choice(string.ascii_letters + string.digits)

#uncomment for testing
#query = 'contact info'

print(f"search query: {query}")

sites = []
for site in search(query=query, tld='com', num=30, stop=30, pause=2):
   sites.append(site)

emailFile = open("emails.txt", "w")
for url in sites:
    try:
        print(f"searching {url}")
        site = requests.get(url, timeout=7)
        site = site.text
        soup = BeautifulSoup(site, 'html.parser')
        for p in soup.findAll("p"):
            p = str(p)
            print(f"looking through {p}")

            email = None

            email = re.findall(r'[A-Za-z0-9\-.]+@[a-zA-Z\-.]+\.[a-zA-Z]+', p)
            
            if email != []:
                print(f"\n\n{email}\n\n")
                for i in email:
                    emailFile.write(i + "\n")
    except:
        continue

#gets all the emails into a list and eliminates duplicates
emailFile.close()
emailFile = open("emails.txt", "r")

emails = singles(emailFile.readlines())
emailFile.close()

"""
lets uhh try to not send spam to government agencies now, shall we?
basically, fliters out any emails that have 'gov' or 'edu' in them
(also strips the emails of newlines)
"""
emailsRemoved = 0
filteredEmails = []
for email in emails:
    if "gov" in email or "edu" in email:
        emailsRemoved += 1
    else:
        filteredEmails.append(email.rstrip())

emails = filteredEmails
del filteredEmails #get delterated B

print(f"\n\nfound {len(emails)} emails:\n")
for email in emails:
    print(email)

print(f"\n{emailsRemoved} emails were removed.")

#puts the new emails back into the file
emailFile = open("emails.txt", "w")
for email in emails:
    emailFile.write(f"{email}\n")
emailFile.close()

if input("send emails? y/n ").lower() != "y":
    quit()

print("sending...")

emailInfoFile = open("info.txt", "r")
emailInfo = emailInfoFile.readlines()
emailInfoFile.close()

user = emailInfo[0].strip()
password = emailInfo[1].strip()

prov = smtplib.SMTP("smtp-mail.outlook.com", 587)

prov.starttls()

prov.login(user, password)

for email in emails:
    message = f"""From: {user}\r\nTo: {email}\r\nSubject: {emailInfo[2].strip()}\r\n

    """

    for i, content in enumerate(emailInfo):
        if i < 3:
            pass
        else:
            message += content
    prov.sendmail(user, email, message)

prov.quit()