#!/bin/bash

# Run Hector v2.0.1 for all defauly RCP scenarios (26, 45, 60, 85)

HECTOR_VERSION="v2.0.1"

HECTOR_ROOT="/mnt/c/Users/nich980/code/hector-worktrees/release_$HECTOR_VERSION"

INPUT_DIR="../input"
SOURCE_DIR="source"

HECTOR_SRC="$HECTOR_ROOT/$SOURCE_DIR"

RCP_FILES="26 45 60 85"

echo "Entering $HECTOR_SRC..."
cd $HECTOR_SRC

# Check that source/output exists. If it does not exist at runtime, Hector output
# will not be written. I'm too lazt to change the macro in headers/h_util.hpp & re-build
echo "Validating output directory..."
if [ ! -d "$HECTOR_SRC/output" ]; then
  mkdir "$HECTOR_SRC/output"
fi

# Run Hector for each RCP scenario
for RCP in $RCP_FILES
do
  INI_FILE="$INPUT_DIR/hector_rcp$RCP.ini"
    
  echo "--- Running Hector for RCP$RCP ---"
  ./hector $INI_FILE
done
