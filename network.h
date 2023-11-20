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
#include "router.h"
#include "destination-data.h"

using namespace std;

struct NetworkMatrix
{
  vector<vector<LinkProps *>> networkMatrix;
  NetworkMatrix ()
  {
  }
  NetworkMatrix (int n)
  {
    this->networkMatrix = vector<vector<LinkProps *>> (n, vector<LinkProps *> (n, NULL));
  }

  void
  addEdge (int i, int j, LinkProps *linkProps)
  {
    this->networkMatrix[i][j] = linkProps;
  }

  LinkProps *
  getLinkProps (int i, int j)
  {
    return this->networkMatrix[i][j];
  }
};

class Network
{
public:
  vector<RouterProps *> routerProps;
  NetworkMatrix networkMatrix;
  vector<P2PRouter *> p2prouters;
  PointToPointHelper pointToPointLeaf;
  vector<NetDeviceContainer> routerToRouterLinks;
  Network (vector<RouterProps *> routerProps, NetworkMatrix networkMatrix)
  {
    this->routerProps = routerProps;
    this->networkMatrix = networkMatrix;
  }

  void
  createRouters ()
  {
    int numRouters = this->routerProps.size ();
    for (uint32_t i = 0; i < numRouters; i++)
      {
        RouterProps *routerProp = this->routerProps[i];
        P2PRouter *router = new P2PRouter (routerProp->dir + "/",
                                           routerProp->queueSize, routerProp->linkBandwidth,
                                           routerProp->linkDelay, routerProp->qdiscTypeId);
        p2prouters.push_back (router);
      }
  }

  void
  connectRouters ()
  {
    pointToPointLeaf.DisableFlowControl ();
    int numRouters = routerProps.size ();
    for (int i = 0; i < numRouters; i++)
      {
        for (int j = 0; j < numRouters; j++)
          {
            LinkProps *link = networkMatrix.getLinkProps (i, j);
            if (link && link->linkExist)
              {
                pointToPointLeaf.SetChannelAttribute ("Delay", TimeValue (link->linkDelay));
                pointToPointLeaf.SetDeviceAttribute (
                    "DataRate", DataRateValue (link->linkBandwidth.GetBitRate ()));
                routerToRouterLinks.push_back (pointToPointLeaf.Install (
                    p2prouters[i]->routers.Get (1), p2prouters[j]->routers.Get (0)));
              }
          }
      }
  }

public:
  P2PRouter *
  getRouters (int i)
  {
    return p2prouters[i];
  }

  void
  installInternetStack (InternetStackHelper *internetStack)
  {
    for (auto p2pRouter : p2prouters)
      {
        internetStack->Install (p2pRouter->routers);
      }
  }

  void
  assignIpAddress (Ipv4AddressHelper *ipAddresses)
  {
    for (auto p2prouter : p2prouters)
      {
        ipAddresses->Assign (p2prouter->netDevice);
        ipAddresses->NewNetwork ();
      }
    for (auto r2rLink : routerToRouterLinks)
      {
        ipAddresses->Assign (r2rLink);
        ipAddresses->NewNetwork ();
      }
  }
};