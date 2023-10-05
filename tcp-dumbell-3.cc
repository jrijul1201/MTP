/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */

// Network topology
//
//       n0 ---------- n1 ---------- n2 ---------- n3
//            10 Mbps       1 Mbps        10 Mbps
//             1 ms         10 ms          1 ms
//
// - TCP flow from n0 to n3 using BulkSendApplication.
// - The following simulation output is stored in results/ in ns-3 top-level directory:
//   - cwnd traces are stored in cwndTraces folder
//   - queue length statistics are stored in queue-size.dat file
//   - pcaps are stored in pcap folder
//   - queueTraces folder contain the drop statistics at queue
//   - queueStats.txt file contains the queue stats and config.txt file contains
//     the simulation configuration.
// - The cwnd and queue length traces obtained from this example were tested against
//   the respective traces obtained from Linux Reno by using ns-3 Direct Code Execution.
//   See internet/doc/tcp.rst for more details.

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
std::string dir = "results/";
Time stopTime = Seconds (200);
Time tracingDuration = Seconds (25);
Time tracingStartTime = stopTime - tracingDuration;
uint32_t segmentSize = 1500;
uint32_t numNodes = 60;
uint32_t prevBytes = 0;
uint32_t currBytes = 0;
Time prevTime = Seconds (0);
DataRate bottleneckBandwidth;
uint32_t rtt = 100;
std::string tcpType = "TcpNewReno";

static uint32_t
GetNodeIdFromContext (std::string context)
{
  std::size_t const n1 = context.find_first_of ("/", 1);
  std::size_t const n2 = context.find_first_of ("/", n1 + 1);
  return std::stoul (context.substr (n1 + 1, n2 - n1 - 1));
}

// Function to check queue length of Router 1
void
CheckQueueSize (Ptr<QueueDisc> queue)
{
  uint32_t qSize = queue->GetCurrentSize ().GetValue ();

  // Check queue size every 1/5 of a second
  Simulator::Schedule (Seconds (0.2), &CheckQueueSize, queue);
  std::ofstream fPlotQueue (std::stringstream (dir + "queue-size.dat").str ().c_str (),
                            std::ios::out | std::ios::app);
  fPlotQueue << Simulator::Now ().GetSeconds () << " " << qSize << std::endl;
  fPlotQueue.close ();
}

// Function to trace change in cwnd at n0
static void
CwndChange (std::string context, uint32_t oldCwnd, uint32_t newCwnd)
{
  uint32_t nodeId = GetNodeIdFromContext (context);
  std::string s = std::to_string (nodeId);
  std::ofstream fPlotQueue (dir + "cwndTraces/n" + s + ".dat", std::ios::out | std::ios::app);
  fPlotQueue << Simulator::Now ().GetSeconds () << " " << newCwnd / segmentSize << std::endl;
  fPlotQueue.close ();
}

// Function to calculate drops in a particular Queue
static void
DropAtQueue (Ptr<OutputStreamWrapper> stream, Ptr<const QueueDiscItem> item)
{
  *stream->GetStream () << Simulator::Now ().GetSeconds () << " 1" << std::endl;
}

// Trace Function for cwnd
void
TraceCwnd (uint32_t node, uint32_t cwndWindow,
           Callback<void, std::string, uint32_t, uint32_t> CwndTrace)
{
  Config::Connect ("/NodeList/" + std::to_string (node) + "/$ns3::TcpL4Protocol/SocketList/" +
                       std::to_string (cwndWindow) + "/CongestionWindow",
                   CwndTrace);
}

// Function to install BulkSend application
void
InstallBulkSend (Ptr<Node> node, Ipv4Address address, uint16_t port, std::string socketFactory,
                 uint32_t nodeId, uint32_t cwndWindow,
                 Callback<void, std::string, uint32_t, uint32_t> CwndTrace)
{
  BulkSendHelper source (socketFactory, InetSocketAddress (address, port));
  source.SetAttribute ("MaxBytes", UintegerValue (0));
  ApplicationContainer sourceApps = source.Install (node);
  sourceApps.Start (Seconds (0.0));
  Simulator::Schedule (tracingStartTime, &TraceCwnd, nodeId, cwndWindow, CwndTrace);
  sourceApps.Stop (stopTime);
}

