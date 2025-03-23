#!/bin/bash

# Function to prune Docker resources
prune_docker_resources() {
  local resource=$1
  echo "Pruning $resource..."
  echo "y" | docker "$resource" prune -f
}

# Prune volumes, system, containers, images, and builders
prune_docker_resources "volume"
prune_docker_resources "system"
prune_docker_resources "container"
prune_docker_resources "image"
prune_docker_resources "builder"

echo "Docker pruning completed!"
