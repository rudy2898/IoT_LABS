import cherrypy
import json
from sw3_4 import *

if __name__=='__main__':
	conf = {
		'/': {
			'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
			'tool.session.on': True
		}
	}
	cherrypy.tree.mount(RemoteController(), '/controller', conf)
	cherrypy.engine.start()
	cherrypy.engine.block()