import time
import subprocess
import copy
import os
import csv
import random
start_time = time.time()

#selection = int(raw_input("Input your choice (1~3): "))
selection = 4

if selection == 1:
    choices = [1]
elif selection == 2:
    choices = [2]
elif selection == 3:
    choices = [3]
elif selection == 4:
    choices = [1, 2, 3]


for choice in choices:
    print 'current choice = ' + str(choice)
    if choice == 1:
        filename = "pEgonet_second_first"
        outputfilename = "pegonet_ratios_second_first.csv"
    elif choice == 2:
        filename = "pEgonet_third_first"
        outputfilename = "pegonet_ratios_third_first.csv"
    elif choice == 3:
        filename = "pEgonet_third_second"
        outputfilename = "pegonet_ratios_third_second.csv"

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
            nodesstr = tmplist[1][1:-1].strip(); nodelist = nodesstr.split(','); nbnodes = float(len(nodelist))
            edgesstr = tmplist[2][1:-1].strip(); edgelist = edgesstr.split(','); nbedges = float(len(edgelist))
            if (nodelist[0] == ''):
                nbnodes = 0
            if (edgelist[0] == ''):
                nbedges = 0
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
            try:
                row['ratioForPegonet'] = float(nbedgeslist[i]) / float(nbnodeslist[i])
            except ZeroDivisionError:
                row['ratioForPegonet'] = 0

            writer.writerow(copy.deepcopy(row))

    print ("Wrote the results to " + outputfilename)
    print("--- %s seconds ---" % (time.time() - start_time))

if (selection == 4):
    print("Executing the R script in calculate_avg_link_node_ratios.R")
    command = 'Rscript'
    cmd = [command, 'calculate_avg_link_node_ratios.R']
    x = subprocess.check_output(cmd, universal_newlines=True)
    print("--- %s seconds ---" % (time.time() - start_time))
