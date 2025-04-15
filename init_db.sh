#!/bin/bash

# Wait for the database to be ready
until pg_isready -h db -U myuser; do
  echo "Waiting for PostgreSQL..."
  sleep 2
done

# Run the schema
psql -h db -U myuser -d mydatabase -f schema.sql
