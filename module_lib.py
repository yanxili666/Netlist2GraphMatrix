def node2G(graphMatrix, gNodeD, nodeIndex, mosIndex, ifInverse): # ifInverse means the direction of vi and vo change
    mosIndex = mosIndex + gNodeD['InitialMosIndex']
    if not ifInverse:
        if (gNodeD['Type'] == 'Gpm') or (gNodeD['Type'] == 'Gnm'):
            # connect GG layer
            graphMatrix[0, nodeIndex, mosIndex] = 1 
            graphMatrix[0, mosIndex, nodeIndex] = -1
            # connect GD layer
            graphMatrix[3, mosIndex, nodeIndex] = -1
            # connect GS layer
            graphMatrix[4, mosIndex, nodeIndex] = -1
    else:
        if gNodeD['Type'] == 'Gpm':
            # DD layer
            graphMatrix[1, nodeIndex, mosIndex] = 1
            graphMatrix[1, nodeIndex, mosIndex+1] = 1
            graphMatrix[1, mosIndex, nodeIndex] = -1
            graphMatrix[1, mosIndex+1, nodeIndex] = -1
            # GD layer
            graphMatrix[3, nodeIndex, mosIndex] = 1
            graphMatrix[3, nodeIndex, mosIndex+1] = 1
            # DS layer
            graphMatrix[5, mosIndex, nodeIndex] = -1
            graphMatrix[5, mosIndex+1, nodeIndex] = -1

        elif gNodeD['Type'] == 'Gnm':
            # DD layer
            graphMatrix[1, nodeIndex, mosIndex+1] = 1
            graphMatrix[1, nodeIndex, mosIndex+3] = 1
            graphMatrix[1, mosIndex+1, nodeIndex] = -1
            graphMatrix[1, mosIndex+3, nodeIndex] = -1
            # GD layer
            graphMatrix[3, nodeIndex, mosIndex+3] = 1
            graphMatrix[3, nodeIndex, mosIndex+1] = 1
            # DS layer
            graphMatrix[5, mosIndex+3, nodeIndex] = -1
            graphMatrix[5, mosIndex+1, nodeIndex] = -1
        

def g2Node(graphMatrix, gNodeD, nodeIndex, mosIndex, ifInverse):
    mosIndex = mosIndex + gNodeD['InitialMosIndex']
    if not ifInverse:
        if gNodeD['Type'] == 'Gpd':
            # DD layer
            graphMatrix[1, mosIndex, nodeIndex] = 1
            graphMatrix[1, mosIndex+2, nodeIndex] = 1
            graphMatrix[1, nodeIndex, mosIndex] = -1
            graphMatrix[1, nodeIndex, mosIndex+2] = -1
            # GD layer
            graphMatrix[3, nodeIndex, mosIndex] = -1
            graphMatrix[3, nodeIndex, mosIndex+2] = -1
            # DS layer
            graphMatrix[5, mosIndex, nodeIndex] = 1
            graphMatrix[5, mosIndex+2, nodeIndex] = 1

        elif (gNodeD['Type'] == 'Gnd') or (gNodeD['Type'] == 'Gnm'):
            # DD layer
            graphMatrix[1, mosIndex+1, nodeIndex] = 1
            graphMatrix[1, mosIndex+3, nodeIndex] = 1
            graphMatrix[1, nodeIndex, mosIndex+1] = -1
            graphMatrix[1, nodeIndex, mosIndex+3] = -1
            # GD layer
            graphMatrix[3, nodeIndex, mosIndex+1] = -1
            graphMatrix[3, nodeIndex, mosIndex+3] = -1
            # DS layer
            graphMatrix[5, mosIndex+1, nodeIndex] = 1
            graphMatrix[5, mosIndex+3, nodeIndex] = 1

        elif gNodeD['Type'] == 'Gpm':
            # DD layer
            graphMatrix[1, mosIndex, nodeIndex] = 1
            graphMatrix[1, mosIndex+1, nodeIndex] = 1
            # GD layer
            graphMatrix[3, nodeIndex, mosIndex] = -1
            graphMatrix[3, nodeIndex, mosIndex+1] = -1
            # DS layer
            graphMatrix[5, mosIndex, nodeIndex] = 1
            graphMatrix[5, mosIndex+1, nodeIndex] = 1 
    else:
        if (gNodeD['Type'] == 'Gpm') or (gNodeD['Type'] == 'Gnm'):
            # GG layer
            graphMatrix[0, mosIndex, nodeIndex] = 1
            graphMatrix[0, nodeIndex, mosIndex] = -1
            # GD layer
            graphMatrix[3, mosIndex, nodeIndex] = 1
            # GS layer
            graphMatrix[4, mosIndex, nodeIndex] = 1
        else:
            print('[error]')

def node2Node(graphMatrix, nodeIdx1, nodeIdx2): # node1 -> node2
    # all layers
    graphMatrix[:, nodeIdx1, nodeIdx2] = 1
    graphMatrix[:, nodeIdx2, nodeIdx1] = -1

