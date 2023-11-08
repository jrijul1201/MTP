#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <fstream>
#include <ctime>
#include <sstream>
#include <sys/stat.h>
#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
#include "ns3/traffic-control-module.h"
#include "ns3/flow-monitor-module.h"

using namespace ns3;

class P2PRouter
{
  // private:
public:
  Time linkDelay;
  DataRate linkBandwidth;
  uint32_t prevBytes;
  Time prevTime;
  std::string qdiscTypeId;
  std::string dir;
  QueueSize queueSize;
  TypeId qdTid;
  uint32_t rtt;

  NodeContainer routers;
  // Create the point-to-point link helpers and connect two router nodes
  PointToPointHelper pointToPointRouter;
  NetDeviceContainer netDevice;
  QueueDiscContainer qd;
  TrafficControlHelper tch;

  // Constructor
  P2PRouter (uint32_t rtt, std::string dir, QueueSize queueSize = QueueSize ("2084p"),
             DataRate linkBandwidth = DataRate ("100Mbps"),
             std::string qdiscTypeId = "ns3::FifoQueueDisc")
  {
    this->linkBandwidth = linkBandwidth;
    this->linkDelay = MilliSeconds (rtt * 0.01);
    this->dir = dir;
    this->rtt = rtt;
    this->qdiscTypeId = qdiscTypeId;
    this->queueSize = queueSize;
    this->prevBytes = 0;
    this->prevTime = Seconds (0);
    
    uint32_t retVal = -1;
    retVal = system (("mkdir -p " + dir).c_str ());
    NS_ASSERT_MSG (retVal == 0, "Error in return value");

    NS_ABORT_MSG_UNLESS (TypeId::LookupByNameFailSafe (qdiscTypeId, &qdTid),
                         "TypeId " << qdiscTypeId << " not found");
    routers.Create (2);

    pointToPointRouter.SetDeviceAttribute ("DataRate", DataRateValue (linkBandwidth));
    pointToPointRouter.SetChannelAttribute ("Delay", TimeValue (linkDelay));
    netDevice = pointToPointRouter.Install (routers.Get (0), routers.Get (1));
    pointToPointRouter.DisableFlowControl ();
    std::string dirToSave = "mkdir -p " + dir;
  }

  void
  installQueueDiscipline ()
  {
    // Set default parameters for queue discipline
    Config::SetDefault (qdiscTypeId + "::MaxSize", QueueSizeValue (queueSize));

    // Install queue discipline on router
    tch.SetRootQueueDisc (qdiscTypeId);
    tch.Uninstall (routers.Get (0)->GetDevice (0));
    qd.Add (tch.Install (routers.Get (0)->GetDevice (0)).Get (0));

    // Enable BQL
    tch.SetQueueLimits ("ns3::DynamicQueueLimits");
  }
};
