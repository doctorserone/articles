#!/bin/sh

echo "Cleaning unused images..."
sudo docker image prune -af