def g2G(graphMatrix, gNodeD1, gNodeD2, mosIndex): # G1 -> G2
    mosIdx1 = mosIndex + gNodeD1['InitialMosIndex']
    mosIdx2 = mosIndex + gNodeD2['InitialMosIndex']
    nodeType1 = gNodeD1['Type']
    nodeType2 = gNodeD2['Type']
    if (nodeType1 == 'Gpd') and ((nodeType2 == 'Gpm') or (nodeType2 == 'Gnm')):
        # GD layer
        graphMatrix[3, mosIdx2, mosIdx1] = -1
        graphMatrix[3, mosIdx2, mosIdx1+2] = -1 
        
    elif (nodeType1 == 'Gnd') and ((nodeType2 == 'Gpm') or (nodeType2 == 'Gnm')):
        # GD layer
        graphMatrix[3, mosIdx2, mosIdx1+1] = -1
        graphMatrix[3, mosIdx2, mosIdx1+3] = -1

    elif (nodeType1 == 'Gpm') and ((nodeType2 == 'Gpm') or (nodeType2 == 'Gnm')):
        # GD layer
        graphMatrix[3, mosIdx2, mosIdx1] = -1
        graphMatrix[3, mosIdx2, mosIdx1+1] = -1
        
    elif (nodeType1 == 'Gnm') and ((nodeType2 == 'Gpm') or (nodeType2 == 'Gnm')):
        # GD layer
        graphMatrix[3, mosIdx2, mosIdx1+1] = -1
        graphMatrix[3, mosIdx2, mosIdx1+3] = -1


