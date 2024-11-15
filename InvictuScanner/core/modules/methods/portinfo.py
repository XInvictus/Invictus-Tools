import json

def port_lookup(port):
    ports = json.loads(open('core/assets/ports.json', 'r').read())
    if str(port) in ports:
        return ports[str(port)]
    else:
        return {
            "service": "Unknown",
            "protocols": "Unknown"
        }