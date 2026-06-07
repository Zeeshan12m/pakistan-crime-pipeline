from airflow.decorators import dag, task
from datetime import datetime
import requests
import subprocess
import sys
import os

PROJECT_ROOT = "/opt/airflow/project"

@dag(
    dag_id="daily_crime_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="0 6 * * *",  # Every day at 6AM
    catchup=False,
    max_active_runs=1,
    tags=["crime", "scraper", "nlp", "daily"],
)
def daily_crime_pipeline():

    @task(task_id="run_scrapers")
    def run_scrapers():
        result = subprocess.run(
            [sys.executable, "-m", "scraper.run_all"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=1800
        )
        if result.returncode != 0:
            raise Exception(f"Scraper failed:\n{result.stderr}")
        print(result.stdout)
        return {"status": "success"}

    @task(task_id="run_nlp")
    def run_nlp(scraper_result):
        result = subprocess.run(
            [sys.executable, "-m", "nlp.run_nlp"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=600
        )
        if result.returncode != 0:
            raise Exception(f"NLP failed:\n{result.stderr}")
        print(result.stdout)
        return {"status": "success"}

    @task(task_id="run_knime_etl")
    def run_knime_etl(nlp_result):
        flask_url = "http://host.docker.internal:8005/run-knime"
        headers = {"X-API-Key": "pakistan-crime-key"}
        response = requests.post(flask_url, headers=headers, timeout=7200)
        response.raise_for_status()
        return response.json()

    @task(task_id="trigger_n8n_alerts")
    def trigger_n8n_alerts(knime_result):
        n8n_url = "http://host.docker.internal:5678/webhook/crime-alert"
        payload = {
            "message": "Daily crime pipeline completed",
            "source": "airflow",
            "knime_result": knime_result
        }
        response = requests.post(n8n_url, json=payload, timeout=300)
        response.raise_for_status()
        try:
            return response.json()
        except Exception:
            return {"status": "success"}

    scraper_out = run_scrapers()
    nlp_out = run_nlp(scraper_out)
    knime_out = run_knime_etl(nlp_out)
    trigger_n8n_alerts(knime_out)


daily_crime_pipeline()