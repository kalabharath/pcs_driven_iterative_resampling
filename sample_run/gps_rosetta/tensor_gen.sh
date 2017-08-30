#!/bin/sh
EXECUTABLE="/rsc/tungsten/data2/Rosetta_freeze/rosetta1505/main/source/bin/score.default.linuxgccrelease"
BROKER_FLAG="-broker::setup $3"
DATABASE="-database /rsc/tungsten/data2/Rosetta_freeze/rosetta1505/main/database/"
FULL="-in:file:fullatom"
#RELAX="-relax::fast"
WEIGHTS="-score:weights $2"
PDBSCORE="-in:file:s $1"
#NATIVE="-in:file:native ../setup/idealized_erp29.pdb"
#OUT="-out:file:scorefile S0919_rescore.fsc"
TENSOR="-PCSTS1:write_extra Ts1_dvp.tensor -PCSTS2:write_extra Ts2_dvp.tensor -PCSTS3:write_extra Ts3_dvp.tensor -PCSTS4:write_extra Ts4_dvp.tensor"
#MUTE="-mute all"
run="${EXECUTABLE} ${NORM} ${DATABASE} ${SILENT} ${WEIGHTS} ${NATIVE} ${PDBSCORE} ${OUT} ${EXCLUDE} ${MUTE} ${FULL} ${TENSOR} ${BROKER_FLAG}"
$run
