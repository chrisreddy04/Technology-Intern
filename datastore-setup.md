# Datastore Setup and Rationale

## Overview

For this project, **PostgreSQL** was chosen as the primary datastore to store and manage the structured data required for my technology intern assessment. This document explains the reasons behind this choice and outlines how the PostgreSQL environment is set up.

## Why PostgreSQL?

- **Structured Data Management:**  
  PostgreSQL is a robust relational database management system (RDBMS) that effectively handles structured data with predefined schemas. The dataset—comprising fields like country, year, industry, AI adoption rate, etc.—fits naturally into a relational model.

- **ACID Compliance and Reliability:**  
  PostgreSQL ensures that transactions are atomic, consistent, isolated, and durable (ACID compliant), which is critical for maintaining data integrity during batch and real-time operations.

- **Advanced Query Capabilities:**  
  Using SQL, PostgreSQL allows complex queries, aggregations, filtering, and joining of tables. This is particularly useful when generating insights (e.g., aggregating data by industry and year) that feed into my visualization components.

- **Scalability and Extensibility:**  
  PostgreSQL is designed to scale well. It supports advanced indexing (e.g., for date columns), custom functions, and extensions—ensuring that it can grow with the demands of the project.

- **Community Support and Ecosystem:**  
  A mature ecosystem with extensive documentation, active community support, and a rich set of tools (e.g., psycopg2 for Python) makes PostgreSQL a practical and dependable choice.

## Datastore Setup in the Project

- **Schema Creation:**  
  A `schema.sql` file is provided to create the `ai_content_impact` table with appropriate data types and indexes. For example, the `published_date` column is indexed to accelerate time-based queries—essential for real-time visualizations.

- **Docker Integration:**  
  The PostgreSQL instance is containerized using Docker. The `docker-compose.yml` file is set up to start PostgreSQL with preset environment variables (database name, user, password) and automatically initialize the schema from `schema.sql`.

## Summary

PostgreSQL was selected for its strong data integrity, scalability, robust query capabilities, and ease of integration with Python applications. Its features directly support the requirements for efficient data ingestion, transformation, and real-time visualization.

