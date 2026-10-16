#!/bin/bash
P=/workspace/columbia_campus/_pipe
for s in runH runJ runP runK runA; do $P/$s.sh; done
echo QDONE > /tmp/queue_fix.done
