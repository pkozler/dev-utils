#!/bin/bash

package_list='requirements.txt'

if [ $# -lt 1 ]
then
  echo 'List of commands:'
  echo ' - check <package_list>'
  echo ' - install <new_package>'
  echo ' - uninstall <old_package>'
  exit
fi

if [ $# -ge 1 ]
then
  cmd="$1"
  echo "Command: $cmd"

  if [ "$cmd" = "check" ]
  then
    python3 -m pip install -r "$package_list"
  fi

  if [ "$cmd" = "install" ] || [ "$cmd" = "uninstall"  ]
  then
    arg="$2"
    echo "Argument: $arg"
    python3 -m pip "$cmd" "$arg"
  fi

  echo "Syncing $package_list file:"
  python3 -m pip freeze > "$package_list"

  echo "Up to date!"
fi

