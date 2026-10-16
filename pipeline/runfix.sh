#!/bin/bash
export PATH=/workspace/tools:$PATH; P=/workspace/columbia_campus/_pipe
cd /workspace/columbia_low_library/v2; blender -b -P finish.py > finish.log 2>&1; BD=$PWD AN=NA_ColumbiaLowLibrary_13x10 blender -b NA_ColumbiaLowLibrary_13x10.blend -P $P/lodcheck.py > lodcheck.log 2>&1
cd /workspace/columbia_campus/Butler; export BD=$PWD AN=NA_ButlerLibrary_11x7; blender -b -P $P/finish.py > finish.log 2>&1; blender -b $AN.blend -P $P/lodcheck.py > lodcheck.log 2>&1
echo DONE > $P/runfix.done
