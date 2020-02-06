#!/bin/bash

# Run the specified Hector version for all defauly RCP scenarios (26, 45, 60, 85)
#
# Usage
# -----
# ./run-hector_vall.sh 2.0.0 2.0.1

RUN_VERSION () {
  HECTOR_VERSION=$1

  HECTOR_ROOT="/mnt/c/Users/nich980/code/hector-worktrees/release_v$HECTOR_VERSION"

  INPUT_DIR="../input"
  SOURCE_DIR="source"

  HECTOR_SRC="$HECTOR_ROOT/$SOURCE_DIR"

  RCP_FILES="26 45 60 85"

  echo "Entering $HECTOR_SRC..."
  cd $HECTOR_SRC

  # Check that source/output exists. If it does not exist at runtime, Hector output
  # will not be written. I'm too lazt to change the macro in headers/h_util.hpp & re-build
  if [ ! -d "$HECTOR_SRC/output" ]; then
    mkdir "$HECTOR_SRC/output"
  fi

  # Run Hector for each RCP scenario
  for RCP in $RCP_FILES
  do
    INI_FILE="$INPUT_DIR/hector_rcp$RCP.ini"
    
    echo "\n--- Running Hector v$HECTOR_VERSION for RCP$RCP ---"
    ./hector $INI_FILE
  done
}

# Execute each given hector version
for VERSION in "$@"
do
  RUN_VERSION $VERSION
done
