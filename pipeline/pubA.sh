#!/bin/bash
# pubA.sh <dir> <msg> : republish existing building reusing README metadata
R=/workspace/Columbia-CS2-Assets/$1
row=$(grep "\[$1\]" /workspace/Columbia-CS2-Assets/README.md)
T=$(echo "$row"|cut -d'|' -f2|xargs); A=$(echo "$row"|cut -d'|' -f4|xargs); L=$(echo "$row"|cut -d'|' -f5|xargs)
LOT=$(grep "^| Lot |" $R/README.md|cut -d'|' -f3|xargs); REAL=$(grep "^| Real reference |" $R/README.md|cut -d'|' -f3|sed 's/^ //;s/ $//')
bash /workspace/columbia_campus/_pipe/pub1.sh $1 $A $1 "$T" "$LOT" "$REAL" "$L" "$2"
