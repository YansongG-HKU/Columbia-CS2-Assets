#!/bin/bash
export PATH=/workspace/tools:$PATH; P=/workspace/columbia_campus/_pipe
while pgrep -f runH.sh >/dev/null; do sleep 15; done
cd /workspace/columbia_campus/Butler
export BD=$PWD AN=NA_ButlerLibrary_11x7 ROOFCOL=0.16,0.16,0.155 BRICKCOL=0.74,0.70,0.62 CARVECOL=0.30,0.27,0.22
rm -f render.log; blender -b -P build.py > build.log 2>&1; blender -b -P $P/bake.py -- 4096 > bake.log 2>&1; blender -b -P $P/finish.py > finish.log 2>&1; blender -b $AN.blend -P $P/lodcheck.py > lodcheck.log 2>&1; blender -b $AN.blend -P $P/render.py -- 48 > render.log 2>&1; echo ALLDONE >> render.log
