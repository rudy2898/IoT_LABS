import cherrypy
import json
import os
import requests
from threading import Thread
import time
import threading

class WebServer(object):
    exposed = True

    def __init__(self):
        self.r = []

    def POST(self, *uri, **params):
        body = cherrypy.request.body.read()
        self.r.append(body)

    def GET(self, *uri, **params):
        return self.r


class IlMioThread (Thread):
   def __init__(self, nome, durata):
       Thread.__init__(self)
       self.nome = nome
       self.durata = durata

   def run(self):
       print ("Thread '" + self.name + "' avviato")
       timestamp=time.time()
       p=requests.GET("192.168.1.52")
       if p!=None:
           x=len(p)
       payload={"temperatura": p[x-1], "tempo":time}
       t=requests.PUT("127.0.0.1/post", data=payload)


if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'request.dispatch': cherrypy.dispatch.MethodDispatcher()
            }
        }
    cherrypy.tree.mount (WebServer(), '/log', conf)
    cherrypy.config.update({'server.socket_host':'192.168.1.52'})
    cherrypy.config.update({'server.socket_port':8080})

    Thread=IlMioThread("GG","infinito")
    x=True
    if threading.current_thread().getName()=="GG":
        while x:
            Thread.run()
            time.sleep(60)
    cherrypy.engine.start()
    cherrypy.engine.block()
    x=False
    Thread.join()