// Function to install sink application
void
InstallPacketSink (Ptr<Node> node, uint16_t port, std::string socketFactory)
{
  PacketSinkHelper sink (socketFactory, InetSocketAddress (Ipv4Address::GetAny (), port));
  ApplicationContainer sinkApps = sink.Install (node);
  sinkApps.Start (Seconds (0.0));
  sinkApps.Stop (stopTime);
}

// Function to calculate variable access link delay
Time *
variedAccessLinkDelays (int numNodes, int mean)
{
  Time *delays = (Time *) malloc (numNodes * sizeof (Time));

  int sum = 0, x;
  for (int i = 0; i < numNodes - 1; i++)
    {
      x = rand () % mean + 1;
      sum += x;
      delays[i] = MilliSeconds (x);
    }

  x = mean * numNodes - sum;
  delays[numNodes - 1] = MilliSeconds (x);

  return delays;
}

// Calculate throughput and link utilisation
static void
TraceThroughputAndLU (Ptr<FlowMonitor> monitor)
{
  FlowMonitor::FlowStatsContainer stats = monitor->GetFlowStats ();
  Time currTime = Now ();

  currBytes = 0;
  auto count = stats.size () / 2;
  // aggregate txBytes for first half flows (going towards sink):
  for (auto itr = stats.begin (); count > 0; ++itr, --count)
    {
      currBytes += itr->second.txBytes;
    }

  // Throughput is in MegaBits/Second
  double throughput = 8 * (currBytes - prevBytes) /
                      (1000 * 1000 * (currTime.GetSeconds () - prevTime.GetSeconds ()));
  double link_util = (throughput * 1000 * 1000 * 100 / bottleneckBandwidth.GetBitRate ());

  std::ofstream thr (dir + "/throughput.dat", std::ios::out | std::ios::app);
  std::ofstream lu (dir + "/linkUtilization.dat", std::ios::out | std::ios::app);
  thr << currTime.GetSeconds () << " " << throughput << std::endl;
  lu << currTime.GetSeconds () << " " << link_util << std::endl;

  prevTime = currTime;
  prevBytes = currBytes;

  Simulator::Schedule (Seconds (0.2), &TraceThroughputAndLU, monitor);
}

