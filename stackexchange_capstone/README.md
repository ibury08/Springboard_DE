# StackExchange API - A data pipeline for NLP
## Project Overview
StackExchange is a network of question-and-answer websites on topics in diverse fields, each site covering a specific topic, where questions, answers, and users are subject to a reputation award process. Anecdotal user feedback, however, indicates that some communities and users are hostile and unhelpful to those seeking help. This project aims to enable whoever wants to use sentiment analysis or other NLP approaches on historical post and comment data to identify positive/negative communities.
### Data Model
<div><img width="50%" src = "https://github.com/ibury08/Springboard_DE/blob/pipeline-dev/stackexchange_capstone/se.png"></div>

## Getting Started
Historical data - found <a href="https://archive.org/details/stackexchange">here</a>. <br>
Live data - using <a href="https://api.stackexchange.com/docs">StackExchange API</a>. An a registered application will be necessary to secure credentials in order to run this pipeline

### Running the pipeline
1. Clone repository & `pip install -r requirements.txt`
2. Create credentials file `.envs.json`. This pipeline currently looks in your current working directory for this file. This file should contain:
{<br>
    "alert_email": <b>\<your-email\></b>,<br>
  "access_token": <b>\<StackExchange API access token\></b>,<br>
  "key": <b>\<StackExchange application key\></b><br>
}
3. Start Airflow - `aiflow webserver && airflow scheduler`
4. Copy api_ingest.py into Airflow DAGs folder - e.g. `cp stackexchange_capstone/api_ingest.py ~/airflow/dags/api_ingest.py`
5. Setting the DAG active should create 5 parquet files (one for each object) per day in your root directory (or pwd depending on your system config)
