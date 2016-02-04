#include <iostream>
#include <fstream>
#include <string>
#include <time.h>
#include <vector>
#include <string.h>
#include <utility>      // std::pair, std::make_pair
#include <unordered_map>
#include <map>
#include <iostream>
#define NBNODES 971427
#define ui unsigned int
using namespace std;

struct node {
  bool existAt1;
  bool existAt2;
  bool existAt3;
};

vector<string> split(string str,string sep){
    char* cstr=const_cast<char*>(str.c_str());
    char* current;
    std::vector<std::string> arr;
    current=strtok(cstr,sep.c_str());
    while(current!=NULL){
        arr.push_back(current);
        current=strtok(NULL,sep.c_str());
    }
    return arr;
}

ui charToDigit (char c) {
  string tmpStr = "0123456789";
  for (ui i = 0; i < tmpStr.length(); i++)
    if (tmpStr[i] == c)
      return i;
}

ui stringToNb (string tmpStr) {
  ui result = 0;
  for (ui i = 0; i < tmpStr.length(); i++)
    result = result * 10 + charToDigit(tmpStr[i]);
  return result;
}

unordered_map <int, node> nodes;      // Mapping from nodeid to struct node
vector<int> adjList[NBNODES];         // Indexed by node id
vector<int> reversedAdjList[NBNODES];  // Indexed by node id
vector<int> tmpList[NBNODES];         // Indexed by node id

