#!/bin/bash

# Exit on error
set -o errexit

# script dir is the dir of the current script
SCRIPT_DIR=$(dirname "$0")
SCRIPTS_DIR="$SCRIPT_DIR/scripts"
GCPTOOLKIT_DIR="$SCRIPT_DIR/gcptoolkit"

# Check for --python flag anywhere in arguments
use_python=false
script_args=()

# Process all arguments to find --python flag and build script_args
for arg in "$@"; do
    if [[ "$arg" == "--python" ]]; then
        use_python=true
    else
        script_args+=("$arg")
    fi
done

# the first arg is the script name
script_name="${script_args[0]}"

# Remove script name from script_args
if [[ ${#script_args[@]} -gt 0 ]]; then
    script_args=("${script_args[@]:1}")
fi

# Check if --python flag is used
if [[ "$use_python" == true ]]; then
    # Check if the Python file exists in the $GCPTOOLKIT_DIR directory
    if [[ -f "$GCPTOOLKIT_DIR/$script_name.py" ]]; then
        uv run "$GCPTOOLKIT_DIR/$script_name.py" "${script_args[@]}"
        exit 0
    else
        echo "Error: Python script not found: $script_name.py in $GCPTOOLKIT_DIR"
        exit 1
    fi
else
    # Check if the file exists in the $SCRIPTS_DIR directory
    if [[ -f "$SCRIPTS_DIR/$script_name.sh" ]]; then
        source "$SCRIPTS_DIR/$script_name.sh" "${script_args[@]}"
        exit 0
    fi
fi

echo "Error: Unknown command: $script_name"
exit 1