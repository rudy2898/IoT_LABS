import cherrypy
import json
import time


# classe device con attributi corrispondenti
class devices(object):
	def __init__(self, uniqueID, end_points, resources):
		self.uniqueID= uniqueID
		self.end_points= end_points
		self.resources= resources
		self.timestamp_d=time.time()

# classe users con attributi corrispondenti
class users(object):
	def __init__(self):
		self.UserId=""
		self.name=""
		self.surname=""
		self.email=""

# classe services con attributi corrispondenti
class services(object):
	def __init__(self, serviceID, description, end_points):
		self.serviceID= serviceID
		self.description= description
		self.end_points= end_points
		self.timestamp_s = time.time()


class Catalog(object):
	exposed=True

	#si creano delle liste contenti oggetti device, users e services
	def __init__(self):
		self.dev = devices
		self.users = users
		self.ser = services
		self.broker = "mqtt.eclipse.org"
		self.port = 8080

	# metodo utilizzato per l'aggiornamento del timestamp per l'esercizio 5
	def updateTimestamp(self, num):
		self.dev[num].timestamp = time.time()

	# metodo che ritorna la lista dei device, richiamato all'interno dell'esercizio 5
	def getDev_list(self):
		return self.dev

	# metodo per la ricerca di un servizio
	def searchServices(self, id):
		servizio = [s for s in self.ser if id == s.serviceID]
		data = {"Services": servizio}
		return data

	# metodo per la ricerca di un device
	def searchDevices(self, id):
		dispositivo = [s for s in self.ser if id == s.uniqueID]
		data = {"Dispositivo": dispositivo}
		return data

	# metodo per la ricerca di un user
	def searchUsers(self, id):
		utente = [s for s in self.user if id == s.UserId]
		data = {"Users": utente}
		return data

	#file json atteso del tipo
	# {"Servizi: "ID", "descrizione": "", "end_points": [""]}

	# meto per l'aggiunta di un nuovo servizio. Controllo sull'aggiunta di un servizio dublicato
	# e corrispondente aggiornamento del timestamp
	def addServices(self, body):
		for s in self.ser:
			if s.serviceID == body['Servizi']:
				s.timestamp_s = time.time()
				return
		servizio = services(body['Servizi'], body['descrizione'], body['end_points'])
		ser.append(servizio)

	#file json atteso del tipo
	# {"Dispositici: "ID", "risorse": [""], "end_points":[""]}

	# meto per l'aggiunta di un nuovo dispositico. Controllo sull'aggiunta di un dispositivo dublicato
	# e corrispondente aggiornamento del timestamp
	def addDevices(self, body):
		for s in self.ser:
			if s.uniqueID == body['Dispositivi']:
				s.timestamp_d = time.time()
				return
		dispositivi = devices(body['Dispositivi'], body['risorse'], body['end_points'])
		self.dev.append(dispositivi)

	#file json atteso del tipo
	# {"Utenti: "ID", "nome":"", "cognome":"", "email":""}

	# meto per l'aggiunta di un nuovo utente. 
	def addUsers(self, body):
		utenti = users(body['Utenti'], body['nome'], body['cognome'], body['email'])
		self.users.append(utenti)

	# meto che ritorna un dizionario composto da {"Services": ["lista di servizi con il proprio serviceID"]}
	def getServices(self):
		data = {"Services": []}
		n = 0
		for i in self.ser:
			data['Services'] = i.serviceID
			n += 1
		return data


	# meto che ritorna un dizionario composto da {"Users": ["lista di utenti con il proprio userID"]}
	def getUsers(self):
		data = {}
		data["Users"]=[]
		n = 0
		for i in self.users:
			data['Users'][n] = i.UserId
			n += 1
		return data


	# meto che ritorna un dizionario composto da {"SDevices": ["lista di dispositivi con il proprio uniqueID"]}
	def getDevices(self):
		data = {"Devices": []}
		n = 0
		for i in self.dev:
			data['Devices'][n] = i.uniqueID
			n += 1
		return data

	# metodo che ritorna il broker e l'indirizzo ip
	def getIp(self):
		data = {"Ip": self.broker, "Porta": self.port}
		return data

	#tutto come uri
	def GET(self, *uri, **params):
		if uri[0]=="services":
			if uri[1]=="list":
				return self.getServices()
			elif uri[1]=="search":
				return self.searchServices(uri[2])
			else:
				return "Comando non valido"
		elif uri[0]=="users":
			if uri[1]=="list":
				return self.getUsers()
			elif uri[1]=="search":
				return self.searchUsers(uri[2])
			else:
				return "Comando non valido"
		elif uri[0]=="devices":
			if uri[1]=="list":
				return self.getDevices()
			elif uri[1]=="search":
				return self.searchDevices(uri[2])
			else:
				return "Comando non valido"
		elif uri[0]=="ip":
			return self.getIp()
		else:
			return "Comando no supportato, riprova"
		


	def PUT (self, *uri, **params):
		body = cherrypy.request.body.read()
		json_body = json.loads(body.decode('utf-8'))
		if uri[0] == "services":
			return self.addServices(json_body)
		elif uri[0] == "users":
			self.addUsers(json_body)
		elif uri[0] == "devices":
			self.addDevices(json_body)
		else:
			return "Nessun campo nel body della funzione PUT"



if __name__=='__main__':
	conf = {
		'/': {
			'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
			'tool.session.on': True
		}
	}
	cherrypy.tree.mount(Catalog(), '/', conf)
	cherrypy.engine.start()
	cherrypy.engine.block()
