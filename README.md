## Nepal Pulse  

# Real-Time Knowledge Discovery Engine for Nepali News Streams

# Overview

Nepal Pulse is a real-time distributed data pipeline that collects news from multiple Nepali and English news websites, processes the data using Kafka and Python, applies machine learning (topic modeling), and displays insights through a live dashboard.

This project demonstrates a complete end-to-end system including:
- Data ingestion
- Streaming with Kafka
- Data processing
- Machine learning
- Visualization

---

# Architecture

News Websites
↓
Node.js Scraper (Ingestion)
↓
Kafka (raw-news)
↓
Python Processing
↓
Kafka (processed-news)
↓
Topic Modeling (ML)
↓
Streamlit Dashboard

---

## Technologies Used

- Node.js (TypeScript)
- Axios & Cheerio (Web scraping)
- Apache Kafka (Streaming)
- Docker (Containerization)
- Python
- kafka-python
- Scikit-learn (Machine Learning)
- Streamlit (Dashboard)
- Pandas

---

## Features

- Scrapes headlines from **20+ Nepali news websites**
- Real-time streaming using Kafka
- Cleans and normalizes text
- Topic modeling using LDA
- Interactive dashboard visualization
- Modular architecture

---

## Requirements

Install the following before running:

- Docker Desktop
- Node.js (v18+ recommended)
- Python 3
- Git

---

## STEP-BY-STEP TUTORIAL ON STARTING THE PROJECT
STEP 1
Clone the Repository
---
```bash
git clone https://github.com/rabin9863/nepal-pulse.git
cd nepal-pulse
---

STEP 2 
OPEN DOCKER DESKTOP IN BACKGROUND

STEP 3 
IN VSCODE 

run the command --- 

docker compose up -- build 

--------------------------

STEP 4
IN DOCKER DESKTOP 

Wait until you see the container named "nepal-pulse"

STEP 5
Open in browser:
http://localhost:8501



## How It Works

Scraper collects news headlines from websites
Sends data to Kafka topic raw-news
Python processor cleans and processes the data
Sends cleaned data to processed-news
Topic model extracts trending topics
Dashboard visualizes everything

## Dashboard Includes
Total processed articles
Source distribution
Language distribution
Trending topics
Latest news table
Frequent words chart

## Stop the Project
CTRL + C





## Project Structure
nepal-pulse/
├── ingestion/
├── processing/
├── dashboard/
├── docker-compose.yml
└── README.md
## Conclusion
Nepal Pulse demonstrates a complete real-time pipeline using:
distributed systems
streaming architecture
machine learning
visualization

## Author

Rabin Dhakal

---
