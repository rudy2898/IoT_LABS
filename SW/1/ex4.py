import json
import cherrypy
import os
import requests

class WebService(object):
    exposed = True
    os.getcwd()
    def GET(self, *uri, **params):
        
        return open('index.html')

    def POST(self, *uri, **params):
        body = cherrypy.request.body.read()
        file = open("./freeboard/dashboard/dashboard.json", 'w')
        file.write(body.decode("utf-8"))

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(), 
            'tools.staticdir.root': os.path.abspath(os.getcwd())
            },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.index':"index.html",
            'tools.staticdir.dir': './freeboard'
            }
        }
    cherrypy.config.update({ 'server.shutdown_timeout': 1 })
    cherrypy.tree.mount (WebService(), '/', conf)
    cherrypy.engine.start()
    cherrypy.engine.block()