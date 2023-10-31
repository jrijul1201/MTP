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
private:
  Time linkDelay;
  DataRate linkBandwidth;
  uint32_t prevBytes;
  uint32_t currBytes;
  Time prevTime;
  uint32_t stream;
  std::string socketFactory;
  std::string qdiscTypeId;
  std::string dir;
  QueueSize queueSize;
  TypeId qdTid;
  uint32_t rtt;
  std::string tcpType;

public:
  NodeContainer routers;
  // Create the point-to-point link helpers and connect two router nodes
  PointToPointHelper pointToPointRouter;
  NetDeviceContainer r1r2ND;
  QueueDiscContainer qd;
  TrafficControlHelper tch;

  // Constructor
  P2PRouter (uint32_t rtt, std::string dir, DataRate linkBandwidth = DataRate ("100Mbps"),
             uint32_t prevBytes = 0, uint32_t currBytes = 0, Time prevTime = Seconds (0),
             uint32_t stream = 1, std::string socketFactory = "ns3::TcpSocketFactory",
             std::string qdiscTypeId = "ns3::FifoQueueDisc",
             QueueSize queueSize = QueueSize ("2084p"), std::string tcpType = "TcpNewReno")
  {
    linkBandwidth = linkBandwidth;
    linkDelay = MilliSeconds (rtt * 0.01);
    stream = stream;
    dir = dir;
    rtt = rtt;
    socketFactory = socketFactory;
    qdiscTypeId = qdiscTypeId;
    queueSize = queueSize;
    prevBytes = prevBytes;
    currBytes = currBytes;
    prevTime = prevTime;
    tcpType = tcpType;
    NS_ABORT_MSG_UNLESS (TypeId::LookupByNameFailSafe (qdiscTypeId, &qdTid),
                         "TypeId " << qdiscTypeId << " not found");
    routers.Create (2);

    pointToPointRouter.SetDeviceAttribute ("DataRate", DataRateValue (linkBandwidth));
    pointToPointRouter.SetChannelAttribute ("Delay", TimeValue (linkDelay));
    r1r2ND = pointToPointRouter.Install (routers.Get (0), routers.Get (1));
    pointToPointRouter.DisableFlowControl ();

    // Set default parameters for queue discipline
    Config::SetDefault (qdiscTypeId + "::MaxSize", QueueSizeValue (queueSize));

    // Install queue discipline on router
    tch.SetRootQueueDisc (qdiscTypeId);
    tch.Uninstall (routers.Get (0)->GetDevice (0));
    qd.Add (tch.Install (routers.Get (0)->GetDevice (0)).Get (0));

    // Enable BQL
    tch.SetQueueLimits ("ns3::DynamicQueueLimits");
  }

  // Function to check queue length of Router 1
  void
  CheckQueueSize (Ptr<QueueDisc> queue, std::string dir)
  {
    uint32_t qSize = queue->GetCurrentSize ().GetValue ();

    // Check queue size every 1/5 of a second
    Simulator::Schedule (Seconds (0.2), &P2PRouter::CheckQueueSize, queue, dir);
    std::ofstream fPlotQueue (std::stringstream (dir + "queue-size.dat").str ().c_str (),
                              std::ios::out | std::ios::app);
    fPlotQueue << Simulator::Now ().GetSeconds () << " " << qSize << std::endl;
    fPlotQueue.close ();
  }

  // Calculate throughput and link utilisation
  void
  TraceThroughputAndLU (Ptr<FlowMonitor> monitor, Ptr<Ipv4FlowClassifier> classifier)
  {
    FlowMonitor::FlowStatsContainer stats = monitor->GetFlowStats ();
    Time currTime = Now ();

    currBytes = 0;
    auto count = stats.size () / 2;
    // aggregate rxBytes for first half flows (going towards sink):
    for (auto itr = stats.begin (); count > 0; ++itr, --count)
      {
        Ipv4FlowClassifier::FiveTuple t = classifier->FindFlow (itr->first);
        // std::cout << "Flow " << itr->first << " (" << t.sourceAddress << " -> "
        //           << t.destinationAddress << ")\n";
        currBytes += itr->second.rxBytes;
      }

    // Throughput is in MegaBits/Second
    double throughput = 8 * (currBytes - prevBytes) /
                        (1000 * 1000 * (currTime.GetSeconds () - prevTime.GetSeconds ()));
    double link_util = (throughput * 1000 * 1000 * 100 / linkBandwidth.GetBitRate ());

    std::ofstream thr (dir + "/throughput.dat", std::ios::out | std::ios::app);
    std::ofstream lu (dir + "/linkUtilization.dat", std::ios::out | std::ios::app);
    thr << currTime.GetSeconds () << " " << throughput << std::endl;
    lu << currTime.GetSeconds () << " " << link_util << std::endl;

    prevTime = currTime;
    prevBytes = currBytes;

    Simulator::Schedule (Seconds (0.001 * rtt), &P2PRouter::TraceThroughputAndLU, monitor,
                         classifier);
  }
};
