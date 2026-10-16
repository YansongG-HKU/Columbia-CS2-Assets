#!/bin/bash
export PATH=/workspace/tools:$PATH
P=/workspace/columbia_campus/_pipe
run_b(){ cd $1; export BD=$1 AN=$2 ROOFCOL=$3 BRICKCOL=$4; rm -f render.log
 blender -b -P build.py > build.log 2>&1; blender -b -P $P/bake.py -- 4096 > bake.log 2>&1; blender -b -P $P/finish.py > finish.log 2>&1; blender -b $AN.blend -P $P/render.py -- 48 > render.log 2>&1; echo ALLDONE >> render.log; }
run_b /workspace/columbia_campus/Butler NA_ButlerLibrary_11x7 0.16,0.16,0.155 0.36,0.17,0.10
cd /workspace/columbia_low_library/v2; rm -f render.log; blender -b -P build.py > build.log 2>&1; blender -b -P bake.py -- 4096 > bake.log 2>&1; blender -b -P finish.py > finish.log 2>&1; blender -b NA_ColumbiaLowLibrary_13x10.blend -P render.py -- 64 > render.log 2>&1; echo ALLDONE >> render.log
run_b /workspace/columbia_campus/StPaulsChapel NA_StPaulsChapel_4x6 0.10,0.26,0.15 0.46,0.22,0.12
echo ALL > /workspace/columbia_campus/_pipe/runall.done