def inConnectG(graphMatrix, gNodeD, vIndexList, mosIndex): # Vdd, Vin, Vip, Vb, 0, Vo
    nodeType = gNodeD['Type']
    mosIndex = mosIndex + gNodeD['InitialMosIndex']
    vddIdx = vIndexList[0]
    vinIdx = vIndexList[1]
    vipIdx = vIndexList[2]
    vbIdx = vIndexList[3]
    gndIdx = vIndexList[4]
    #voIdx = vIndexList[5]

    if nodeType == 'Gpd':

        # GG layer
        graphMatrix[0, mosIndex+2, mosIndex+3] = 1
        graphMatrix[0, vipIdx, mosIndex] = 1
        graphMatrix[0, vinIdx, mosIndex+1] = 1
        graphMatrix[0, vbIdx, mosIndex+4] = 1
        graphMatrix[0, mosIndex+3, mosIndex+2] = -1
        graphMatrix[0, mosIndex, vipIdx] = -1
        graphMatrix[0, mosIndex+1, vinIdx] = -1
        graphMatrix[0, mosIndex+4, vbIdx] = -1
        # DD layer
        graphMatrix[1, mosIndex+2, mosIndex+1] = 1
        graphMatrix[1, mosIndex+1, mosIndex+2] = -1
        # SS layer
        graphMatrix[2, vddIdx, mosIndex+2] = 1
        graphMatrix[2, vddIdx, mosIndex+3] = 1
        graphMatrix[2, mosIndex+4, gndIdx] = 1
        graphMatrix[2, mosIndex+2, vddIdx] = -1
        graphMatrix[2, mosIndex+3, vddIdx] = -1
        graphMatrix[2, gndIdx, mosIndex+4] = -1
        # GD layer
        graphMatrix[3, mosIndex, vipIdx] = -1
        graphMatrix[3, mosIndex+1, vinIdx] = -1
        graphMatrix[3, mosIndex+3, mosIndex+3] = 1
        graphMatrix[3, mosIndex+4, vbIdx] = -1
        # GS layer
        graphMatrix[4, mosIndex, vipIdx] = -1
        graphMatrix[4, mosIndex+1, vinIdx] = -1
        graphMatrix[4, mosIndex+4, vbIdx] = -1
        graphMatrix[4, vddIdx, mosIndex+2] = 1
        graphMatrix[4, vddIdx, mosIndex+3] = 1
        graphMatrix[4, gndIdx, mosIndex+4] = -1
        # DS layer
        graphMatrix[5, mosIndex+4, mosIndex] = -1
        graphMatrix[5, mosIndex+4, mosIndex+1] = -1
        graphMatrix[5, vddIdx, mosIndex+2] = 1
        graphMatrix[5, vddIdx, mosIndex+3] = 1
        graphMatrix[5, gndIdx, mosIndex+4] = -1

    elif nodeType == 'Gnd':
        #print('[Debug] Gnd')
        # GG layer
        graphMatrix[0, mosIndex, vipIdx] = -1
        graphMatrix[0, mosIndex+1, vinIdx] = -1
        graphMatrix[0, mosIndex+2, mosIndex+3] = -1
        graphMatrix[0, mosIndex+3, mosIndex+2] = 1
        graphMatrix[0, mosIndex+4, vbIdx] = -1
        graphMatrix[0, vinIdx, mosIndex+1] = 1
        graphMatrix[0, vipIdx, mosIndex] = 1
        graphMatrix[0, vbIdx, mosIndex+4] = 1
        # DD layer
        graphMatrix[1, mosIndex+2, mosIndex] = 1
        graphMatrix[1, mosIndex, mosIndex+2] = -1
        # SS layer
        graphMatrix[2, mosIndex+2, vddIdx] = -1
        graphMatrix[2, mosIndex+3, vddIdx] = -1
        graphMatrix[2, vddIdx, mosIndex+2] = 1
        graphMatrix[2, vddIdx, mosIndex+3] = 1
        graphMatrix[2, mosIndex+4, gndIdx] = 1
        graphMatrix[2, gndIdx, mosIndex+4] = -1
        # GD layer
        graphMatrix[3, mosIndex+2, mosIndex+2] = 1
        graphMatrix[3, vinIdx, mosIndex+1] = 1
        graphMatrix[3, vipIdx, mosIndex] = 1
        graphMatrix[3, vbIdx, mosIndex+4] = 1
        # GS layer
        graphMatrix[4, mosIndex, vipIdx] = -1
        graphMatrix[4, mosIndex+1, vinIdx] = -1
        graphMatrix[4, mosIndex+4, vbIdx] = -1
        graphMatrix[4, vddIdx, mosIndex+2] = 1
        graphMatrix[4, vddIdx, mosIndex+3] = 1
        graphMatrix[4, gndIdx, mosIndex+4] = -1
        # DS layer
        graphMatrix[5, mosIndex+4, mosIndex] = -1
        graphMatrix[5, mosIndex+4, mosIndex+1] = -1
        graphMatrix[5, vddIdx, mosIndex+2] = 1
        graphMatrix[5, vddIdx, mosIndex+3] = 1
        graphMatrix[5, gndIdx, mosIndex+4] = -1

    elif nodeType == 'Gpm':
        #print('[Debug] Gpm')
        # GG layer
        graphMatrix[0, mosIndex+1, vbIdx] = -1
        graphMatrix[0, vbIdx, mosIndex+1] = 1
        # DD layer
        #graphMatrix[1, mosIndex, voIdx] = 1
        #graphMatrix[1, mosIndex+1, voIdx] = 1
        #graphMatrix[1, voIdx, mosIndex] = -1
        #graphMatrix[1, voIdx, mosIndex+1] = -1

        # SS layer
        graphMatrix[2, mosIndex, vddIdx] = -1
        graphMatrix[2, vddIdx, mosIndex] = 1
        graphMatrix[2, mosIndex+1, gndIdx] = 1
        graphMatrix[2, gndIdx, mosIndex+1] = -1
        # GD layer
        graphMatrix[3, mosIndex+1, vbIdx] = -1
        #graphMatrix[3, voIdx, mosIndex] = -1
        #graphMatrix[3, voIdx, mosIndex+1] = -1

        # GS layer
        graphMatrix[4, mosIndex+1, vbIdx] = -1
        graphMatrix[4, vddIdx, mosIndex] = 1
        graphMatrix[4, gndIdx, mosIndex+1] = -1
        # DS layer
        #graphMatrix[5, mosIndex, voIdx] = 1
        #graphMatrix[5, mosIndex+1, voIdx] = 1
        graphMatrix[5, vddIdx, mosIndex] = 1
        graphMatrix[5, gndIdx, mosIndex+1] = -1

    elif nodeType == 'Gnm':
        # GG layer
        graphMatrix[0, mosIndex+1, vbIdx] = -1
        graphMatrix[0, mosIndex+2, mosIndex+3] = 1
        graphMatrix[0, mosIndex+3, mosIndex+2] = -1
        graphMatrix[0, vbIdx, mosIndex+1] = 1
        # DD layer
        graphMatrix[1, mosIndex, mosIndex+2] = 1
        graphMatrix[1, mosIndex+2, mosIndex] = -1
        # SS layer
        graphMatrix[2, mosIndex+2, gndIdx] = 1
        graphMatrix[2, mosIndex+3, gndIdx] = 1
        graphMatrix[2, vddIdx, mosIndex] = 1
        graphMatrix[2, vddIdx, mosIndex+1] = 1
        # GD layer
        graphMatrix[3, mosIndex+1, vbIdx] = -1
        graphMatrix[3, mosIndex+2, mosIndex+2] = -1
        # GS layer
        graphMatrix[4, mosIndex+1, vbIdx] = -1
        graphMatrix[4, vddIdx, mosIndex] = 1
        graphMatrix[4, vddIdx, mosIndex+1] = 1
        graphMatrix[4, gndIdx, mosIndex+2] = -1
        graphMatrix[4, gndIdx, mosIndex+3] = -1
        # DS layer
        graphMatrix[5, vddIdx, mosIndex] = 1
        graphMatrix[5, vddIdx, mosIndex+1] = 1
        graphMatrix[5, gndIdx, mosIndex+2] = -1
        graphMatrix[5, gndIdx, mosIndex+3] = -1
    

    