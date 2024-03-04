# NODES=(60)
TCP_FLAVOUR=("TcpLinuxReno" "TcpNewReno")
# THRESH=(true false)

# cd ../results/
# rm -rf *

# cd ../../


# # first loop iterates over nodes
# for i in {0..0}
# do
#     # # second loop iterates over TCP flavours
#     for j in {0..1}
#     do
#         # # third loop iterate over RTT
#         for k in {0..1}
#         do
#             # # fourth loop iterate over Thresh
#             for l in {0..1}
#             do
#                 echo "Running this config:" ${NODES[$i]} ${TCP_FLAVOUR[j]} ${RTT[k]} ${THRESH[l]}
#                 ./ns3 run parking-lot-topology -- --numNodes=${NODES[$i]} --tcpVariant=${TCP_FLAVOUR[$j]} --roundTripTime=${RTT[$k]} --thEnabled=${THRESH[$l]}
#                 echo "This config ran successfully:" ${NODES[$i]} ${TCP_FLAVOUR[j]} ${RTT[k]} ${THRESH[l]}
#             done
#         done
#     done
# done

# # fourth loop iterate over Thresh
for l in {0..2}
do
    for rtt in {10..300..5}
    do
        echo "Running this config:" ${rtt}
        ../../ns3 run multi-bottleneck -- --thEnabled=true --roundTripTime=${rtt}ms --qTh=100
        ../../ns3 run multi-bottleneck -- --thEnabled=true --roundTripTime=${rtt}ms --qTh=15
        ../../ns3 run multi-bottleneck -- --thEnabled=false --roundTripTime=${rtt}ms
        echo "This config ran successfully:" ${rtt}
        # echo $rtt
    done
done