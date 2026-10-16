#!/bin/bash
while [ ! -f /tmp/queue_fix.done ]; do sleep 20; done
/workspace/columbia_campus/_pipe/runL.sh; /workspace/columbia_campus/_pipe/runPu.sh; echo > /tmp/queue2.done
