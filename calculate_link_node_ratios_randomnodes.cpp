#include <iostream>
#include <fstream>
#include <string>
#include <time.h>
#include <vector>
#include <string.h>
#include <utility>      // std::pair, std::make_pair
#include <map>
#include <iostream>
#include <cstdlib>      // std::rand, std::srand
#include <set>
#define NBNODES 971427
#define ui unsigned int
using namespace std;

map < pair<int, int>, bool > isEdge;
vector <int> nodesExistAt1;
vector <int> nodesExistAt2;

int nbNodes = 0;
int nbEdges = 0;

vector<int> randomsampling(vector <int>, int);
vector<string> split(string,string);
ui charToDigit (char);
ui stringToNb (string);

double max (double a, double b) {
  return a > b ? a : b;
}

int main() {
  srand(time(0));

  bool firstLine;
  vector<string> arr1, arr2, arr3;
  string line, inputfilename, outputfilename;
  int tmpSrc, tmpDest;
  pair <int, int> tmpPair;
  clock_t tStart = clock();

  firstLine = true;
  ifstream mynodefile ("input/nodes.kmap");
  if (mynodefile.is_open()) {
    while (getline(mynodefile, line)) {
      if (firstLine)
        firstLine = false;
      else {
        nbNodes ++;
        arr1 = split(line, " ");
        int tmpnodeid = stringToNb(arr1[0]);
        if (arr1[1] != "0/0/0/0/0")
          nodesExistAt1.push_back(tmpnodeid);
        if (arr1[2] != "0/0/0/0/0")
          nodesExistAt2.push_back(tmpnodeid);
      }
    }
    mynodefile.close();
  }
  printf("Read the info of all nodes\n");
  printf("Time taken: %.2fs\n", (double)(clock() - tStart)/CLOCKS_PER_SEC);


  firstLine = true;
  ifstream myedgefile ("input/edges.kmap");
  if (myedgefile.is_open()) {
    while ( getline (myedgefile,line) ) {
      if (firstLine)
        firstLine = false;
      else {
        nbEdges++;
        if (nbEdges % 1000000 == 0)
          cout << "nbEdges = " << nbEdges << "\n";

        arr1 = split(line," ");
        arr2 = split(arr1[0], "/");
        tmpSrc = stringToNb(arr2[0]);
        tmpDest = stringToNb(arr2[1]);
        tmpPair.first = tmpSrc;
        tmpPair.second = tmpDest;
        isEdge[tmpPair] = true;
      }
    }
    myedgefile.close();
  }
  printf("Read the info of all edges\n");
  printf("Time taken: %.2fs\n", (double)(clock() - tStart)/CLOCKS_PER_SEC);

  for (int choice = 1; choice < 4; choice++) {
    cout << "Currently, choice = " << choice << "\n";
    if (choice == 1) {
        inputfilename = "pegonet_avgratios_second_first.csv";
        outputfilename = "randomnodes_avgratios_second_first.csv";
    }
    else if (choice == 2) {
        inputfilename = "pegonet_avgratios_third_first.csv";
        outputfilename = "randomnodes_avgratios_third_first.csv";
    }
    else if (choice == 3) {
        inputfilename = "pegonet_avgratios_third_second.csv";
        outputfilename = "randomnodes_avgratios_third_second.csv";
    }
    inputfilename = "link_node_ratio_output/" + inputfilename;
    outputfilename = "link_node_ratio_output/" + outputfilename;

    firstLine = true;
    vector <int> nbnodes_list;
    ifstream myinputfile (inputfilename.c_str());
    if (myinputfile.is_open()) {
      while (getline(myinputfile, line)) {
        if (firstLine)
          firstLine = false;
        else {
          arr1 = split(line, ",");
          int tmpnbnodes = stringToNb(arr1[0]);
          nbnodes_list.push_back(tmpnbnodes);
        }
      }
      myinputfile.close();
    }


    vector <double> rslists;
    vector <double> maxrslists;
    for (int i = 0; i < nbnodes_list.size(); i++) {
      maxrslists.push_back(0);
      float curnbnode = nbnodes_list[i];
      double rsratio = 0;
      int nbstimulations = 10;
      for (int j = 0; j < nbstimulations; j++) {
        double edgecounts = 0;
        vector <int> rand_smpl;
        if (choice < 3)
          rand_smpl = randomsampling(nodesExistAt1, (int) curnbnode);
        else
          rand_smpl = randomsampling(nodesExistAt2, (int) curnbnode);

        for (int z1 = 0; z1 < rand_smpl.size(); z1++)
          for (int z2 = 0; z2 < rand_smpl.size(); z2++)
            if (z1 != z2) {
              tmpPair.first = rand_smpl[z1];
              tmpPair.second = rand_smpl[z2];
              if (isEdge.find(tmpPair) != isEdge.end())
                edgecounts += 1;
            }
        double tmpincr = 0;
        if (curnbnode > 0)
          tmpincr = edgecounts/curnbnode;
        rsratio += tmpincr;
        maxrslists[maxrslists.size()-1] = max(maxrslists[maxrslists.size()-1], tmpincr);
      }
      rsratio = rsratio / nbstimulations;
      rslists.push_back(rsratio);
    }

    ofstream myoutputfile;
    myoutputfile.open (outputfilename.c_str());
    myoutputfile << "nbNodesInPegonet,avgRatios,maxRatio\n";
    for (int zz = 0; zz < nbnodes_list.size(); zz++) {
      myoutputfile << nbnodes_list[zz] << "," << rslists[zz] << "," << maxrslists[zz] << "\n";
    }
    myoutputfile.close();

    printf("Time taken: %.2fs\n", (double)(clock() - tStart)/CLOCKS_PER_SEC);
  }


}


vector<int> randomsampling(vector <int> my_vector, int n) {
  set<int> indexes;
  vector <int> choices;
  int max_index = my_vector.size();
  while (indexes.size() < min(n, max_index))
  {
    int random_index = rand() % max_index;
    if (indexes.find(random_index) == indexes.end())
    {
        choices.push_back(my_vector[random_index]);
        indexes.insert(random_index);
    }
  }
  return choices;
}

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
