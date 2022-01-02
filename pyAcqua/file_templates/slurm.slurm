#!/bin/bash
env
version="STAR_VERSION"

cpus="$SLURM_CPUS_ON_NODE"
nodelistcompact="$SLURM_JOB_NODELIST"
nodelistfull=`scontrol show hostnames $nodelistcompact`
nodes=`echo $nodelistfull | sed 's/$/ /g' | sed 's/ /:'"$cpus,"'/g'`

rm -f DONE
rm -f ABORT



sim_file="SIM_FILE_NAME"
java_name="JOB_NAME"
rm -f "JOB_NAME".log

${version}/star/bin/starccm+ -printpids -batch -rsh ssh $java_name.java $sim_file.sim -on $nodes >> "JOB_NAME".log


touch DONE