int main() {
  node tmpNode;
  string line;
  vector<string> arr1, arr2, arr3;
  int a, b;
  clock_t tStart = clock();


  // Read info of nodes
  ifstream nodefile("input/nodes.kmap");
  if (nodefile.is_open()) {
    getline(nodefile, line);
    while (getline(nodefile, line)) {
      arr1 = split(line, " ");
      int curNodeId = stringToNb(arr1[0]);
      tmpNode.existAt1 = true;
      tmpNode.existAt2 = true;
      tmpNode.existAt3 = true;
      if (arr1[1] == "0/0/0/0/0")
        tmpNode.existAt1 = false;
      if (arr1[2] == "0/0/0/0/0")
        tmpNode.existAt2 = false;
      if (arr1[3] == "0/0/0/0/0")
        tmpNode.existAt3 = false;
      nodes[curNodeId] = tmpNode;
    }
  }
  nodefile.close();
  cout << "Read info of all nodes\n";
  printf("Time taken: %.2fs\n", (double)(clock() - tStart)/CLOCKS_PER_SEC);


  // Read info of edges
  int edgeId = 0;
  ifstream edgefile("input/edges.kmap");
  if (edgefile.is_open()) {
    getline(edgefile, line);
    while (getline(edgefile, line)) {
      arr1 = split(line," ");
      arr2 = split(arr1[0], "/");
      a = stringToNb(arr2[0]);
      b = stringToNb(arr2[1]);
      adjList[a].push_back(b);
      reversedAdjList[b].push_back(a);
      tmpList[a].push_back(edgeId);
      edgeId++;
    }
  }
  edgefile.close();
  cout << "Read info of all edges\n";
  printf("Time taken: %.2fs\n", (double)(clock() - tStart)/CLOCKS_PER_SEC);


  // We will look at each node one-by-one
  ofstream output_egonet_second; output_egonet_second.open("output/egonet_second");
  ofstream output_egonet_third; output_egonet_third.open("output/egonet_third");
  ofstream output_second_first; output_second_first.open("output/pEgonet_second_first");
  ofstream output_third_second; output_third_second.open("output/pEgonet_third_second");
  ofstream output_third_first;  output_third_first.open("output/pEgonet_third_first");
  output_egonet_second << "NodeId EgonetNodes EgonetEdges\n";
  output_egonet_third  << "NodeId EgonetNodes EgonetEdges\n";
  output_second_first << "NodeId pEgonetNodes pEgonetEdges\n";
  output_third_second << "NodeId pEgonetNodes pEgonetEdges\n";
  output_third_first  << "NodeId pEgonetNodes pEgonetEdges\n";

  unordered_map <int, bool> isInNeighborSet;
  vector<int> pEgonetNodes;
  vector<int> pEgonetEdges;
  for (int i = 0; i < NBNODES; i++) {
    // Look at node with id i
    isInNeighborSet.clear();
    isInNeighborSet[i] = true;
    for (int j = 0; j < adjList[i].size(); j++)
      isInNeighborSet[adjList[i][j]] = true;
    for (int j = 0; j < reversedAdjList[i].size(); j++)
      isInNeighborSet[reversedAdjList[i][j]] = true;

    if (!nodes[i].existAt1 && nodes[i].existAt2) {
      // This is a new node at second timeslot

      // Update the file output_egonet_second
      pEgonetNodes.clear(); pEgonetEdges.clear();
      for(unordered_map<int,bool>::iterator it = isInNeighborSet.begin(); it != isInNeighborSet.end(); ++it) {
        int v = (it->first);
        if (nodes[v].existAt2) {
          pEgonetNodes.push_back(v);
          for (int j = 0; j < adjList[v].size(); j++)
            if (isInNeighborSet.find(adjList[v][j]) != isInNeighborSet.end())
              if (nodes[adjList[v][j]].existAt2)
                pEgonetEdges.push_back(tmpList[v][j]);
        }
      }
      output_egonet_second << i << " [";
      for (int j = 0; j < pEgonetNodes.size(); j++) {
        output_egonet_second << pEgonetNodes[j];
        if (j != pEgonetNodes.size() - 1)
          output_egonet_second << ",";
      }
      output_egonet_second << "] [";
      for (int j = 0; j < pEgonetEdges.size(); j++) {
        output_egonet_second << pEgonetEdges[j];
        if (j != pEgonetEdges.size() - 1)
          output_egonet_second << ",";
      }
      output_egonet_second << "]\n";

      // Update the file pEgonet_second_first
      pEgonetNodes.clear(); pEgonetEdges.clear();
      for(unordered_map<int,bool>::iterator it = isInNeighborSet.begin(); it != isInNeighborSet.end(); ++it) {
        int v = (it->first);
        if (nodes[v].existAt1) {
          pEgonetNodes.push_back(v);
          for (int j = 0; j < adjList[v].size(); j++)
            if (isInNeighborSet.find(adjList[v][j]) != isInNeighborSet.end())
              if (nodes[adjList[v][j]].existAt1)
                pEgonetEdges.push_back(tmpList[v][j]);
        }
      }
      output_second_first << i << " [";
      for (int j = 0; j < pEgonetNodes.size(); j++) {
        output_second_first << pEgonetNodes[j];
        if (j != pEgonetNodes.size() - 1)
          output_second_first << ",";
      }
      output_second_first << "] [";
      for (int j = 0; j < pEgonetEdges.size(); j++) {
        output_second_first << pEgonetEdges[j];
        if (j != pEgonetEdges.size() - 1)
          output_second_first << ",";
      }
      output_second_first << "]\n";

    }
    else if (!nodes[i].existAt2 && nodes[i].existAt3) {
      // This is a new node at third timeslot

      // Update the output file egonet_third
      pEgonetNodes.clear(); pEgonetEdges.clear();
      for(unordered_map<int,bool>::iterator it = isInNeighborSet.begin(); it != isInNeighborSet.end(); ++it) {
        int v = (it->first);
        if (nodes[v].existAt3) {
          pEgonetNodes.push_back(v);
          for (int j = 0; j < adjList[v].size(); j++)
            if (isInNeighborSet.find(adjList[v][j]) != isInNeighborSet.end())
              if (nodes[adjList[v][j]].existAt3)
                pEgonetEdges.push_back(tmpList[v][j]);
        }
      }
      output_egonet_third << i << " [";
      for (int j = 0; j < pEgonetNodes.size(); j++) {
        output_egonet_third << pEgonetNodes[j];
        if (j != pEgonetNodes.size() - 1)
          output_egonet_third << ",";
      }
      output_egonet_third << "] [";
      for (int j = 0; j < pEgonetEdges.size(); j++) {
        output_egonet_third << pEgonetEdges[j];
        if (j != pEgonetEdges.size() - 1)
          output_egonet_third << ",";
      }
      output_egonet_third << "]\n";

      // Update the file pEgonet_third_first
      pEgonetNodes.clear(); pEgonetEdges.clear();
      for(unordered_map<int,bool>::iterator it = isInNeighborSet.begin(); it != isInNeighborSet.end(); ++it) {
        int v = (it->first);
        if (nodes[v].existAt1) {
          pEgonetNodes.push_back(v);
          for (int j = 0; j < adjList[v].size(); j++)
            if (isInNeighborSet.find(adjList[v][j]) != isInNeighborSet.end())
              if (nodes[adjList[v][j]].existAt1)
                pEgonetEdges.push_back(tmpList[v][j]);
        }
      }
      output_third_first << i << " [";
      for (int j = 0; j < pEgonetNodes.size(); j++) {
        output_third_first << pEgonetNodes[j];
        if (j != pEgonetNodes.size() - 1)
          output_third_first << ",";
      }
      output_third_first << "] [";
      for (int j = 0; j < pEgonetEdges.size(); j++) {
        output_third_first << pEgonetEdges[j];
        if (j != pEgonetEdges.size() - 1)
          output_third_first << ",";
      }
      output_third_first << "]\n";


      // Update the file pEgonet_third_second
      pEgonetNodes.clear(); pEgonetEdges.clear();
      for(unordered_map<int,bool>::iterator it = isInNeighborSet.begin(); it != isInNeighborSet.end(); ++it) {
        int v = (it->first);
        if (nodes[v].existAt2) {
          pEgonetNodes.push_back(v);
          for (int j = 0; j < adjList[v].size(); j++)
            if (isInNeighborSet.find(adjList[v][j]) != isInNeighborSet.end())
              if (nodes[adjList[v][j]].existAt2)
                pEgonetEdges.push_back(tmpList[v][j]);
        }
      }
      output_third_second << i << " [";
      for (int j = 0; j < pEgonetNodes.size(); j++) {
        output_third_second << pEgonetNodes[j];
        if (j != pEgonetNodes.size() - 1)
          output_third_second << ",";
      }
      output_third_second << "] [";
      for (int j = 0; j < pEgonetEdges.size(); j++) {
        output_third_second << pEgonetEdges[j];
        if (j != pEgonetEdges.size() - 1)
          output_third_second << ",";
      }
      output_third_second << "]\n";
    }
  }
  output_second_first.close();
  output_third_second.close();
  output_third_first.close();
  output_egonet_second.close();
  output_egonet_third.close();
  cout << "Finished everything\n";
  printf("Time taken: %.2fs\n", (double)(clock() - tStart)/CLOCKS_PER_SEC);

}
