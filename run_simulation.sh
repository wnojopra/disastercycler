#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 <day_number>"
  exit 1
fi

DAY_NUM="$1"

python -m engine.simulation the_first_script "actions_${DAY_NUM}"
