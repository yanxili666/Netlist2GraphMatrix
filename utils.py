def addNode(name, port, portDict, lNext):
    if port not in portDict.keys():
        portDict.update({
            port:{
                'last': [],
                'next': []
            }
        })
    portDict[port][lNext].append(name)
