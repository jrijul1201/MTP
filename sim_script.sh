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

cd ../


# # first loop iterates over nodes
# for i in {0..2}
# do
# # # second loop iterates over TCP flavours
# for j in {0..2}
# # # third loop iterate over RTT
# do
# for k in {0..4}
# do
# ./ns3 run parking-lot-topology -- --numNodes=${NODES[$i]} --tcpVariant=${TCP_FLAVOUR[$j]} --roundTripTime=${RTT[$k]}
# echo "This config ran successfully:" ${NODES[$i]} ${TCP_FLAVOUR[j]} ${RTT[k]}
# done
# done
# done

# for l in {0..2}
# do
# # # second loop iterates over TCP flavours
# for m in {0..2}
# # # third loop iterate over RTT
# do
# for n in {0..4}
# do
# ./ns3 run parking-lot-topology -- --numNodes=${NODES[$l]} --tcpVariant=${TCP_FLAVOUR[$m]} --roundTripTime=${RTT[$k]} --thEnabled=true
# echo "This config ran successfully for thresh:" ${NODES[$i]} ${TCP_FLAVOUR[$j]} ${RTT[$k]}
# done
# done
# done

cd results/
for dir in *
do
cd ${dir}
for folder in *
do
rm -rf ${folder}/plots/
mkdir ${folder}/plots/
current_path=$(pwd)
cd ../../MTP
echo ${current_path}/${folder} | python3 plotScript.py
cd ../results/${dir}
done
cd ../
done

# git add .
# git commit -m "updated plots"
# git push