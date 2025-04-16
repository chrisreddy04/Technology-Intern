# Visualization

## Overview

This document explains how to view and interact with the real-time dashboard created for the project. The dashboard is built using Plotly Dash and displays key trends such as AI Adoption Rate and Job Loss Due to AI over time by industry.

## How It Works

### Dashboard Components

1. **Graphs:**
   - **AI Adoption Rate Over Time:**  
     Displays a line chart showing the AI adoption rate by industry. Data is aggregated by year, ensuring continuous lines for each industry.
   - **Job Loss Due to AI Over Time:**  
     Displays a line chart with a percentage (%) label on the y-axis. This chart shows the average job loss due to AI by industry over time.
     
2. **Slider Filtering:**
   - The dashboard includes a year slider that allows users to filter the data up to a selected year.
   - Users can adjust the slider to observe trends for different time periods. The charts update dynamically based on this selection.

3. **Auto Refresh:**
   - An interval component refreshes the charts every 5 seconds to ensure that the latest data from the database is displayed in real time.

## How to View the Dashboard

- **Locally:**  
  If you’re running the application locally (or within Docker), the dashboard can be accessed via your web browser at:
  
  [http://localhost:8050]
  
## Screenshot

A screenshot of the dashboard is included in the repository as `dashboard-1.png` and `dashboard-2.png`.

## Running the Dashboard

- **Docker Environment:**  
  In Docker setup, the dashboard is part of the `dashboard` service. To launch the dashboard, run:

  ```bash
  docker-compose up --build dashboard
