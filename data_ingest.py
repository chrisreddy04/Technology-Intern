# data_ingest.py
import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime

def transform_data(df):
   
    # Rename columns based on our mapping
    df = df.rename(columns={
        'Country': 'country',
        'Year': 'published_date',  
        'Industry': 'industry',
        'AI Adoption Rate (%)': 'ai_adoption_rate',
        'AI-Generated Content Volume (TBs per year)': 'ai_content_volume_tb',
        'Job Loss Due to AI (%)': 'job_loss_due_to_ai',
        'Revenue Increase Due to AI (%)': 'revenue_increase_due_to_ai',
        'Human-AI Collaboration Rate (%)': 'human_ai_collab_rate',
        'Top AI Tools Used': 'top_ai_tools_used',
        'Regulation Status': 'regulation_status',
        'Consumer Trust in AI (%)': 'consumer_trust_in_ai',
        'Market Share of AI Companies (%)': 'market_share_ai_companies'
    })
    
    
    df['published_date'] = df['published_date'].apply(lambda x: datetime(int(x), 1, 1))
    
   
    numeric_columns = [
        'ai_adoption_rate', 'ai_content_volume_tb', 'job_loss_due_to_ai',
        'revenue_increase_due_to_ai', 'human_ai_collab_rate',
        'consumer_trust_in_ai', 'market_share_ai_companies'
    ]
    
   
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
   
    df = df.dropna(subset=['country', 'published_date', 'industry'] + numeric_columns)
    
    return df

def insert_data(df):
   
    conn = psycopg2.connect(
        host=os.environ.get("DATABASE_HOST", "localhost"),
        dbname=os.environ.get("DATABASE_NAME", "mydatabase"),
        user=os.environ.get("DATABASE_USER", "myuser"),
        password=os.environ.get("DATABASE_PASSWORD", "mypassword")
    )
    cursor = conn.cursor()
    
    # Prepare tuples from the DataFrame
    data_tuples = list(df[['country', 'published_date', 'industry', 'ai_adoption_rate',
                             'ai_content_volume_tb', 'job_loss_due_to_ai',
                             'revenue_increase_due_to_ai', 'human_ai_collab_rate',
                             'top_ai_tools_used', 'regulation_status',
                             'consumer_trust_in_ai', 'market_share_ai_companies'
                            ]].to_records(index=False))
   
    insert_query = """
        INSERT INTO ai_content_impact (
            country, published_date, industry, ai_adoption_rate,
            ai_content_volume_tb, job_loss_due_to_ai, revenue_increase_due_to_ai,
            human_ai_collab_rate, top_ai_tools_used, regulation_status,
            consumer_trust_in_ai, market_share_ai_companies
        ) VALUES %s
    """
    execute_values(cursor, insert_query, data_tuples)
    conn.commit()
    cursor.close()
    conn.close()
    print("Data ingestion complete!")

if __name__ == "__main__":
   
    csv_file = "Global_AI_Content_Impact_Dataset.csv"
    
    try:
       
        df = pd.read_csv(csv_file)
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        exit(1)
    
   
    transformed_df = transform_data(df)

    insert_data(transformed_df)
