
import os
import numpy as np
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime

def transform_data(df):
   
   
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
    
    
    df['published_date'] = pd.to_datetime(df['published_date'], format='%Y').dt.date

    
   
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

    df = df.astype({
        'ai_adoption_rate': float,
        'ai_content_volume_tb': float,
        'job_loss_due_to_ai': float,
        'revenue_increase_due_to_ai': float,
        'human_ai_collab_rate': float,
        'consumer_trust_in_ai': float,
        'market_share_ai_companies': float
    })

    conn = psycopg2.connect(
        host=os.environ.get("DATABASE_HOST", "localhost"),
        dbname=os.environ.get("DATABASE_NAME", "mydatabase"),
        user=os.environ.get("DATABASE_USER", "myuser"),
        password=os.environ.get("DATABASE_PASSWORD", "mypassword")
    )
    cursor = conn.cursor()
    

    raw_data_tuples = df[[
        'country', 'published_date', 'industry', 'ai_adoption_rate',
        'ai_content_volume_tb', 'job_loss_due_to_ai', 'revenue_increase_due_to_ai',
        'human_ai_collab_rate', 'top_ai_tools_used', 'regulation_status',
        'consumer_trust_in_ai', 'market_share_ai_companies'
    ]].to_records(index=False)

    data_tuples = []
    for record in raw_data_tuples:
        new_record = []
        for item in record:
            if isinstance(item, np.datetime64):
                new_item = pd.Timestamp(item).to_pydatetime()
            elif isinstance(item, np.generic):
                new_item = item.item()
            else:
                new_item = item
            new_record.append(new_item)
        data_tuples.append(tuple(new_record))
   
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
