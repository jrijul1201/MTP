build_example(
  NAME tcp-large-transfer
  SOURCE_FILES tcp-large-transfer.cc
  LIBRARIES_TO_LINK
    ${libpoint-to-point}
    ${libapplications}
    ${libinternet}
)

build_example(
  NAME tcp-star-server
  SOURCE_FILES tcp-star-server.cc
  LIBRARIES_TO_LINK
    ${libpoint-to-point}
    ${libapplications}
    ${libinternet}
)

build_example(
  NAME star
  SOURCE_FILES star.cc
  LIBRARIES_TO_LINK
    ${libnetanim}
    ${libpoint-to-point}
    ${libpoint-to-point-layout}
    ${libapplications}
    ${libinternet}
)

build_example(
  NAME tcp-bbr-example
  SOURCE_FILES tcp-bbr-example.cc
  LIBRARIES_TO_LINK
    ${libpoint-to-point}
    ${libinternet}
    ${libapplications}
    ${libtraffic-control}
    ${libnetwork}
    ${libinternet-apps}
    ${libflow-monitor}
)

build_example(
  NAME tcp-bulk-send
  SOURCE_FILES tcp-bulk-send.cc
  LIBRARIES_TO_LINK
    ${libpoint-to-point}
    ${libapplications}
    ${libinternet}
)

build_example(
  NAME tcp-pcap-nanosec-example
  SOURCE_FILES tcp-pcap-nanosec-example.cc
  LIBRARIES_TO_LINK
    ${libpoint-to-point}
    ${libapplications}
    ${libinternet}
)

build_example(
  NAME tcp-variants-comparison
  SOURCE_FILES tcp-variants-comparison.cc
  LIBRARIES_TO_LINK
    ${libpoint-to-point}
    ${libinternet}
    ${libapplications}
    ${libflow-monitor}
)

build_example(
  NAME tcp-pacing
  SOURCE_FILES tcp-pacing.cc
  LIBRARIES_TO_LINK
    ${libpoint-to-point}
    ${libinternet}
    ${libapplications}
    ${libflow-monitor}
)

build_example(
  NAME tcp-linux-reno
  SOURCE_FILES tcp-linux-reno.cc
  LIBRARIES_TO_LINK
    ${libpoint-to-point}
    ${libinternet}
    ${libapplications}
    ${libtraffic-control}
    ${libnetwork}
)

build_example(
  NAME tcp-dumbell
  SOURCE_FILES tcp-dumbell.cc
  LIBRARIES_TO_LINK
    ${libpoint-to-point}
    ${libinternet}
    ${libapplications}
    ${libtraffic-control}
    ${libnetwork}
)

build_example(
  NAME tcp-dumbell-2
  SOURCE_FILES tcp-dumbell-2.cc
  LIBRARIES_TO_LINK
    ${libpoint-to-point}
    ${libinternet}
    ${libapplications}
    ${libtraffic-control}
    ${libnetwork}
)

build_example(
  NAME single-bottleneck-dumbbell-topology
  SOURCE_FILES single-bottleneck-dumbbell-topology.cc
  LIBRARIES_TO_LINK
    ${libpoint-to-point}
    ${libinternet}
    ${libapplications}
    ${libtraffic-control}
    ${libnetwork}
    ${libflow-monitor}
)

build_example(
  NAME parking-lot-topology
  SOURCE_FILES parking-lot-topology.cc
  LIBRARIES_TO_LINK
    ${libpoint-to-point}
    ${libinternet}
    ${libapplications}
    ${libtraffic-control}
    ${libnetwork}
    ${libflow-monitor}
)

build_example(
  NAME sandwich-network-topology
  SOURCE_FILES sandwich-network-topology.cc
  LIBRARIES_TO_LINK
    ${libpoint-to-point}
    ${libinternet}
    ${libapplications}
    ${libtraffic-control}
    ${libnetwork}
    ${libflow-monitor}
)

build_example(
  NAME static-routing-via-virtual
  SOURCE_FILES static-routing-via-virtual.cc
  LIBRARIES_TO_LINK
    ${libpoint-to-point}
    ${libinternet}
    ${libapplications}
    ${libtraffic-control}
    ${libnetwork}
    ${libflow-monitor}
)

build_example(
  NAME tcp-validation
  SOURCE_FILES tcp-validation.cc
  LIBRARIES_TO_LINK
    ${libpoint-to-point}
    ${libinternet}
    ${libapplications}
    ${libtraffic-control}
    ${libnetwork}
    ${libinternet-apps}
)

build_example(
  NAME dctcp-example
  SOURCE_FILES dctcp-example.cc
  LIBRARIES_TO_LINK
    ${libcore}
    ${libnetwork}
    ${libinternet}
    ${libpoint-to-point}
    ${libapplications}
    ${libtraffic-control}
)

build_example(
  NAME afct-single
  SOURCE_FILES afct-single-bottleneck-dumbbell-topology.cc
  LIBRARIES_TO_LINK
    ${libpoint-to-point}
    ${libinternet}
    ${libapplications}
    ${libtraffic-control}
    ${libnetwork}
    ${libflow-monitor}
)

build_example(
  NAME afct2-single
  SOURCE_FILES afct2-single-bottleneck-dumbbell-topology.cc
  LIBRARIES_TO_LINK
    ${libpoint-to-point}
    ${libinternet}
    ${libapplications}
    ${libtraffic-control}
    ${libnetwork}
    ${libflow-monitor}
)

build_example(
  NAME multi-bottleneck
  SOURCE_FILES multi-bottleneck-topology.cc
  LIBRARIES_TO_LINK
    ${libcore}
    ${libnetwork}
    ${libinternet}
    ${libpoint-to-point}
    ${libapplications}
    ${libipv4-static-routing}
    ${libipv4-list-routing}
    ${libconfig-store}
)