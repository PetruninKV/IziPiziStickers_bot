#!/bin/bash

git stash & git pull
sudo docker-compose up --build --force-recreate -d
