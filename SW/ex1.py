import json
import cherrypy
import pytemp
import array

keys={"K","C","F"}
""" possibili unita di misura disponibili per la conversione """

def checkUri(uri):
    """Controllo se il path corrisponde al nome del servizio

    :uri: array
    :return: True se corretto, False altrimenti

    """
    if uri[0]=="" or uri[0]!="converter":
        return False
    else:
        return True

def checkParams(params):
    """controllo errore sui parametri passati

    :params: dictonary
    :returns: True se corretto, False altrimenti

    """
    chiavi=list(params.keys())
    valori=params.values()
    """ controllo chiavi """
    if len(chiavi)!=3:
        return False
    if chiavi[0]!="value" or chiavi[1]!="originalUnit" or chiavi[2]!="targetUnit":
        return False
    if chiavi[1] == chiavi[2]:
        return False
    else:
        return True
    """ controllo valori """
    if len(valori)!=3:
        return False
    if not str.isdigit(valori[0]) or not keys.intersection(valori[1]) or not keys.intersection(valori[2]):
        return False # se il primo valore non e' un numero e i caratteri non sono validi
    else:
        return True

class MyWebServices(object):

    exposed=True

    def GET(self,*uri,**params):
        if checkUri(uri) == False:
            raise cherrypy.HTTPError(404)
        if checkParams(params) == False:
            raise cherrypy.HTTPError(400)
        final_value = trasforma_valori(params.values())
        diz = {
                "originalValue":params.get("value"),
                "originalUnit":params.get("originalUnit"),
                "convertedValue":final_value,
                "targetUnit":params.get("targetUnit")
                }
        return json.dumps(diz)
#        r="".join(uri)
#        if uri!="":
#            if r=="converter":
#                if params!="":
#                    k=params.keys()
#                    v=params.values()
#                    x=controllo_chiavi(k)
#                    if x==0:
#                        return "errore"
#                    x=trasforma_valori(v)
#                    if x==None:
#                        return "errore"
#                    else:
#                        c=[1,2,3]
#                        i=0
#                        for p in v:
#                            c[i]=str(p)
#                            i+=1
#                            diz={str(c[0]) : str(c[1]), str(x) : str(c[2])}
#                            pp=json.dumps(diz)
#                            return pp
#                        else:
#                            return "funzione non richiamata correttamente"

def controllo_chiavi(chiavi):
    if len(chiavi)!=3:
        return False
    if chiavi[0]=="value" and chiavi[1]=="originalUnit" and chiavi[2]=="targetUnit":
        return True
    else:
        return True

def trasforma_valori(valori):
    val = list(valori)
    return pytemp.pytemp(float(val[0]), val[1], val[2])

#    """ controlla i valori passati al web service e ne effetua la conversione """
#    if len(valori)!=3:
#        return False
#    if !str.isdigit(valori[0]) or !keys.intersection(valori[1]) or !keys.intersection(valori[2]):
#        return False """ se il primo valore non e' un numero e i caratteri non sono validi """
#        i=0
#        c=[3,1,2]
#        for p in valori:
#            c[i]=str(p)
#            i+=1
#            if c[1]==c[2]:
#                return None
#            if c[1]=="k" or c[1]=="K":
#                if int(c[0]) < 0:
#                    return None
#                x=pytemp.pytemp(int(c[0]),c[1],c[2])
#                return x
