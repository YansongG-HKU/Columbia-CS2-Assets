#!/bin/bash
export PATH=/workspace/tools:$PATH; P=/workspace/columbia_campus/_pipe; cd /workspace/columbia_campus/Butler
export BD=$PWD AN=NA_ButlerLibrary_11x7 ROOFCOL=0.16,0.16,0.155 BRICKCOL=0.30,0.125,0.08
rm -f render.log; blender -b -P $P/finish.py > finish.log 2>&1; blender -b $AN.blend -P $P/lodcheck.py > lodcheck.log 2>&1; echo ALLDONE >> render.log
