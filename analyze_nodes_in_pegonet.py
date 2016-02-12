import time
import csv
start_time = time.time()

def mean(alist):
    return sum(alist)/len(alist)


nbOfNodes = 0
property_map_first = {}
property_map_second = {}
property_map_third = {}
existAt1 = {}
existAt2 = {}
existAt3 = {}
in_pegonet_count = {}

choice = int(raw_input("Input your choice (1~3):"))

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
        property_map_first[nodeid] = [int(tmpvar) for tmpvar in tmplist[1].split('/')]
        property_map_second[nodeid] = [int(tmpvar) for tmpvar in tmplist[2].split('/')]
        property_map_third[nodeid] = [int(tmpvar) for tmpvar in tmplist[3].split('/')]

        existAt1[nodeid] = True
        existAt2[nodeid] = True
        existAt3[nodeid] = True
        if sum(property_map_first[nodeid]) == 0:
            existAt1[nodeid] = False
        if sum(property_map_second[nodeid]) == 0:
            existAt2[nodeid] = False
        if sum(property_map_third[nodeid]) == 0:
            existAt3[nodeid] = False
        in_pegonet_count[nodeid] = 0

print("Read the info of all nodes")
print("--- %s seconds ---" % (time.time() - start_time))


if choice == 1:
    filename = "pEgonet_second_first"
    csvoutputfilename = "second_first.csv"
elif choice == 2:
    filename = "pEgonet_third_first"
    csvoutputfilename = "third_first.csv"
elif choice == 3:
    filename = "pEgonet_third_second"
    csvoutputfilename = "third_second.csv"

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
        nodesstr = tmplist[1]
        nodesstr = nodesstr[1:-1]
        try:
            nodes = [int(n) for n in nodesstr.split(',')]
            for node in nodes:
                in_pegonet_count[node] += 1
        except:
            pass
print("Read the info of all pEgonets")
print("--- %s seconds ---" % (time.time() - start_time))

newdataset = []
for curnodeid in range(nbOfNodes):
    nodeproperties = property_map_second[curnodeid]
    if choice < 3:
        nodeproperties = property_map_first[curnodeid]

    newdataset.append((curnodeid, in_pegonet_count[curnodeid],nodeproperties[0], nodeproperties[1], nodeproperties[2], nodeproperties[3], nodeproperties[4]))
print("Finished the analysis")
print("--- %s seconds ---" % (time.time() - start_time))


with open('csv_output/'+csvoutputfilename, 'w') as csvfile:
    fieldnames = ['nodeid', '#Pegonets', 'nodesize', '#instances', '#instancesHavingType', '#instancesRedirected', 'infoboxLength']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for data in newdataset:
        current_node_id = int(data[0])
        if ((choice < 3 and existAt1[current_node_id]) or (choice == 3 and existAt2[current_node_id])):
            writer.writerow({'nodeid': data[0],
                            '#Pegonets': data[1],
                            'nodesize': data[2],
                            '#instances': data[3],
                            '#instancesHavingType': data[4],
                            '#instancesRedirected': data[5],
                            'infoboxLength': data[6]})
print("Write the analysis result to a csv file")
print("--- %s seconds ---" % (time.time() - start_time))