int
main (int argc, char *argv[])
{
  time_t now = time (0);
  std::stringstream ss;
  ss << now;
  std::string ts = ss.str ();

  uint32_t stream = 1;
  std::string socketFactory = "ns3::TcpSocketFactory";
  std::string qdiscTypeId = "ns3::FifoQueueDisc";
  bool isSack = true;
  uint32_t delAckCount = 1;
  std::string recovery = "ns3::TcpClassicRecovery";
  QueueSize queueSize = QueueSize ("2084p");

  CommandLine cmd;
  cmd.AddValue ("qdiscTypeId", "Queue disc for gateway (e.g., ns3::CoDelQueueDisc)", qdiscTypeId);
  cmd.AddValue ("segmentSize", "TCP segment size (bytes)", segmentSize);
  cmd.AddValue ("delAckCount", "Delayed ack count", delAckCount);
  cmd.AddValue ("enableSack", "Flag to enable/disable sack in TCP", isSack);
  cmd.AddValue ("numNodes", "Number of nodes in the sender", numNodes);
  cmd.AddValue ("roundTripTime", "Round trip time of a network packet", rtt);
  cmd.AddValue ("tcpVariant", "Type of tcp varient you want to use", tcpType);
  cmd.AddValue ("stopTime", "Stop time for applications / simulation time will be stopTime",
                stopTime);
  cmd.AddValue ("recovery", "Recovery algorithm type to use (e.g., ns3::TcpPrrRecovery", recovery);
  cmd.Parse (argc, argv);

  dir += std::to_string (numNodes) + "-" + tcpType + "-" + std::to_string (rtt) + "/";

  bottleneckBandwidth = DataRate ("100Mbps"); // 100Mbps for actual sims
  Time bottleneckDelay = MilliSeconds (rtt * 0.01);
  DataRate accessLinkBandwidth = DataRate ((1.2 * bottleneckBandwidth.GetBitRate ()) / numNodes);
  // 100 - 1 - 1 divided by 4
  Time *accessLinkDelays = variedAccessLinkDelays (numNodes, (rtt * 0.24));

  TypeId qdTid;
  NS_ABORT_MSG_UNLESS (TypeId::LookupByNameFailSafe (qdiscTypeId, &qdTid),
                       "TypeId " << qdiscTypeId << " not found");

  // Set recovery algorithm and TCP variant
  Config::SetDefault ("ns3::TcpL4Protocol::RecoveryType",
                      TypeIdValue (TypeId::LookupByName (recovery)));

  // Create nodes
  NodeContainer leftNodes, rightNodes, routers;
  routers.Create (2);
  leftNodes.Create (numNodes);
  rightNodes.Create (numNodes);

  std::vector<NetDeviceContainer> leftToRouter;
  std::vector<NetDeviceContainer> routerToRight;

  // Create the point-to-point link helpers and connect two router nodes
  PointToPointHelper pointToPointRouter;
  pointToPointRouter.SetDeviceAttribute ("DataRate", DataRateValue (bottleneckBandwidth));
  pointToPointRouter.SetChannelAttribute ("Delay", TimeValue (bottleneckDelay));
  NetDeviceContainer r1r2ND = pointToPointRouter.Install (routers.Get (0), routers.Get (1));
  pointToPointRouter.DisableFlowControl ();

  // Create the point-to-point link helpers and connect leaf nodes to router
  PointToPointHelper pointToPointLeaf;
  pointToPointLeaf.DisableFlowControl ();
  pointToPointLeaf.SetDeviceAttribute ("DataRate", DataRateValue (accessLinkBandwidth));
  pointToPointLeaf.DisableFlowControl ();
  for (uint32_t i = 0; i < numNodes; ++i)
    {
      pointToPointLeaf.SetChannelAttribute ("Delay", TimeValue (accessLinkDelays[i]));
      leftToRouter.push_back (pointToPointLeaf.Install (leftNodes.Get (i), routers.Get (0)));
      routerToRight.push_back (pointToPointLeaf.Install (routers.Get (1), rightNodes.Get (i)));
    }

  InternetStackHelper internetStack;

  internetStack.Install (leftNodes);
  internetStack.Install (rightNodes);
  internetStack.Install (routers);

  // Assign IP addresses to all the network devices
  // TODO: For N > 3.2k, change bitmask to accomodate larger network
  Ipv4AddressHelper ipAddresses ("10.0.0.0", "255.255.0.0");

  Ipv4InterfaceContainer r1r2IPAddress = ipAddresses.Assign (r1r2ND);
  ipAddresses.NewNetwork ();

  std::vector<Ipv4InterfaceContainer> leftToRouterIPAddress;
  for (uint32_t i = 0; i < numNodes; i++)
    {
      leftToRouterIPAddress.push_back (ipAddresses.Assign (leftToRouter[i]));
      ipAddresses.NewNetwork ();
    }

  std::vector<Ipv4InterfaceContainer> routerToRightIPAddress;
  for (uint32_t i = 0; i < numNodes; i++)
    {
      routerToRightIPAddress.push_back (ipAddresses.Assign (routerToRight[i]));
      ipAddresses.NewNetwork ();
    }

  Ipv4GlobalRoutingHelper::PopulateRoutingTables ();
  Config::SetDefault ("ns3::TcpL4Protocol::SocketType", StringValue ("ns3::" + tcpType));

  // Set default sender and receiver buffer size as 1MB
  Config::SetDefault ("ns3::TcpSocket::SndBufSize", UintegerValue (1 << 27));
  // Receive buffer size is 1GB to allow for sufficiently large receiving window
  Config::SetDefault ("ns3::TcpSocket::RcvBufSize", UintegerValue (1 << 30));

  // Set default initial congestion window as 10 segments
  Config::SetDefault ("ns3::TcpSocket::InitialCwnd", UintegerValue (10));

  // Set default delayed ack count to a specified value
  Config::SetDefault ("ns3::TcpSocket::DelAckCount", UintegerValue (delAckCount));

  // Set default segment size of TCP packet to a specified value
  Config::SetDefault ("ns3::TcpSocket::SegmentSize", UintegerValue (segmentSize));

  // Enable/Disable SACK in TCP
  // Config::SetDefault ("ns3::TcpSocketBase::Sack", BooleanValue (isSack));

  // Create directories to store dat files
  struct stat buffer;
  [[maybe_unused]] int retVal;
  if ((stat (dir.c_str (), &buffer)) == 0)
    {
      std::string dirToRemove = "rm -rf " + dir;
      retVal = system (dirToRemove.c_str ());
      NS_ASSERT_MSG (retVal == 0, "Error in return value");
    }
  std::string dirToSave = "mkdir -p " + dir;
  retVal = system (dirToSave.c_str ());
  NS_ASSERT_MSG (retVal == 0, "Error in return value");
  // retVal = system ((dirToSave + "/pcap/").c_str ());
  // NS_ASSERT_MSG (retVal == 0, "Error in return value");
  retVal = system ((dirToSave + "/queueTraces/").c_str ());
  NS_ASSERT_MSG (retVal == 0, "Error in return value");
  retVal = system ((dirToSave + "/cwndTraces/").c_str ());
  NS_ASSERT_MSG (retVal == 0, "Error in return value");

  // Set default parameters for queue discipline
  Config::SetDefault (qdiscTypeId + "::MaxSize", QueueSizeValue (queueSize));

  // Install queue discipline on router
  TrafficControlHelper tch;
  tch.SetRootQueueDisc (qdiscTypeId);
  QueueDiscContainer qd;
  tch.Uninstall (routers.Get (0)->GetDevice (0));
  qd.Add (tch.Install (routers.Get (0)->GetDevice (0)).Get (0));

  // Enable BQL
  tch.SetQueueLimits ("ns3::DynamicQueueLimits");

  // Calls function to check queue size
  Simulator::Schedule (tracingStartTime, &CheckQueueSize, qd.Get (0));

  AsciiTraceHelper asciiTraceHelper;
  Ptr<OutputStreamWrapper> streamWrapper;

  // Create dat to store packets dropped and marked at the router
  streamWrapper = asciiTraceHelper.CreateFileStream (dir + "/queueTraces/drop-0.dat");
  qd.Get (0)->TraceConnectWithoutContext ("Drop", MakeBoundCallback (&DropAtQueue, streamWrapper));

  // Install packet sink at receiver side for N nodes
  uint16_t port = 50000;
  for (uint32_t i = 0; i < numNodes; i++)
    {
      InstallPacketSink (rightNodes.Get (i), port, "ns3::TcpSocketFactory");
    }
  // Install BulkSend application for N nodes
  for (uint32_t i = 0; i < numNodes; i++)
    {
      // NodeId 0 and 1 are assigned to routers, hence (2 + i) will be the nodeId
      InstallBulkSend (leftNodes.Get (i), routerToRightIPAddress[i].GetAddress (1), port,
                       socketFactory, 2 + i, 0, MakeCallback (&CwndChange));
    }
  // Enable PCAP on all the point to point interfaces
  // pointToPointLeaf.EnablePcapAll (dir + "pcap/ns-3", true);

  // Check for dropped packets using Flow Monitor
  FlowMonitorHelper flowmon;
  Ptr<FlowMonitor> monitor = flowmon.InstallAll ();
  Simulator::Schedule (tracingStartTime, &TraceThroughputAndLU, monitor);

  Simulator::Stop (stopTime);
  Simulator::Run ();

  // Store queue stats in a file
  std::ofstream myfile;
  myfile.open (dir + "queueStats.txt", std::fstream::in | std::fstream::out | std::fstream::app);
  myfile << std::endl;
  myfile << "Stat for Queue 1";
  myfile << qd.Get (0)->GetStats ();
  myfile.close ();

  // Store configuration of the simulation in a file
  myfile.open (dir + "config.txt", std::fstream::in | std::fstream::out | std::fstream::app);
  myfile << "qdiscTypeId " << qdiscTypeId << "\n";
  myfile << "stream  " << stream << "\n";
  myfile << "segmentSize " << segmentSize << "\n";
  myfile << "delAckCount " << delAckCount << "\n";
  myfile << "stopTime " << stopTime.As (Time::S) << "\n";
  myfile.close ();

  Simulator::Destroy ();

  return 0;
}