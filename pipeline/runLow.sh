#!/bin/bash
export PATH=/workspace/tools:$PATH; P=/workspace/columbia_campus/_pipe; cd /workspace/columbia_low_library/v2
rm -f render.log; blender -b -P build.py > build.log 2>&1; blender -b -P bake.py -- 4096 > bake.log 2>&1; blender -b -P finish.py > finish.log 2>&1
BD=$PWD AN=NA_ColumbiaLowLibrary_13x10 blender -b NA_ColumbiaLowLibrary_13x10.blend -P $P/lodcheck.py > lodcheck.log 2>&1
blender -b NA_ColumbiaLowLibrary_13x10.blend -P render.py -- 64 > render.log 2>&1; echo ALLDONE >> render.log
