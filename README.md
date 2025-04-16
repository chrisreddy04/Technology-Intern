
# Technology Intern Assessment Submission

## Overview

This repository contains a comprehensive submission for the Technology Intern Take-Home Assessment. The project demonstrates full-stack development capabilities by integrating data ingestion, transformation, and real-time visualization into a cohesive solution. The following components are included:

1. **Datastore Setup:**  
   - **PostgreSQL** is used as the datastore.
   - The `schema.sql` file contains the schema for the `ai_content_impact` table.
   - Docker is used to containerize the database, ensuring a consistent development and deployment environment.
   - The `docker-compose.yml` file sets up the PostgreSQL database and its dependencies.
   - The `docker-compose up` command can be used to start the database container.
   - The `docker-compose down` command can be used to stop and remove the database container.
   - Please refer datastore-setup.md file for detailed script.

2. **Data Ingestion:**  
   - The `data_ingest.py` script loads and transforms data from a CSV file (`Global_AI_Content_Impact_Dataset.csv`), and inserts it into PostgreSQL.
   - Data transformations include column renaming, type conversion, and handling of missing/erroneous data.
   - This batch process ensures the dataset is clean and ready for analysis.
   - Please refer data-ingestion.md file for detailed script.

3. **Data Visualization:**  
   - The `visualization.py` script builds a real-time dashboard using Plotly Dash.
   - Added aggregate_data metric to calculate the mean values for clear graph plotting.
   - Two key metrics are visualized:
     - **AI Adoption Rate Over Time by Industry**
     - **Job Loss Due to AI Over Time by Industry**
   - A user-controlled slider filters data by year, and the dashboard auto-refreshes every 5 seconds.
   - The dashboard is accessible at [http://localhost:8050] when running the Docker setup.
   - Please refer visualization.md file for detailed script.


