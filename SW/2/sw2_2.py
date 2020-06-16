import requests

if __name__ == "__main__":
    code = input("Inserire il codice corrispondente all'operazione desiderata:\n1->Stampa il message broker\n2->Lista utenti\n3->Lista dispostivi\n4->Cerca utente\n5->Cerca dispositivo\n")
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
        r4 = requests.get("http://localhost:8080/users/search/User1")
        print(r4)
    elif code=="5":
        r5 = requests.get("http://localhost:8080/devices/search/Device1")
        print(r5)