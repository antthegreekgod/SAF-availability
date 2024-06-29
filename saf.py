#!/usr/bin/env python3

import requests
import datetime
import pdb
import re
from tabulate import tabulate
from termcolor import colored
from getpass import getpass

class SAF:

    def __init__(self, day="today", idDeporte=531):
        self.disp = "https://uab.deporsite.net/ajax/TInnova_v2/ReservaRecursos_Selector_v2_2/llamadaAjax/solicitaDisponibilidad"
        self.today = self.actual_date()
        self.day = day
        if self.day == "tomorrow":
            self.today = str(int(self.today) + 1)
        self.weekday = self.dayOfWeek()
        if not self.weekday:
            idDeporte = 546
        self.url = f"https://uab.deporsite.net/reserva-espais?IdDeporte={idDeporte}"
        self.payload = f"fechaInicio={self.today}%2F06%2F2024&fechaFin={self.today}%2F06%2F2024&IdCentro=3&IdDeporte={idDeporte}&IdTipoRecurso=0&IdModalidad=0&RecursoHumano=0&IdPersona=0&UtilizarIdUsuarioParaObtenerDisponibilidad=0"
        pdb.set_trace()
        self.weekdays = {"7:15":"","8:30":"","9:45":"","11:00":"","12:15":"","13:30":"","14:45":"","16:00":"","17:15":"","18:30":"","19:45":""}
        self.weekends = {"8:00":"","9:30":"","11:00":"","12:30":"","14:00":"","15:30":"","17:00":"","18:30":""}
        self.url_login = "https://uab.deporsite.net/ajax/TInnova_c/Login/llamadaAjax/validaUsuarioPassword"
        self.s = requests.Session()
   # Get Today's Date Number
    @staticmethod
    def actual_date():
        today = str(datetime.date.today())
        return re.split("-", today)[2]
    
    def dayOfWeek(self):
        today = datetime.date.weekday(datetime.date.today())
        if self.day == "today":
            if today >= 5:
                return False
            else:
                return True
        else:
            if today == 4 or today == 5:
                return False
            else:
                return True



    # Regex to Retrieve CSRF Token
    def token(self, first):
        csrf = re.findall('csrf-token" content=.*', first.text)[0]
        csrf = re.findall('content.*', csrf)[0]
        csrf = re.findall('".*?"', csrf)[0]
        csrf = csrf.replace('"',"")
        return csrf

    # set CSRF token headers and laravel cookie
    def setting_session(self):
        first = self.s.get(self.url, verify=False)
        csrf = self.token(first)
        return csrf

    # retrieve availability
    def availability(self):
        csrf = self.setting_session()
        req = self.s.post(self.disp, headers={'X-Csrf-Token': csrf, 'Content-Type':'application/x-www-form-urlencoded'}, data=self.payload, verify=False)
        self.pretty_availability(req)

    # Create table with Current Availability
    def pretty_availability(self, req):
        disponibilidad = re.findall('disponibilidad":"\d[0-9]+', req.text)[0]
        numbers = re.findall('\d[0-9]+', disponibilidad)[0]
        pos = 0
        if self.weekday:
            for num in numbers:
                if num == "0":
                    self.weekdays[list(self.weekdays.keys())[pos]] = colored("Available", "green")
                elif num == "1":
                    self.weekdays[list(self.weekdays.keys())[pos]] = colored("Full", "red")
                else:
                    self.weekdays[list(self.weekdays.keys())[pos]] = colored("Not Available", "yellow")
                pos += 1 
        else:
            for num in numbers:
                if num == "0":
                    self.weekends[list(self.weekdays.keys())[pos]] = colored("Available", "green")
                elif num == "1":
                    self.weekends[list(self.weekdays.keys())[pos]] = colored("Full", "red")
                else:
                    self.weekends[list(self.weekdays.keys())[pos]] = colored("Not Available", "yellow")
                pos += 1 
 
        head = ['Time', 'Availability']
        if self.weekday:
            print(tabulate(self.weekdays.items(), headers=head, tablefmt="grid"))
        else:
            print(tabulate(self.weekends.items(), headers=head, tablefmt="grid"))

    def credentials(self):
        username = input(colored("\n>> Username: ", 'yellow'))
        password = getpass(colored('>> Password: ', 'yellow'))
        return username, password

    # somehow PHPSESSID is not valid
    def login(self):
        username, password = self.credentials()
        csrf = self.setting_session()
        payload = f"_token={csrf}&email={username}&password={password}"
        req = self.s.post(self.url_login, headers={'X-Csrf-Token': csrf, 'Content-Type':'application/x-www-form-urlencoded'}, data=payload)
        with open("response.txt", "w") as f:
            f.write(req.text)


def menu():
    banner = """
    --------------------- WELCOME TO SAF ---------------------

    1) Today's availability
    2) Tomorrow's availability
    3) Exit
    
    ------------------- by @antthegreekgod -------------------
    """
    while True:
        print(banner)
        try:
            return int(input(">> "))
        except:
            print(colored("Please enter a valid number!", "red"))


    
def main():
    while True:
        choice = menu()
        if choice == 1:
            saf = SAF()
            saf.availability()
        elif choice == 2:
            saf = SAF("tomorrow")
            saf.availability()
        elif choice == 3:
            print(colored("\nUntil next time!", "green"))
            break
        else:
            print("Option not implemented")
            break

if __name__ == '__main__':
    main()
