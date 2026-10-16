#!/bin/bash
export PATH=/workspace/tools:$PATH; P=/workspace/columbia_campus/_pipe; cd /workspace/columbia_campus/StPaulsChapel
export BD=$PWD AN=NA_StPaulsChapel_4x6 ROOFCOL=0.40,0.17,0.11 BRICKCOL=0.46,0.22,0.12 SAFEDROP=1
rm -f render.log; blender -b -P build.py > build.log 2>&1; blender -b -P $P/bake.py -- 4096 > bake.log 2>&1; blender -b -P $P/finish.py > finish.log 2>&1; blender -b $AN.blend -P $P/lodcheck.py > lodcheck.log 2>&1; blender -b $AN.blend -P $P/render.py -- 48 > render.log 2>&1; echo ALLDONE >> render.log
