#!/bin/bash

if [ $1 ]; then
    date=$1
    full=1
else
    date=`date -v -12H +'%Y%m%d'`
fi

massdate=${date:2}
year=${date:0:4}
day=${date:4:4}

if [ -z "$MASSPIPE" ]; then
    MASSPIPE="/Users/timdimm/MASSDIMM/masspipe"
fi

execdir="$MASSPIPE/"
datadir="$MASSPIPE/data/$year/$day/"

stmfile="$massdate-mass.stm"
stmurl="http://massdimm.suth/mass/$stmfile"

full="${date}_13_layer.atmos"
quick="${full}297"

if [ -e $datadir ]; then
    echo "Already have done $date."
else
    echo "Making $datadir..."
    mkdir -p $datadir
    echo "Moving to $datadir..."
    cd $datadir
    echo "Getting stm file $stmurl..."
    curl -f -O $stmurl

    if [ -e $stmfile ]; then
        echo "Running quick analysis..."
        $execdir/quickmass $stmfile > $quick

        if [ $full ]; then
            echo "Running full analysis..."
            $execdir/fullmass $stmfile > $full
        fi
    else
        echo "Whoops!  No data for $date..."
    fi
fi
