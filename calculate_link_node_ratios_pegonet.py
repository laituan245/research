import time
import copy
import os
import csv
import random
start_time = time.time()

choice = int(raw_input("Input your choice (1~3): "))

if choice == 1:
    choices = [1]
elif choice == 2:
    choices = [2]
elif choice == 3:
    choices = [3]
elif choice == 4:
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


for choice in choices:
    if choice == 1:
        filename = "pEgonet_second_first"
        outputfilename = "ratio_second_first.csv"
    elif choice == 2:
        filename = "pEgonet_third_first"
        outputfilename = "ratio_third_first.csv"
    elif choice == 3:
        filename = "pEgonet_third_second"
        outputfilename = "ratio_third_second.csv"

    nbnodeslist = []
    nbedgeslist = []
    nbPegonets = 0
    first = True
    f = open('output/' + filename, 'r')
    for line in f:
        if first:
            first = False
        else:
            nbPegonets += 1
            line = line.strip()
            tmplist = line.split()
            nodesstr = tmplist[1][1:-1]; nodelist = nodesstr.split(','); nbnodes = float(len(nodelist))
            edgesstr = tmplist[2][1:-1]; edgelist = edgesstr.split(','); nbedges = float(len(edgelist))
            nbnodeslist.append(nbnodes)
            nbedgeslist.append(nbedges)
    f.close()
    print("Read the info of all pEgonets")
    print("--- %s seconds ---" % (time.time() - start_time))


    if not os.path.exists('link_node_ratio_output'):
        os.makedirs('link_node_ratio_output')

    with open('link_node_ratio_output/'+outputfilename, 'w') as csvfile:
        fieldnames = ['#nodesInPegonet', '#edgesInPegonet', 'ratioForPegonet']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        print 'nbPegonets = ' + str(nbPegonets)
        for i in range(nbPegonets):
            if (i % 10000 == 0):
                print 'currently, i = ' + str(i)
            row = {}
            row['#nodesInPegonet'] = int(nbnodeslist[i])
            row['#edgesInPegonet'] = int(nbedgeslist[i])
            row['ratioForPegonet'] = float(nbedgeslist[i]) / float(nbnodeslist[i])

            writer.writerow(copy.deepcopy(row))

    print ("Wrote the results to " + outputfilename)
    print("--- %s seconds ---" % (time.time() - start_time))
