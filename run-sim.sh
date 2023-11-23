NODES=(60)
TCP_FLAVOUR=("TcpNewReno" "TcpCubic")
RTT=(10 200)
THRESH=(true false)

cd ../results/
# rm -rf *

cd ../../


# first loop iterates over nodes
for i in {0..0}
do
    # # second loop iterates over TCP flavours
    for j in {0..1}
    do
        # # third loop iterate over RTT
        for k in {0..1}
        do
            # # fourth loop iterate over Thresh
            for l in {0..1}
            do
                echo "Running this config:" ${NODES[$i]} ${TCP_FLAVOUR[j]} ${RTT[k]} ${THRESH[l]}
                ./ns3 run single-bottleneck-dumbbell-topology -- --numNodes=${NODES[$i]} --tcpVariant=${TCP_FLAVOUR[$j]} --roundTripTime=${RTT[$k]} --thEnabled=${THRESH[$l]}
                echo "This config ran successfully:" ${NODES[$i]} ${TCP_FLAVOUR[j]} ${RTT[k]} ${THRESH[l]}
            done
        done
    done
done