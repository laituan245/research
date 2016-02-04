import time
start_time = time.time()

existAt1 = {}
existAt2 = {}
existAt3 = {}

first = True
f = open('input/nodes.kmap')
for line in f:
    if first:
        first = False
    else:
        line = line.strip()
        tmplist = line.split()
        nodeid = int(tmplist[0])
        existAt1[nodeid] = True
        if (tmplist[1] == '0/0/0/0/0'):
            existAt1[nodeid] = False
        existAt2[nodeid] = True
        if (tmplist[2] == '0/0/0/0/0'):
            existAt2[nodeid] = False
        existAt3[nodeid] = True
        if (tmplist[3] == '0/0/0/0/0'):
            existAt3[nodeid] = False
print("Read the info of all nodes")
print("--- %s seconds ---" % (time.time() - start_time))


#testingNodeId = int(raw_input('Input new node at the second timeslot'))
testingNodeId = 3
neighborSet = [testingNodeId]

first = True
f = open('input/edges.kmap')
for line in f:
    if first:
        first = False
    else:
        line = line.strip()
        tmplist = line.split()[0].split('/')
        a = int(tmplist[0])
        b = int(tmplist[1])
        if (a == testingNodeId):
            neighborSet.append(b);
        if (b == testingNodeId):
            neighborSet.append(a);

f.close()
print("Read the info of all edges")
print("--- %s seconds ---" % (time.time() - start_time))


tmpEdges = []
edgeId = 0
first = True
f = open('input/edges.kmap')
for line in f:
    if first:
        first = False
    else:
        line = line.strip()
        tmplist = line.split()[0].split('/')
        a = int(tmplist[0])
        b = int(tmplist[1])
        if (a in neighborSet and b in neighborSet):
            tmpEdges.append((edgeId, a, b))
        edgeId = edgeId + 1

egonetNodes = []
egonetEdges = []
print 'Egonet of the node ' + str(testingNodeId) + ' at this second timeslot is:'
for edge in tmpEdges:
    edgeId, a, b = edge
    if (existAt2[a] and existAt2[b]):
        egonetEdges.append(edgeId)
for nodeId in neighborSet:
    if existAt2[nodeId] and (not nodeId in egonetNodes):
        egonetNodes.append(nodeId)
print str(egonetNodes) + ' ' + str(egonetEdges)

egonetNodes = []
egonetEdges = []
print 'pEgonet of this node (pEgonet_second_first) is:'
for edge in tmpEdges:
    edgeId, a, b = edge
    if (existAt1[a] and existAt1[b]):
        egonetEdges.append(edgeId)
for nodeId in neighborSet:
    if existAt1[nodeId] and (not nodeId in egonetNodes):
        egonetNodes.append(nodeId)
print str(egonetNodes) + ' ' + str(egonetEdges)


#testingNodeId = int(raw_input('Input new node at the second timeslot'))
testingNodeId = 13
neighborSet = [testingNodeId]

first = True
f = open('input/edges.kmap')
for line in f:
    if first:
        first = False
    else:
        line = line.strip()
        tmplist = line.split()[0].split('/')
        a = int(tmplist[0])
        b = int(tmplist[1])
        if (a == testingNodeId):
            neighborSet.append(b);
        if (b == testingNodeId):
            neighborSet.append(a);

tmpEdges = []
edgeId = 0
first = True
f = open('input/edges.kmap')
for line in f:
    if first:
        first = False
    else:
        line = line.strip()
        tmplist = line.split()[0].split('/')
        a = int(tmplist[0])
        b = int(tmplist[1])
        if (a in neighborSet and b in neighborSet):
            tmpEdges.append((edgeId, a, b))
        edgeId = edgeId + 1

egonetNodes = []
egonetEdges = []
print 'Egonet of the node ' + str(testingNodeId) + ' at this third timeslot is:'
for edge in tmpEdges:
    edgeId, a, b = edge
    if (existAt3[a] and existAt3[b]):
        egonetEdges.append(edgeId)
for nodeId in neighborSet:
    if existAt3[nodeId] and (not nodeId in egonetNodes):
        egonetNodes.append(nodeId)
print str(egonetNodes) + ' ' + str(egonetEdges)

egonetNodes = []
egonetEdges = []
print 'pEgonet of this node at first timeslot (pEgonet_third_first) is:'
for edge in tmpEdges:
    edgeId, a, b = edge
    if (existAt1[a] and existAt1[b]):
        egonetEdges.append(edgeId)
for nodeId in neighborSet:
    if existAt1[nodeId] and (not nodeId in egonetNodes):
        egonetNodes.append(nodeId)
print str(egonetNodes) + ' ' + str(egonetEdges)

egonetNodes = []
egonetEdges = []
print 'pEgonet of this node at second timeslot (pEgonet_third_second) is:'
for edge in tmpEdges:
    edgeId, a, b = edge
    if (existAt2[a] and existAt2[b]):
        egonetEdges.append(edgeId)
for nodeId in neighborSet:
    if existAt2[nodeId] and (not nodeId in egonetNodes):
        egonetNodes.append(nodeId)
print str(egonetNodes) + ' ' + str(egonetEdges)
