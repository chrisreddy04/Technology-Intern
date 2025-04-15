DROP TABLE IF EXISTS ai_content_impact;

CREATE TABLE ai_content_impact (
    id SERIAL PRIMARY KEY,
    country VARCHAR(100) NOT NULL,
    published_date TIMESTAMP NOT NULL,
    industry VARCHAR(100) NOT NULL,
    ai_adoption_rate NUMERIC(5,2) NOT NULL,
    ai_content_volume_tb NUMERIC(10,2) NOT NULL,
    job_loss_due_to_ai NUMERIC(5,2) NOT NULL,
    revenue_increase_due_to_ai NUMERIC(5,2) NOT NULL,       
    human_ai_collab_rate NUMERIC(5,2) NOT NULL,         
    regulation_status VARCHAR(50) NOT NULL,                
    consumer_trust_in_ai NUMERIC(5,2) NOT NULL,             
    market_share_ai_companies NUMERIC(5,2) NOT NULL 

);

-- Indexes to optimize querying for real-time benefits
CREATE INDEX idx_published_date ON ai_content_impact (published_date);
CREATE INDEX idx_country ON ai_content_impact (country);
CREATE INDEX idx_industry ON ai_content_impact (industry);