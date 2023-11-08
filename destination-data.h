#include <ctime>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <fstream>
#include <ctime>
#include <sstream>
#include <sys/stat.h>
#include "ns3/core-module.h"

using namespace ns3;

class DestinationData
{
public:
  uint32_t prevBytes;
  Time prevTime;
  uint32_t groupID;
  uint32_t destinationID;
  std::string throughput_file;

  DestinationData (uint32_t groupID, uint32_t destinationID, std::string dir)
  {
    this->prevBytes = 0;
    this->prevTime = Seconds (0);
    this->groupID = groupID;
    this->destinationID = destinationID;
    this->throughput_file = dir + "/throughput/throughput" + std::to_string (groupID) + "_" +
                            std::to_string (destinationID) + ".dat";
  }
};