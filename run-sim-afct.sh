#!/bin/bash

TCP_FLAVOUR=("TcpCubic" "TcpNewReno")
THRESH=(true false)
RTT=(10 200)

cd ../../
# # second loop iterates over TCP flavours
# for j in {0..1}
# do
#     # # third loop iterate over RTT
#     for k in {0..1}
#     do
#         # # fourth loop iterate over Thresh
#         for l in {0..1}
#         do
#             echo "Running this config:"  ${TCP_FLAVOUR[j]} ${RTT[k]} ${THRESH[l]}
#             ./ns3 run afct-single -- --tcpVariant=${TCP_FLAVOUR[$j]} --roundTripTime=${RTT[$k]} --thEnabled=${THRESH[$l]}
#             echo "This config ran successfully:"  ${TCP_FLAVOUR[j]} ${RTT[k]} ${THRESH[l]}
#         done
#     done
# done

# # second loop iterates over TCP flavours
for j in {0..1}
do
    # # third loop iterate over RTT
    for k in {0..1}
    do
        # # fourth loop iterate over Thresh
        for l in {0..1}
        do
            echo "Running this config:"  ${TCP_FLAVOUR[j]} ${RTT[k]} ${THRESH[l]}
            ./ns3 run afct-parking -- --tcpVariant=${TCP_FLAVOUR[$j]} --roundTripTime=${RTT[$k]} --thEnabled=${THRESH[$l]}
            echo "This config ran successfully:"  ${TCP_FLAVOUR[j]} ${RTT[k]} ${THRESH[l]}
        done
    done
done