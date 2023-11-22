cd ../end-sem-results/
for folder in *
    do
        cd ${folder}
        for resultFolder in *
            do
                rm -rf ${resultFolder}/plots/
                mkdir ${resultFolder}/plots/
                current_path=$(pwd)
                echo ${current_path}/${resultFolder} | python3 ../../MTP/makePlots.py
        done
        cd ../
done
