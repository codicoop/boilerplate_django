#!/usr/bin/env bash

set -eo pipefail

APP_NAME="${1}" # App name that we want to change to.
FIND_APP_NAME="django_boilerplate" # Current app name

# Check that the necessary args have been passed.
if [ -z "${APP_NAME}" ]; then
    echo "You must supply an app, example: ${0} myapp"
    exit 1
fi

# Check that a new name has been chosen.
if [ "${APP_NAME}" = "${FIND_APP_NAME}" ]; then
    echo "Your new app name must be different than the current app name"
    exit 1
fi

cat << EOF

When renaming your project you'll need to re-create a new database.

This can easily be done with Docker, but before this script does it
please agree that it's ok for this script to delete your current
project's database(s) by removing any associated Docker volumes.

EOF

while true; do
    read -p "Run docker compose down -v (y/n)? " -r yn
    case "${yn}" in
        [Yy]* )
          printf "\n--------------------------------------------------------\n"
          docker compose down -v
          printf -- "--------------------------------------------------------\n"

          break;;
        [Nn]* ) exit;;
        * ) echo "";;
    esac
done

# -----------------------------------------------------------------------------
# The core of the script which renames a few things.
# -----------------------------------------------------------------------------
#
# The `find . -type -f` command finds every file in the current and any children
# directory. With the `-exec`, for each file we execute the perl interpreter.
# The options of the interpreter are:
#   -i: edit the files in place
#   -p: execute the given code for every line in the file, and print the line
#   -e commandline: a simle substitute command
#
# The it executes a one line program which uses the substitue command and
# finds and replaces both the app and module names in each file. 
find . -type f -exec \
  perl -i -pe "s/${FIND_APP_NAME}/${APP_NAME}/g;" {} +
# -----------------------------------------------------------------------------

cat << EOF

--------------------------------------------------------
Your project has been renamed successfully!
--------------------------------------------------------

EOF

function init_git_repo {
  [ -d .git/ ] && rm -rf .git/

cat << EOF

--------------------------------------------------------
$(git init)
--------------------------------------------------------
EOF

  # Points HEAD to the new main branch
  git symbolic-ref HEAD refs/heads/main
}

while true; do
    read -p "Do you want to init a new local git repo (y/n)? " -r yn
    case "${yn}" in
        [Yy]* ) init_git_repo; break;;
        [Nn]* ) break;;
        * ) echo "";;
    esac
done

cat << EOF

Project rename completed succesfully!

EOF