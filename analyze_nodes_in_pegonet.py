import time
import csv
start_time = time.time()

def mean(alist):
    return sum(alist)/len(alist)


nbOfNodes = 0
property_map_first = {}
property_map_second = {}
property_map_third = {}
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
    nodesize = property_map_second[curnodeid][0]
    if choice < 3:
        nodesize = property_map_first[curnodeid][0]
    newdataset.append((curnodeid, in_pegonet_count[curnodeid],nodesize))
print("Finished the analysis")
print("--- %s seconds ---" % (time.time() - start_time))


with open('csv_output/'+csvoutputfilename, 'w') as csvfile:
    fieldnames = ['nodeid', '#Pegonets', 'nodesize']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for data in newdataset:
        writer.writerow({'nodeid': data[0], '#Pegonets': data[1], 'nodesize': data[2]})
print("Write the analysis result to a csv file")
print("--- %s seconds ---" % (time.time() - start_time))
