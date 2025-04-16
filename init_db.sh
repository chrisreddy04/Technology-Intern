#!/bin/bash

until pg_isready -h db -U myuser; do
  echo "Waiting for PostgreSQL..."
  sleep 2
done

psql -h db -U myuser -d mydatabase -f schema.sql
