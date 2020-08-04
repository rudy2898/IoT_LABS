import cherrypy
import json
import pytemp


units = ['c', 'f', 'k']

def check_unit(oU, tU):
    if oU.lower() not in units or tU.lower() not in units:
        return 0
    return 1

def switcher(cl, cu):
    if cl == False:
        return "Not all numbers in the list"
    elif cu == False:
        return "Unit passed not available"
    return "Cannot convert from same units"


def check_list(list):
    for num in list:
        if not isinstance(num, int):
            return 0
    return 1


def check_values(list):
    for l in list:
        if l < -273.15:
            return 0
    return 1


def check_equals(oU, tU):
    if oU.lower() == tU.lower():
        return 0
    return 1


def convert(original_list, oU, tU):
    list = []
    for num in original_list:
        list.append(round(pytemp.pytemp(int(num), oU.lower(), tU.lower()), 2))
    return list


class myWebServices(object):
    exposed=True

    def __init__(self):
        pass

    def PUT(self, **params):
        body = cherrypy.request.body.read()
        json_body = json.loads(body.decode('utf-8'))
        # se si prova ad inserire un carattere indipendentemente dalla posizione e non un numero ritorna direttamente
        # errore senza salvare nulla nella lista, non so come si potrebbe controllare fin da subito
        list_values = json_body['values']
        originalUnit = json_body['originalUnit']
        targetUnit = json_body['targetUnit']
        cl = check_list(list_values)
        cu = check_unit(originalUnit, targetUnit)
        ce = check_equals(originalUnit, targetUnit)
        if cl==(cu==(ce==True)):
            values = convert(list_values, originalUnit, targetUnit)
            if check_values(values):
                json_body['convertedValue'] = values
                return json.dumps(json_body)
            else:
                return json.dumps({"Error": "Values over absolute zero."})
        else:
            ret = switcher(cl, cu)
            return ret


if __name__ == "__main__":
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tool.session.on': True
        }
    }
    cherrypy.tree.mount(myWebServices(), '/', conf)
    cherrypy.engine.start()
    cherrypy.engine.block()
