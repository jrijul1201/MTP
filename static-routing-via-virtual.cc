/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */

// Parking Lot Topology: https://arxiv.org/pdf/1907.06302.pdf

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
#include "network.h"

using namespace ns3;

std::string dir = "examples/results/static-routing-via-virtual/";
Time stopTime = Seconds (200);
Time tracingDuration = Seconds (25);
Time tracingStartTime = stopTime - tracingDuration;
uint32_t segmentSize = 1500;
uint32_t numNodes = 146;
uint32_t rtt = 100;
std::string tcpType = "TcpNewReno";
bool isThresholdAQMEnabled = false;
uint32_t stream = 1;
std::string socketFactory = "ns3::TcpSocketFactory";
std::string qdiscTypeId = "ns3::FifoQueueDisc";
uint32_t delAckCount = 1;
std::string recovery = "ns3::TcpClassicRecovery";
QueueSize queueSize = QueueSize ("2084p");
uint32_t groups = 3; // Number of sources and destinations groups
DataRate bottleneckBandwidth = DataRate ("100Mbps"); // 100Mbps for actual sims
DataRate accessLinkBandwidth = DataRate ((1.2 * bottleneckBandwidth.GetBitRate ()) / 60);
Time minimumLinkDelay = MicroSeconds (1);
Time *accessLinkDelays;
std::ofstream myfile;
std::map<Ipv4Address, DestinationData *> IPtoDestinationData;
std::vector<double> throughputPerGroup;
uint32_t numNodesInGroup;
uint32_t numRouters = 6;
std::vector<int> realSourcesForRouters = {60, 0, 0, 0, 0, 0};
std::vector<int> realDestinationsForRouters = {0, 5, 32, 5, 4, 14};
std::vector<int> virtualsForRouters = {0, 0, 0, 28, 23, 35};
std::vector<int> srcToRouterMapping;
std::vector<int> desToRouterMapping;

vector<vector<int>> matrix = {{0, 1, 1, 0, 0, 0}, {0, 0, 0, 1, 0, 1}, {0, 0, 0, 0, 1, 0},
                              {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}};

void
populateRouters ()
{
  srcToRouterMapping.clear ();
  desToRouterMapping.clear ();

  for (int i = 0; i < numRouters; i++)
    {
      for (int j = 0; j < realSourcesForRouters[i]; j++)
        {
          srcToRouterMapping.push_back (i);
        }
    }
  for (int i = 0; i < numRouters; i++)
    {
      for (int j = 0; j < virtualsForRouters[i]; j++)
        {
          srcToRouterMapping.push_back (i);
        }
    }
  for (int i = 0; i < numRouters; i++)
    {
      for (int j = 0; j < realDestinationsForRouters[i]; j++)
        {
          desToRouterMapping.push_back (i);
        }
    }
  for (int i = 0; i < numRouters; i++)
    {
      for (int j = 0; j < virtualsForRouters[i]; j++)
        {
          desToRouterMapping.push_back (i);
        }
    }

  for (int i = 0; i < numNodes; i++)
    {
      // std::cout << i + 1 << "->" << srcToRouterMapping[i] + 1 << " " << desToRouterMapping[i] + 1;
      // std::cout << "\n";
    }
}

static uint32_t
GetNodeIdFromContext (std::string context)
{
  std::size_t const n1 = context.find_first_of ("/", 1);
  std::size_t const n2 = context.find_first_of ("/", n1 + 1);
  return std::stoul (context.substr (n1 + 1, n2 - n1 - 1));
}

