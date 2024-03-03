#!/bin/bash

git fetch origin
git checkout -f origin/main

docker compose up
