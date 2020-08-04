import json
import cherrypy
import pytemp
import array

keys={"K","C","F"}

def check_uri(uri):
    if len(uri)==4:
    	if uri[0]=='converter' or str.isdigit(uri[1] or uri[2] in keys or uri[3] in keys):
       		check_temp(uri[1], uri[2], uri[3])
        	return True
    return False

def check_temp(temp, unit1, unit2):
    if unit1 == unit2:
        return False
    else:
        return True

def convert(uri):
    return pytemp.pytemp(float(uri[1]), uri[2], uri[3])

class MyWebServices(object):

	exposed=True

	def GET(self,*uri):
		if uri != '':
			ind = ' '.join(uri)
			ind = ind.split(' ')
			if check_uri(ind):
				ind.append(convert(ind))
				i=1
				diz = {
                                        'value':'',
                                        'originalUnit':'',
                                        'targetUnit':'',
                                        'valueConvert':''
                                        }
				for key in diz.keys():
					diz[key] = ind[i]
					i+=1
				return json.dumps(diz)
                        else:
				return "Valori passati non corretti"
		else:
			return "Nessuna richiesta"
