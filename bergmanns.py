#!bin/python3
import sys
import configparser
import requests
from datetime import datetime, time, timedelta
from bs4 import BeautifulSoup

config = configparser.ConfigParser()
config.sections()
config.read('etc/bergmanns.ini')

username = config['User']['username']
password = config['User']['password']
domain = config['Website']['domain']

data = {'Login_Name': username, 'Login_Passwort': password}
### Tage ###
heute = datetime.combine(datetime.today(), time.min)
morgen = heute + timedelta(days=1)
uemorgen = heute + timedelta(days=2)

heute = int(heute.timestamp())
morgen = int(morgen.timestamp())
umorgen = int(uemorgen.timestamp())

sitemorgen = {'m': '2;1', 'sel_type': 'day', 'sel_date': morgen}

class color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


#####
#####def main(domain, data):
#####    cookie = get.login(domain, data).cookies
#####    parse_morgen = get.get_day(domain, cookie, morgen)
#####    get_namen(site_morgen)
#####
#####
#####if __name__ == "__main__":
#####    main(domain, data)
#####
####### GET ###########

### VARIABLE ###
## Basics ##
#data = {'Login_Name': username, 'Login_Passwort': password}
#lin_param = {'ear_a': 'akt_login'}
#lout_param = {'ear_a': 'akt_login','a': 'login/logout'}
## Menu ##
## Übersicht #
#bestellung_alle = {'m': '2;1'}
#bestellung_tag = {'m': '2;1', 'sel_type': 'day', 'sel_date': date}
#bestellung_woche = {'m': '2;1', 'sel_type': 'week', 'sel_date': date}
## Speiseplan #
#wochenplan = {'m': '2;0'}

### Tage ###
heute = datetime.combine(datetime.today(), time.min)
morgen = heute + timedelta(days=1)
uemorgen = heute + timedelta(days=2)

heute_int = int(heute.timestamp())
morgen_int = int(morgen.timestamp())
umorgen_int = int(uemorgen.timestamp())
### Funktionen ###

#login to the website
def login(domain, data):
    lin_param = {'ear_a': 'akt_login'}
    login = requests.post(domain, data=data, params=lin_param)
    return login

#logout from the website
def logout(cookie):
    lout_param = {'ear_a': 'akt_login','a': 'login/logout'}
    logout = requests.get(domain, params=lout_param, cookies=cookie)
    return logout

#Menü aufrufen
def get_uri(domain, cookie, param):
    response = requests.get(domain, cookies=cookie, params=param)
    return response

#Bestellung an Datum abfragen
def get_day(domain, cookie, datum):
    datum = {'m': '2;1', 'sel_type': 'day', 'sel_date': datum}
    response = get_uri(domain, cookie, datum)
    return response


###### Parse ######

#site = b.get_day(mb, b.umorgen).text
#bs = BeautifulSoup(site)
#
#bestellung = bs('table', attrs={'class':'auflistung bestellungen'})
#bestellung_head = bs('tr', attrs={'class':'head'})
#bestellung_artikel = bestellung.findAll('tr', attrs={'class':'auflistung0'})
#
#bestellung_nummer = bestellung.findAll('td',attrs={'class':'bestellungen_menuart'})
#bestellung_text = bestellung.findAll('td',attrs={'class':'bestellungen_menu'})

def get_nummern(site):
    site = site.text
    bs = BeautifulSoup(site, "lxml")
    bestellung_nummer = bs.findAll('td',attrs={'class':'bestellungen_menuart'})
    for i in bestellung_nummer:
        nummern = print(''.join(i))
    return nummern

def get_namen(site):
    site = site.text
    bs = BeautifulSoup(site, "lxml")
    bestellung_text = bs.findAll('td',attrs={'class':'bestellungen_menu'})
    text = []
    for i in bestellung_text:
        text.extend(i)
    return text

if __name__ == "__main__":
    print(color.HEADER,'Moment ich sehe kurz für dich nach',color.ENDC)
    heute = datetime.combine(datetime.today(), time.min)
    morgen = heute + timedelta(days=1)
    login = login(domain, data)
    if login.status_code != 200:
        print(color.FAIL+'HTTP STATUSCODE == '+login.status_code+color.ENDC)
        sys.exit()
    cookie = login.cookies
    liste = [heute, morgen]
    for i in liste:
        intday = int(i.timestamp())
        parsed = get_day(domain, cookie, intday)
        if parsed.status_code == 200:
            print('Du hast am '+color.BOLD,i,color.ENDC+' folgendes bestellt')
            essen = get_namen(parsed)
            if not essen:
                print(color.WARNING+'Du hast noch nicht bestellt'+color.ENDC)
            else:
                print(color.OKBLUE+'\n'.join(essen)+color.ENDC)
        else:
            print(color.FAIL+'Fehler beim Verbindungsaufbau'+color.ENDC)
    logout(cookie)

