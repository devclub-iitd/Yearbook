#!/bin/bash

echo "Starting Development server..."
docker-compose -f app/docker-compose.dev.yml up --build