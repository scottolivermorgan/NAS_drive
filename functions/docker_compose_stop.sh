#!/bin/bash

# List of directories
directories=(
  "/home/scott/NAS_drive/ansible/tasks/abs_compose"
  "/home/scott/NAS_drive/ansible/tasks/arr_stack_compose"
  "/home/scott/NAS_drive/ansible/tasks/grafana_compose"
  "/home/scott/NAS_drive/ansible/tasks/immich_compose"
  "/home/scott/NAS_drive/ansible/tasks/index_page_compose"
  "/home/scott/NAS_drive/ansible/tasks/jellyfin_compose"
  "/home/scott/NAS_drive/ansible/tasks/komga_compose"
  "/home/scott/NAS_drive/ansible/tasks/nextcloud_compose"
  "/home/scott/NAS_drive/ansible/tasks/tandoor_compose"
)

# Loop over each directory and bring down the services
for dir in "${directories[@]}"; do
  cd "$dir" || { echo "Failed to cd into $dir"; exit 1; }
  echo "stopping container $dir"
  docker-compose stop
done
