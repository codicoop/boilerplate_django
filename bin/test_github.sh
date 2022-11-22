#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

# Building and testing dev image:
docker compose build
docker compose up -d
docker compose down -v
