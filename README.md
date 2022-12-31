Introducing the emailScraper!

Essencially does a random google search, and scans the top 30 results for email adresses, deposits them into a file, and then optionally sends an email to them through an outlook account.

Also filters out any emails it finds that contain the phrases 'gov' or 'edu'.

To be able to batch send emails, editing info.txt is required, alongside an outlook account. When configured, info.txt should look like this:
```
username for outlook account
password
email subject
email contents (can span multiple lines)
```

be sure to use
```
pip install -r requirements.txt
```
to install all the requirements for the script to work
