# This code is too slow
import time
import subprocess
import copy
import os
import csv
import random
start_time = time.time()

choices = [1, 2, 3]

nbOfNodes = 0
nodeExistAt1 = []
nodeExistAt2 = []
nodeExistAt3 = []
first = True
f = open('input/nodes.kmap', 'r')
for line in f:
    if first:
        # The first line is
        # #node_id node_size/#instances/#instancesHavingType/#instancesRedirected/infoboxLength
        first = False
    else:
        nbOfNodes += 1
        line = line.strip()
        tmplist = line.split()
        nodeid = int(tmplist[0])
        property_map_first = [int(tmpvar) for tmpvar in tmplist[1].split('/')]
        property_map_second = [int(tmpvar) for tmpvar in tmplist[2].split('/')]
        property_map_third = [int(tmpvar) for tmpvar in tmplist[3].split('/')]

        if sum(property_map_first) != 0:
            nodeExistAt1.append(nodeid)
        if sum(property_map_second) != 0:
            nodeExistAt2.append(nodeid)
        if sum(property_map_third) != 0:
            nodeExistAt3.append(nodeid)

print("Read the info of all nodes")
print("--- %s seconds ---" % (time.time() - start_time))


adjList = [[] for i in range(nbOfNodes)]
cur_nb_edges = 0
f = open('input/edges.kmap', 'r')
first_line = True
for line in f:
    if (first_line):
        first_line = False
    else:
        line = line.strip()
        a,b  = (line.split()[0]).split('/')
        a,b  = int(a), int(b)
        cur_nb_edges = cur_nb_edges + 1
        adjList[a].append(b)
        if (cur_nb_edges % 1000000 == 0):
            print 'cur_nb_edges = ' + str(cur_nb_edges)

f.close()
print("Read the info of all edges")
print("--- %s seconds ---" % (time.time() - start_time))


for choice in choices:
    print 'current choice = ' + str(choice)
    if choice == 1:
        inputfilename = "pegonet_avgratios_second_first.csv"
        outputfilename = 'randomnodes_avgratios_second_first.csv'
    elif choice == 2:
        inputfilename = "pegonet_avgratios_third_first.csv"
        outputfilename = 'randomnodes_avgratios_third_first.csv'
    elif choice == 3:
        inputfilename = "pegonet_avgratios_third_second.csv"
        outputfilename = 'randomnodes_avgratios_third_second.csv'

    nbnodeslist = []
    with open('link_node_ratio_output/' + inputfilename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            nbnodeslist.append(int(row['nbNodesInPegonet']))

    rslists = []
    for curnbnode in nbnodeslist:
        nbstimulations = 50
        rsratio = 0
        for j in range(nbstimulations):
            edgecounts = 0
            if choice < 3:
                mylist = nodeExistAt1
            elif choice == 3:
                mylist = nodeExistAt2
            rand_smpl = [ mylist[z] for z in sorted(random.sample(xrange(len(mylist)), curnbnode)) ]
            for tmpnode1 in rand_smpl:
                for z in range(len(adjList[tmpnode1])):
                    if (adjList[tmpnode1][z] in rand_smpl):
                        edgecounts += 1
            try:
                tmpincr = (float(edgecounts) / float(curnbnode))
                rsratio += tmpincr
            except ZeroDivisionError:
                pass
        rsratio = rsratio / nbstimulations

        rslists.append(rsratio)

    with open('link_node_ratio_output/' + outputfilename, 'w') as csvfile:
        fieldnames = ['nbNodesInPegonet', 'avgRatios']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(len(rslists)):
            row = {}
            row['nbNodesInPegonet'] = int(nbnodeslist[i])
            row['avgRatios'] = float(rslists[i])
            writer.writerow(copy.deepcopy(row))
