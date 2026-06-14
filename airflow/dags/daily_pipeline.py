from airflow.decorators import dag, task
from datetime import datetime
import requests

FLASK_BASE = "http://host.docker.internal:8005"
HEADERS = {"X-API-Key": "pakistan-crime-key"}

@dag(
    dag_id="daily_crime_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="0 6 * * *",
    catchup=False,
    max_active_runs=1,
    tags=["crime", "scraper", "nlp", "daily"],
)
def daily_crime_pipeline():

    @task(task_id="run_scrapers")
    def run_scrapers():
        resp = requests.post(f"{FLASK_BASE}/run-scrapers", headers=HEADERS, timeout=1800)
        data = resp.json()
        if data.get("status") != "success":
            raise Exception(f"Scrapers failed: {data}")
        print(data.get("stdout", ""))
        return {"status": "success"}

    @task(task_id="run_nlp")
    def run_nlp(scraper_result):
        resp = requests.post(f"{FLASK_BASE}/run-nlp", headers=HEADERS, timeout=600)
        data = resp.json()
        if data.get("status") != "success":
            raise Exception(f"NLP failed: {data}")
        print(data.get("stdout", ""))
        return {"status": "success"}

    @task(task_id="run_knime_etl")
    def run_knime_etl(nlp_result):
        resp = requests.post(f"{FLASK_BASE}/run-knime", headers=HEADERS, timeout=7200)
        data = resp.json()
        if data.get("status") != "success":
            raise Exception(f"KNIME failed: {data}")
        return {"status": "success"}

    @task(task_id="trigger_n8n_alerts")
    def trigger_n8n_alerts(knime_result):
        n8n_url = "http://host.docker.internal:5678/webhook/crime-alert"
        resp = requests.post(n8n_url, json={"source": "airflow"}, timeout=300)
        try:
            return resp.json()
        except Exception:
            return {"status": "success"}

    scraper_out = run_scrapers()
    nlp_out = run_nlp(scraper_out)
    knime_out = run_knime_etl(nlp_out)
    trigger_n8n_alerts(knime_out)


daily_crime_pipeline()