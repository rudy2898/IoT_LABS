import cherrypy
import json
import time
from sw2_1_nonweb import *


# classe device con attributi corrispondenti
class dev:
	exposed=True
	def __init__(self):
		
		self.disp=[]

	def GET(self, *uri, **params):
		if uri[0]=="list":
			return funzioni_varie.get(self.disp,"Device")
		elif uri[0]=="search" and len(uri) > 1:
			return funzioni_varie.search(self.disp,uri[1],"Devices")
		else:
			return {"Risultato" : "Invalid_command"}

	def PUT(self, *uri, **params):
		body = cherrypy.request.body.read()
		json_body = json.loads(body.decode('utf-8'))
		if uri[0] == "devices":
			t=funzioni_varie.add(self.disp, json_body,"Devices")
			if t==None:
				return {"Risultato": "Errore"}
			else:
				return {"Risultato": "Ok"}
		else:
			return {"Risultato": "No_dati"}


# classe users con attributi corrispondenti
class us:
	exposed=True
	def __init__(self):
		self.us=[]

	def GET(self, *uri, **params):
		if uri[0]=="list":
			return funzioni_varie.get(self.us,"Users")
		elif uri[0]=="search" and len(uri) > 1:
			return funzioni_varie.search(self.us,uri[1],"Users")
		else:
			return {"Risultato": "Invalid_command" }

	def PUT (self, *uri, **params):
		body = cherrypy.request.body.read()
		json_body = json.loads(body.decode('utf-8'))
		if uri[0] == "users":
			t=funzioni_varie.add(self.us, json_body,"Users")
			if t==None:
				return {"Risultato": "Errore"}
			else:
				return {"Risultato": "Ok"}
		else:
			return {"Risultato": "No_dati"}

# classe services con attributi corrispondenti
class ser:
	exposed=True
	def __init__(self):
		self.serv=[]

	def GET(self, *uri, **params):
			if uri[0]=="list":
				return funzioni_varie.get(self.serv,"Services")
			elif uri[0]=="search" and len(uri) > 1:
				return funzioni_varie.search(self.serv,uri[1],"Services")
			else:
				return {"Risultato": "Invalid_command" }

	def PUT (self, *uri, **params):
		body = cherrypy.request.body.read()
		json_body = json.loads(body.decode('utf-8'))
		if uri[0] == "services":
			t=funzioni_varie.add(self.serv, json_body,"Servizi")
			if t==None:
				return {"Risultato": "Errore"}
			else:
				return {"Risultato": "Ok"}
		else:
			return {"Risultato": "No_dati"}

class br:
	exposed=True
	
	def __init__(self):
		self.broker = "test.mosquitto.org"
		self.port = 1883

	

	def GET(self, *uri, **params):
		if uri[0]=="ip":
			d = {"Ip": self.broker, "port":self.port}
			return json.dumps(d)
		else:
			return {"Risultato": "Invalid_command" }




	
	

	

	
	

	


	#file json atteso del tipo
	# {"Servizi: "ID", "descrizione": "", "end_points": [""]}

	# metodo per l'aggiunta di un nuovo servizio. Controllo sull'aggiunta di un servizio dublicato
	# e corrispondente aggiornamento del timestamp
	

	#file json atteso del tipo
	# {"Dispositici: "ID", "risorse": [""], "end_points":[""]}

	

	#file json atteso del tipo
	# {"Utenti: "ID", "nome":"", "cognome":"", "email":""}

	# metodo per l'aggiunta di un nuovo utente. 
	

	# meto che ritorna un dizionario composto da {"Services": ["lista di servizi con il proprio serviceID"]}
	


	


	
	


	