// Function to check queue length of Router 1
void
CheckQueueSize (P2PRouter *p2prouter)
{
  Ptr<QueueDisc> queue = p2prouter->qd.Get (0);
  uint32_t qSize = queue->GetCurrentSize ().GetValue ();

  // Check queue size every 1/5 of a second
  Simulator::Schedule (Seconds (0.001), &CheckQueueSize, p2prouter);
  std::ofstream fPlotQueue (std::stringstream (p2prouter->dir + "queueSize.dat").str ().c_str (),
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

// Calculate throughput and link utilisation for all flows
static void
TraceThroughputAndLU (Ptr<FlowMonitor> monitor, Ptr<Ipv4FlowClassifier> classifier,
                      P2PRouter *p2prouter)
{
  FlowMonitor::FlowStatsContainer stats = monitor->GetFlowStats ();
  Time currTime = Now ();
  uint32_t currBytes = 0;

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
  double throughput = 8 * (currBytes - p2prouter->prevBytes) /
                      (1000 * 1000 * (currTime.GetSeconds () - p2prouter->prevTime.GetSeconds ()));
  double link_util = (throughput * 1000 * 1000 * 100 / p2prouter->linkBandwidth.GetBitRate ());

  std::ofstream thr (p2prouter->dir + "/throughput.dat", std::ios::out | std::ios::app);
  std::ofstream lu (p2prouter->dir + "/linkUtilization.dat", std::ios::out | std::ios::app);
  thr << currTime.GetSeconds () << " " << throughput << std::endl;
  lu << currTime.GetSeconds () << " " << link_util << std::endl;

  p2prouter->prevTime = currTime;
  p2prouter->prevBytes = currBytes;

  Simulator::Schedule (Seconds (0.001 * rtt), &TraceThroughputAndLU, monitor, classifier,
                       p2prouter);
}

// Function to calculate and record the throughput for a specific destination IP
static void
TraceThroughputHelper (Ipv4Address destIP, uint32_t currBytes)
{
  Time currTime = Now ();

  // Calculate throughput using the formula: (change in bytes) / (time difference)
  double throughput =
      8 * (currBytes - IPtoDestinationData[destIP]->prevBytes) /
      (1000 * 1000 *
       (currTime.GetSeconds () - IPtoDestinationData[destIP]->prevTime.GetSeconds ()));

  std::ofstream thr (IPtoDestinationData[destIP]->throughput_file, std::ios::out | std::ios::app);
  thr << currTime.GetSeconds () << " " << throughput << std::endl;

  IPtoDestinationData[destIP]->prevTime = currTime;
  IPtoDestinationData[destIP]->prevBytes = currBytes;

  // Accumulate the calculated throughput to the corresponding group's accumulated throughput
  throughputPerGroup[IPtoDestinationData[destIP]->groupID] += throughput;
}

// Function to calculate and record the average throughput per group
static void
TraceAvgThroughputPerGroup ()
{
  // Get the current time
  Time currTime = Now ();

  // Loop through each group to calculate the average throughput
  for (uint32_t i = 0; i < groups; i++)
    {
      // Calculate the average throughput per group by dividing accumulated throughput by the number of nodes in the group
      throughputPerGroup[i] /= numNodesInGroup;
      std::ofstream thr (dir + "/throughput/avgThroughput_" + std::to_string (i),
                         std::ios::out | std::ios::app);
      thr << currTime.GetSeconds () << " " << throughputPerGroup[i] << std::endl;
    }
}

// Function to calculate flow-wise throughput
static void
TraceThroughput (Ptr<FlowMonitor> monitor, Ptr<Ipv4FlowClassifier> classifier)
{
  // Retrieve flow statistics
  FlowMonitor::FlowStatsContainer stats = monitor->GetFlowStats ();

  // Initialize the throughput per group to zero
  throughputPerGroup.assign (groups, 0.0);

  // Count the number of flows to process
  auto count = stats.size () / 2;

  // Aggregate received bytes for the first half of flows going towards the sink
  for (auto itr = stats.begin (); count > 0; ++itr, --count)
    {
      // Find the flow and its destination address
      Ipv4FlowClassifier::FiveTuple t = classifier->FindFlow (itr->first);
      // Calculate and record the throughput for the specific destination address
      TraceThroughputHelper (t.destinationAddress, itr->second.rxBytes);
    }

  // Calculate and record the average throughput per group
  TraceAvgThroughputPerGroup ();

  // Schedule the next throughput calculation after a certain time (rtt)
  Simulator::Schedule (Seconds (0.001 * rtt), &TraceThroughput, monitor, classifier);
}

void
printNodeIdsFromContainer (NodeContainer nc)
{
  uint32_t nNodes = nc.GetN ();
  for (uint32_t j = 0; j < nNodes; ++j)
    {
      Ptr<Node> p = nc.Get (j);
      std::cout << p->GetId () << " ";
    }
  std::cout << "\n";
}

void
saveTraceFiles (PointToPointHelper pointToPointLeaf)
{
  AsciiTraceHelper ascii;
  pointToPointLeaf.EnableAsciiAll (ascii.CreateFileStream (dir + "tcp.tr"));
}

void
saveQueueStats (P2PRouter *p2prouter)
{
  // Store queue stats in a file
  myfile.open (p2prouter->dir + "queueStats.txt",
               std::fstream::in | std::fstream::out | std::fstream::app);
  myfile << std::endl;
  myfile << "Stat for Queue";
  myfile << p2prouter->qd.Get (0)->GetStats ();
  myfile.close ();
}

vector<RouterProps *>
getRouterProps ()
{
  vector<RouterProps *> routerProps (numRouters);
  int i = 0;
  for (auto &props : routerProps)
    {
      i++;
      props = new RouterProps (minimumLinkDelay, bottleneckBandwidth,
                               dir + "router" + std::to_string (i) + '/', queueSize, qdiscTypeId);
    }
  return routerProps;
}

void
generateMatrix (NetworkMatrix *networkMatrix)
{
  for (int i = 0; i < numRouters; i++)
    {
      for (int j = i; j < numRouters; j++)
        {
          if (matrix[i][j])
            {
              LinkProps *props = new LinkProps (minimumLinkDelay, bottleneckBandwidth);
              networkMatrix->addEdge (i, j, props);
            }
        }
    }
}

static void
AllFlows (Ptr<FlowMonitor> monitor, Ptr<Ipv4FlowClassifier> classifier)
{
  FlowMonitor::FlowStatsContainer stats = monitor->GetFlowStats ();

  auto count = stats.size ();
  // aggregate rxBytes for first half flows (going towards sink):
  for (auto itr = stats.begin (); count > 0; ++itr, --count)
    {
      Ipv4FlowClassifier::FiveTuple t = classifier->FindFlow (itr->first);
      std::cout << "Flow " << itr->first << " (" << t.sourceAddress << " -> "
                << t.destinationAddress << ")\n";
    }

  Simulator::Schedule (Seconds (0.001 * rtt), &AllFlows, monitor, classifier);
}

int
main (int argc, char *argv[])
{
  if (isThresholdAQMEnabled)
    {
      if (tcpType == "TcpNewReno")
        {
          queueSize = QueueSize ("15p");
        }
      else
        {
          queueSize = QueueSize ("50p");
        }
    }

  CommandLine cmd;
  cmd.AddValue ("qdiscTypeId", "Queue disc for gateway (e.g., ns3::CoDelQueueDisc)", qdiscTypeId);
  cmd.AddValue ("segmentSize", "TCP segment size (bytes)", segmentSize);
  cmd.AddValue ("delAckCount", "Delayed ack count", delAckCount);
  cmd.AddValue ("numNodes", "Number of nodes in the sender", numNodes);
  cmd.AddValue ("roundTripTime", "Round trip time of a network packet", rtt);
  cmd.AddValue ("tcpVariant", "Type of tcp varient you want to use", tcpType);
  cmd.AddValue ("stopTime", "Stop time for applications / simulation time will be stopTime",
                stopTime);
  cmd.AddValue ("recovery", "Recovery algorithm type to use (e.g., ns3::TcpPrrRecovery", recovery);
  cmd.AddValue ("thEnabled", "Recovery algorithm type to use (e.g., ns3::TcpPrrRecovery",
                isThresholdAQMEnabled);
  cmd.Parse (argc, argv);

  dir += (isThresholdAQMEnabled ? "WithThresh/" : "WithoutThresh/") + std::to_string (numNodes) +
         "-" + tcpType + "-" + std::to_string (rtt) + "/";
  Config::SetDefault ("ns3::TcpL4Protocol::RecoveryType",
                      TypeIdValue (TypeId::LookupByName (recovery)));
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
  retVal = system ((dirToSave + "/cwndTraces/").c_str ());
  NS_ASSERT_MSG (retVal == 0, "Error in return value");
  retVal = system ((dirToSave + "/throughput/").c_str ());
  NS_ASSERT_MSG (retVal == 0, "Error in return value");

  populateRouters ();

  // Create nodes
  vector<RouterProps *> routerProps = getRouterProps ();

  NetworkMatrix *networkMatrix = new NetworkMatrix (numRouters);
  generateMatrix (networkMatrix);

  Network *network = new Network (routerProps, *networkMatrix);
  network->createRouters ();
  network->connectRouters ();

  NodeContainer sources, destinations;
  sources.Create (numNodes);
  destinations.Create (numNodes);

  vector<NetDeviceContainer> sourceToRouter, routerToDestination;

  PointToPointHelper pointToPointLeaf;
  pointToPointLeaf.DisableFlowControl ();
  pointToPointLeaf.SetDeviceAttribute ("DataRate", DataRateValue (accessLinkBandwidth));
  pointToPointLeaf.DisableFlowControl ();

  accessLinkDelays = variedAccessLinkDelays (numNodes, (rtt / 4));
  for (uint32_t j = 0; j < numNodes; ++j)
    {
      // 100 - 1 - 1 divided by 4
      pointToPointLeaf.SetChannelAttribute ("Delay", TimeValue (accessLinkDelays[j]));
      sourceToRouter.push_back (pointToPointLeaf.Install (
          sources.Get (j), network->getRouters (srcToRouterMapping[j])->routers.Get (0)));
      routerToDestination.push_back (pointToPointLeaf.Install (
          network->getRouters (desToRouterMapping[j])->routers.Get (1), destinations.Get (j)));
    }

  InternetStackHelper internetStack;

  internetStack.Install (sources);
  internetStack.Install (destinations);

  network->installInternetStack (&internetStack);

  // Assign IP addresses to all the network devices
  // TODO: For N > 3.2k, change bitmask to accomodate larger network
  vector<Ipv4Address> destinationIPAddresses;
  Ipv4AddressHelper ipAddresses ("10.0.0.0", "255.255.0.0");
  network->assignIpAddress (&ipAddresses);

  for (auto s2rLink : sourceToRouter)
    {
      ipAddresses.Assign (s2rLink);
      ipAddresses.NewNetwork ();
    }
  for (auto r2dLink : routerToDestination)
    {
      destinationIPAddresses.push_back (ipAddresses.Assign (r2dLink).GetAddress (1));
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

  AsciiTraceHelper asciiTraceHelper;
  Ptr<OutputStreamWrapper> streamWrapper;

  for (auto p2prouter : network->p2prouters)
    {
      // Calls function to check queue size
      p2prouter->installQueueDiscipline ();

      Simulator::Schedule (tracingStartTime, &CheckQueueSize, p2prouter);

      // Create dat to store packets dropped and marked at the router
      streamWrapper = asciiTraceHelper.CreateFileStream (p2prouter->dir + "drop.dat");
      p2prouter->qd.Get (0)->TraceConnectWithoutContext (
          "Drop", MakeBoundCallback (&DropAtQueue, streamWrapper));
    }

  // Install packet sink at receiver side for N nodes

  uint16_t port = 50000;
  for (uint32_t j = 0; j < numNodes; j++)
    {
      // NodeId 0 and 1 are assigned to routers, hence (2 + i) will be the nodeId
      InstallBulkSend (sources.Get (j), destinationIPAddresses[j], port, socketFactory,
                       sources.Get (j)->GetId (), 0, MakeCallback (&CwndChange));
    }

  for (uint32_t j = 0; j < numNodes; j++)
    {
      InstallPacketSink (destinations.Get (j), port, socketFactory);
    }
  // Install BulkSend application for N nodes

  // Enable PCAP on all the point to point interfaces
  // pointToPointLeaf.EnablePcapAll (dir + "pcap/ns-3", true);

  // Check for dropped packets using Flow Monitor
  FlowMonitorHelper flowmon;
  Ptr<FlowMonitor> monitor = flowmon.InstallAll ();
  Ptr<Ipv4FlowClassifier> classifier = DynamicCast<Ipv4FlowClassifier> (flowmon.GetClassifier ());
  // for (auto p2prouter : p2prouters)
  //   {
  //     Simulator::Schedule (tracingStartTime, &TraceThroughputAndLU, monitor, classifier, p2prouter);
  //   }
  // Simulator::Schedule (tracingStartTime, &TraceThroughput, monitor, classifier);
  // Simulator::Schedule (tracingStartTime, &AllFlows, monitor, classifier);

  Simulator::Stop (stopTime);
  Simulator::Run ();

  for (auto p2prouter : network->p2prouters)
    {
      saveQueueStats (p2prouter);
    }

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