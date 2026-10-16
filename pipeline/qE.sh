#!/bin/bash
while [ ! -f /tmp/q3.done ]; do sleep 15; done
/workspace/columbia_campus/_pipe/runE.sh; echo > /tmp/qE.done
