#!/bin/sh

echo "Rebuilding cluster..."
sudo docker compose build 

echo "Running cluster again..."
sudo docker compose up
