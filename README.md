# Pakistan Crime & Safety Data Pipeline

## Project Overview

The Pakistan Crime & Safety Data Pipeline is an automated data engineering solution that collects crime-related news from major Pakistani news websites, processes the data using NLP techniques, performs ETL transformations, generates automated alerts, and visualizes crime trends through an interactive dashboard.

## Objectives

* Collect crime news from multiple sources.
* Extract structured crime information using NLP.
* Clean and transform data through ETL workflows.
* Generate automated crime alerts.
* Visualize crime trends and hotspots across Pakistan.

## Technologies Used

* Python
* Selenium
* BeautifulSoup
* spaCy
* NLTK
* RapidFuzz
* KNIME
* Apache Airflow
* n8n
* Streamlit
* Docker (Optional Deployment)

## Data Sources

* Dawn News
* Geo News
* Express Tribune

## Pipeline Workflow

1. Scrape crime-related news articles.
2. Extract crime type, city, severity, and date.
3. Remove duplicates and clean data.
4. Perform ETL processing in KNIME.
5. Schedule workflows using Airflow.
6. Generate alerts using n8n.
7. Display insights through a Streamlit dashboard.

## Features

* Automated news collection
* Crime classification
* City extraction
* Duplicate detection
* Crime trend analysis
* Crime hotspot visualization
* Automated Email/WhatsApp alerts
* Interactive dashboard

## Survey Validation

A Google Forms survey was conducted with 14 respondents.

### Key Findings

* 78.6% showed interest in a crime dashboard.
* 71.4% actively follow crime news.
* 64.3% preferred automated alerts.
* 100% currently track crime information manually.
* More than 70% wanted Email/WhatsApp crime notifications.

## Results

* 41 articles collected
* 25 unique articles after deduplication
* 22 relevant crime records extracted
* 12 automated alerts generated
* Crime trends visualized by city and category

## Project Team

* M. Zeeshan Zahid – Web Scraping , n8n
* M. Yahya – NLP & ETL Processing
* Syed Minhal Naqvi – Airflow & Dashboard Development

## Future Enhancements

* Real-time data streaming
* Urdu language support
* Mobile application integration
* Advanced predictive crime analytics

## Conclusion

This project demonstrates how modern data engineering tools can be integrated to build an automated crime intelligence platform that helps users monitor crime trends, receive alerts, and make informed decisions based on data-driven insights.
