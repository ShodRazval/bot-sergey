#!/bin/bash

git fetch origin
git checkout -f origin/deploy

docker compose up
