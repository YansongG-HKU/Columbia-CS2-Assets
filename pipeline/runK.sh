#!/bin/bash
export PATH=/workspace/tools:$PATH; P=/workspace/columbia_campus/_pipe; cd /workspace/columbia_campus/KentHall
export BD=$PWD AN=NA_KentHall_8x4 ROOFCOL=0.20,0.38,0.30 BRICKCOL=0.30,0.125,0.08
rm -f render.log; blender -b -P build.py > build.log 2>&1; blender -b -P $P/bake.py -- 4096 > bake.log 2>&1; blender -b -P $P/finish.py > finish.log 2>&1; blender -b $AN.blend -P $P/lodcheck.py > lodcheck.log 2>&1; blender -b $AN.blend -P $P/render.py -- 48 > render.log 2>&1; echo ALLDONE >> render.log
