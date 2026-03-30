# Manufacturing Anomaly Detection Platform

## Overview
This project is an end-to-end data pipeline that detects anomalies in manufacturing machine data. It generates synthetic data, processes it, detects abnormal behavior, and displays results through a dashboard.

## Features
- Synthetic data generation (normal, anomaly, missing values)
- Data ingestion from CSV
- Data cleaning and missing value handling
- Threshold-based anomaly detection
- Alert generation and logging
- MySQL database integration
- Dashboard for visualization
- CLI execution with performance tracking

## Project Structure
config/  
data/  
database/  
detection/  
alerts/  
utils/  
interface/  
main.py  
cli.py  

## How It Works
1. Generate synthetic machine data  
2. Read and process the data  
3. Detect anomalies based on thresholds  
4. Generate alerts  
5. Store data in MySQL  
6. Display results in dashboard  

## Technologies Used
Python  
Pandas  
MySQL  
Streamlit  

## Setup

1. Install dependencies  
pip install -r requirements.txt  

2. Configure database (.env file)  
DB_HOST=localhost  
DB_USER=root  
DB_PASSWORD=your_password  
DB_NAME=your_database  

## How to Run

1. Run the pipeline  
python cli.py  

2. Run the dashboard  
streamlit run interface/dashboard.py  

## Output
- Machine data stored in database  
- Alerts stored in database and log files  
- Dashboard shows summary and recent alerts