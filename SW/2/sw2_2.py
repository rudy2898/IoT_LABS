import requests

if __name__ == "__main__":
    code = input(
        """Inserire il codice corrispondente all'operazione desiderata:\n
        1->Stampa il message broker\n
        2->Lista utenti\n
        3->Lista dispostivi\n
        4->Lista servizi\n
        5->Cerca utente\n
        6->Cerca dispositivo\n
        7->Cerca servizio\n""")
    if code=="1":
        r1 = requests.get("http://localhost:8080/ip")
        print(r1)
    elif code=="2":
        r2 = requests.get("http://localhost:8080/users/list")
        print(r2)
    elif code=="3":
        r3 = requests.get("http://localhost:8080/devices/list")
        print(r3)
    elif code=="4":
        r4 = requests.get("http://localhost:8080/services/list/")
        print(r4)
    elif code=="5":
        r5 = requests.get("http://localhost:8080/users/search/User1")
        print(r5)
    elif code=="6":
        r6 = requests.get("http://localhost:8080/devices/search/Device1")
        print(r6)
    elif code=="7":
        r7 = requests.get("http://localhost:8080/services/search/Service1")
        print(r7)