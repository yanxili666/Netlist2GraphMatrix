import os
import re
import torch
import numpy as np
from module_lib import *
from utils import *
import numpy as np

# output complete matrix
np.set_printoptions(threshold=np.inf)

work_dir = os.getcwd()
circuits_path = "./transistor_level_circuits/"
all_circuits = os.listdir(circuits_path)

for circuit in all_circuits:
    netlist = open("{}{}/netlist/netlist".format(circuits_path, circuit), "r")
    gpdNum = 0
    gndNum = 0
    gpmNum = 0
    gnmNum = 0
    mosNum = 0
    rNum = 0
    cNum = 0
    totalNum = 6 # Vdd, Vip, Vin, Vb, GND, Vo
    graphMatrix = [] # N x N x 6
    rDict = {}
    cDict = {}
    gpdDict = {}
    gndDict = {}
    gpmDict = {}
    gnmDict = {}
    deviceDict = {}
    deviceList = []
    totalPortDict = {}
    #portList = []

    for line in netlist.readlines():
        line.strip()
        # match device and obtain the ports
        matchR = re.search(r'^(R\d)\s[(](\S+)\s(\S+)[)]\s\S+\s\S+$', line)
        matchC = re.search(r'^(C\d)\s[(](\S+)\s(\S+)[)]\s\S+\s\S+$', line)
        matchGpd = re.search(r'^(I\d)\s[(]vdd!\s(\S+)\s(\S+)\s(\S+)\s(\S+)\s(\S+)[)]\sgm_positive_diff_\d$', line) # positive diff
        matchGnd = re.search(r'^(I\d)\s[(]vdd!\s(\S+)\s(\S+)\s(\S+)\s(\S+)\s(\S+)[)]\sgm_negative_diff_\d$', line) # negative diff
        matchGpm = re.search(r'^(I\d)\s[(]vdd!\s(\S+)\s(\S+)\s(\S+)\s(\S+)[)]\sgm_positive_mid_\d$', line) # positive mid
        matchGnm = re.search(r'^(I\d)\s[(]vdd!\s(\S+)\s(\S+)\s(\S+)\s(\S+)[)]\sgm_negative_mid_\d$', line) # negative mid
    
        if matchR:
            rNum += 1
            rDict.update({matchR.groups()[0]:{'Vin': matchR.groups()[1],
                                              'Vo': matchR.groups()[2]}})
            deviceList.append(matchR.groups()[0])
            #portList.append(matchR.groups()[1])
            #portList.append(matchR.groups()[2])
            addNode(matchR.groups()[0], matchR.groups()[1], totalPortDict, 'next')
            addNode(matchR.groups()[0], matchR.groups()[2], totalPortDict, 'last')   
        elif matchC: 
            cNum += 1
            cDict.update({matchC.groups()[0]:{'Vin': matchC.groups()[1],
                                              'Vo': matchC.groups()[2]}})
            deviceList.append(matchC.groups()[0])
            addNode(matchC.groups()[0], matchC.groups()[1], totalPortDict, 'next')
            addNode(matchC.groups()[0], matchC.groups()[2], totalPortDict, 'last')
            #portList.append(matchC.groups()[1])
            #portList.append(matchC.groups()[2])
        elif matchGpd:
            gpdDict.update({'Gpd{}'.format(gpdNum): {'Vin': matchGpd.groups()[1],
                                                     'Vip': matchGpd.groups()[2],
                                                     'Vo': matchGpd.groups()[3],
                                                     'Vss': matchGpd.groups()[4],
                                                     'Vb': matchGpd.groups()[5],
                                                     'InitialMosIndex': mosNum,
                                                     'MosNumber': 5,
                                                     'Type': 'Gpd',
                                                     'Inverse': False
            }})
            deviceList.append('Gpd{}'.format(gpdNum))
            addNode('Gpd{}'.format(gpdNum), matchGpd.groups()[1], totalPortDict, 'next')
            addNode('Gpd{}'.format(gpdNum), matchGpd.groups()[3], totalPortDict, 'last')
            #portList.append(matchGpd.groups()[1])
            #portList.append(matchGpd.groups()[2])
            #portList.append(matchGpd.groups()[3])
            #portList.append(matchGpd.groups()[4])
            #portList.append(matchGpd.groups()[5])
            gpdNum += 1
            mosNum += 5
        elif matchGnd:
            gndDict.update({'Gnd{}'.format(gndNum): {'Vin': matchGnd.groups()[1],
                                                     'Vip': matchGnd.groups()[2],
                                                     'Vo': matchGnd.groups()[3],
                                                     'Vss': matchGnd.groups()[4],
                                                     'Vb': matchGnd.groups()[5],
                                                     'InitialMosIndex': mosNum,
                                                     'MosNumber': 5,
                                                     'Type': 'Gnd',
                                                     'Inverse': False
            }})
            deviceList.append('Gnd{}'.format(gndNum))
            addNode('Gnd{}'.format(gndNum), matchGnd.groups()[1], totalPortDict, 'next')
            addNode('Gnd{}'.format(gndNum), matchGnd.groups()[3], totalPortDict, 'last')
            #portList.append(matchGnd.groups()[1])
            #portList.append(matchGnd.groups()[2])
            #portList.append(matchGnd.groups()[3])
            #portList.append(matchGnd.groups()[4])
            #portList.append(matchGnd.groups()[5])
            gndNum += 1
            mosNum += 5
        elif matchGpm:
            # consider feedback
            ifInverse = False
            if matchGpm.groups()[1] == 'net_vo':
                addNode('Gpm{}'.format(gpmNum), matchGpm.groups()[1], totalPortDict, 'last')
                addNode('Gpm{}'.format(gpmNum), matchGpm.groups()[2], totalPortDict, 'next')
                ifInverse = True
            else:
                addNode('Gpm{}'.format(gpmNum), matchGpm.groups()[1], totalPortDict, 'next')
                addNode('Gpm{}'.format(gpmNum), matchGpm.groups()[2], totalPortDict, 'last')
            gpmDict.update({'Gpm{}'.format(gpmNum): {'Vin': matchGpm.groups()[1],
                                                     'Vo': matchGpm.groups()[2],
                                                     'Vss': matchGpm.groups()[3],
                                                     'Vb': matchGpm.groups()[4],
                                                     'InitialMosIndex': mosNum,
                                                     'MosNumber': 2,
                                                     'Type': 'Gpm',
                                                     'Inverse': ifInverse
            }})
            deviceList.append('Gpm{}'.format(gpmNum))
            #portList.append(matchGpm.groups()[1])
            #portList.append(matchGpm.groups()[2])
            #portList.append(matchGpm.groups()[3])
            #portList.append(matchGpm.groups()[4])
            gpmNum += 1
            mosNum += 2
        elif matchGnm:
            # consider feedback
            ifInverse = False
            if matchGnm.groups()[1] == 'net_vo':
                ifInverse = True
                addNode('Gnm{}'.format(gnmNum), matchGnm.groups()[1], totalPortDict, 'last')
                addNode('Gnm{}'.format(gnmNum), matchGnm.groups()[2], totalPortDict, 'next')
            else:
                addNode('Gnm{}'.format(gnmNum), matchGnm.groups()[1], totalPortDict, 'next')
                addNode('Gnm{}'.format(gnmNum), matchGnm.groups()[2], totalPortDict, 'last')
            gnmDict.update({'Gnm{}'.format(gnmNum): {'Vin': matchGnm.groups()[1],
                                                     'Vo': matchGnm.groups()[2],
                                                     'Vss': matchGnm.groups()[3],
                                                     'Vb': matchGnm.groups()[4],
                                                     'InitialMosIndex': mosNum,
                                                     'MosNumber': 4,
                                                     'Type': 'Gnm',
                                                     'Inverse': ifInverse
            }})
            deviceList.append('Gnm{}'.format(gnmNum))  
            #portList.append(matchGnm.groups()[1])
            #portList.append(matchGnm.groups()[2])
            #portList.append(matchGnm.groups()[3])
            #portList.append(matchGnm.groups()[4])
            gnmNum += 1
            mosNum += 4
    netlist.close()
    deviceDict.update(rDict)
    deviceDict.update(cDict)
    deviceDict.update(gpdDict)
    deviceDict.update(gndDict)
    deviceDict.update(gpmDict)
    deviceDict.update(gnmDict)
    totalNum = totalNum + rNum + cNum + mosNum
    gNum = gpdNum + gndNum + gpmNum + gnmNum
    graphMatrix = np.zeros((6, totalNum, totalNum)) # GG, DD, SS, GD, GD, DS and R, C, Mos, V (Vdd, Vin, Vip, Vb, 0, Vo)
    rIndex = 0
    cIndex = rNum
    mosIndex = rNum + cNum
    voIndex = totalNum - 1
    groundIndex = totalNum - 2
    vbIndex = totalNum - 3
    vipIndex = totalNum - 4
    vinIndex = totalNum - 5
    vddIndex = totalNum - 6
    vIndexList = [vddIndex, vinIndex, vipIndex, vbIndex, groundIndex, voIndex]

    # construct the internal structures of all G
    for device in deviceList:
        if device[0:1] == 'G':
            inConnectG(graphMatrix, deviceDict[device], vIndexList, mosIndex)

    # construct the connectction structure of all nodes
    for port in totalPortDict.keys():
        portDict = totalPortDict[port]
        if port == 'net_vin':
            for dev in portDict['next']:            
                if dev[0:1] == 'R':
                    node2Node(graphMatrix, vinIndex, (rIndex+int(dev[1:2])))
                elif dev[0:1] == 'C':
                    node2Node(graphMatrix, vinIndex, (cIndex+int(dev[1:2])))
                elif dev[0:1] == 'G':
                    node2G(graphMatrix, deviceDict[dev], vinIndex, mosIndex, deviceDict[dev]['Inverse'])         
        elif port == '0':
            for dev in portDict['last']:
                if dev[0:1] == 'R':
                    node2Node(graphMatrix, (rIndex+int(dev[1:2])), groundIndex)
                elif dev[0:1] == 'C':
                    node2Node(graphMatrix, (cIndex+int(dev[1:2])), groundIndex)
                elif dev[0:1] == 'G':
                    g2Node(graphMatrix, deviceDict[dev], groundIndex, mosIndex, deviceDict[dev]['Inverse'])
        elif port == 'net_vo':
            for dev in portDict['next']:               
                if dev[0:1] == 'R':
                    node2Node(graphMatrix, voIndex, (rIndex+int(dev[1:2])))
                elif dev[0:1] == 'C':
                    node2Node(graphMatrix, voIndex, (cIndex+int(dev[1:2])))
                elif dev[0:1] == 'G':
                    node2G(graphMatrix, deviceDict[dev], voIndex, mosIndex, deviceDict[dev]['Inverse']) 
            for dev in portDict['last']:
                if dev[0:1] == 'R':
                    node2Node(graphMatrix, (rIndex+int(dev[1:2])), voIndex)
                elif dev[0:1] == 'C':
                    node2Node(graphMatrix, (cIndex+int(dev[1:2])), voIndex)
                elif dev[0:1] == 'G':
                    g2Node(graphMatrix, deviceDict[dev], voIndex, mosIndex, deviceDict[dev]['Inverse'])    
        else:
            for dev1 in portDict['last']:
                for dev2 in portDict['next']:
                    if (dev1[0:1] == 'R') and (dev2[0:1] == 'R'):
                        node2Node(graphMatrix, rIndex+int(dev1[1:2]), rIndex+int(dev2[1:2]))
                    elif (dev1[0:1] == 'R') and (dev2[0:1] == 'C'):
                        node2Node(graphMatrix, rIndex+int(dev1[1:2]), cIndex+int(dev2[1:2]))
                    elif (dev1[0:1] == 'R') and (dev2[0:1] == 'G'):
                        node2G(graphMatrix, deviceDict[dev2], rIndex+int(dev1[1:2]), mosIndex, deviceDict[dev2]['Inverse'])
                    elif (dev1[0:1] == 'C') and (dev2[0:1] == 'R'):
                        node2Node(graphMatrix, cIndex+int(dev1[1:2]), rIndex+int(dev2[1:2]))
                    elif (dev1[0:1] == 'C') and (dev2[0:1] == 'C'):
                        node2Node(graphMatrix, cIndex+int(dev1[1:2]), cIndex+int(dev2[1:2]))
                    elif (dev1[0:1] == 'C') and (dev2[0:1] == 'G'):
                        node2G(graphMatrix, deviceDict[dev2], cIndex+int(dev1[1:2]), mosIndex, deviceDict[dev2]['Inverse'])
                    elif (dev1[0:1] == 'G') and (dev2[0:1] == 'R'):
                        g2Node(graphMatrix, deviceDict[dev1], rIndex+int(dev2[1:2]), mosIndex, deviceDict[dev1]['Inverse'])
                    elif (dev1[0:1] == 'G') and (dev2[0:1] == 'C'):
                        g2Node(graphMatrix, deviceDict[dev1], cIndex+int(dev2[1:2]), mosIndex, deviceDict[dev1]['Inverse'])
                    elif (dev1[0:1] == 'G') and (dev2[0:1] == 'G'):
                        g2G(graphMatrix, deviceDict[dev1], deviceDict[dev2], mosIndex)
    #print('\n\n')
    tGraphMatrix = torch.from_numpy(graphMatrix)
    # save data

    if not os.path.exists('./gmatrix_circuits/{}'.format(circuit)):
        os.mkdir('./gmatrix_circuits/' + circuit)
    torch.save(tGraphMatrix, "{}{}/data.pt".format('./gmatrix_circuits/', circuit))
    np.save("{}{}/device_dict.npy".format('./gmatrix_circuits/', circuit), deviceDict)
    np.save("{}{}/port_dict.npy".format('./gmatrix_circuits/', circuit), totalPortDict)
    print('[Info] circuits {} is finished'.format(circuit))
    