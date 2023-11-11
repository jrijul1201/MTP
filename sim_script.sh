#!/bin/bash

# this script runs FAST TCP simulations
# SM Aug 2015
# 2 factors: buffer size and RTT
# generates tracefiles for each value of buffer size and RTT. All simulations corresponding to a given buffer size are clubbed in a directory named after the buffer size. 
# NODES=(1)
# TCP_FLAVOUR=("TcpNewReno")
# RTT=(10)

# NODES=(40 60 80)
# TCP_FLAVOUR=("TcpNewReno" "TcpBbr" "TcpCubic")
# RTT=(10 50 100 150 200)

# cd ../results/
# rm -rf *
# git add .
# git commit -m "cleaned results"
# git push --force

cd ../../


# # first loop iterates over nodes
# for i in {0..2}
# do
# # # second loop iterates over TCP flavours
# for j in {0..2}
# # # third loop iterate over RTT

# do

# for k in {0..4}

# do
# ./ns3 run parking-lot-topology -- --numNodes=${NODES[$i]} --tcpVariant=${TCP_FLAVOUR[j]} --roundTripTime=${RTT[k]}
# # mkdir examples/results/${NODES[$i]}-${TCP_FLAVOUR[j]}-${RTT[k]}
# # # mv {queue,queue${RTT[$j]}}.tr
# # # mv {queuebw,queuebw${RTT[$j]}}.tr
# # # mv {queuelost,queuelost${RTT[$j]}}.tr
# # # mv {queuesize,queuesize${RTT[$j]}}.tr
# # # mv {queuewin,queuewin${RTT[$j]}}
# # # moving the trace files to the directory associated with the buffer size 
# # # mv $buff queue${RTT[$j]}.tr queuebw${RTT[$j]}.tr queuelost${RTT[$j]}.tr queuelost1${RTT[$j]}.tr queuesize${RTT[$j]}.tr queuewin${RTT[$j]}
# # echo "This config ran successfully:" ${NODES[$i]} ${TCP_FLAVOUR[j]} ${RTT[k]}
# done

# done

# done

cd examples/results/
for folder in *
do
rm -rf ${folder}/plots/
mkdir ${folder}/plots/
current_path=$(pwd)
cd ../tcp
echo ${current_path}/${folder} | python3 plotScript.py
cd ../results
done

# git add .
# git commit -m "updated plots"
# git push