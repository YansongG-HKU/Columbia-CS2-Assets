#!/bin/bash
while [ ! -f /tmp/qE.done ]; do sleep 15; done
/workspace/columbia_campus/_pipe/runU.sh; echo > /tmp/qU.done
