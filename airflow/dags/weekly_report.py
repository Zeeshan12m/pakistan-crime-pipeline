from airflow.decorators import dag, task
from datetime import datetime
import requests
import subprocess
import sys
import os
import glob
import pandas as pd

PROJECT_ROOT = "/opt/airflow/project"

@dag(
    dag_id="weekly_crime_report",
    start_date=datetime(2026, 1, 1),
    schedule="0 8 * * 0",  # Every Sunday at 8AM
    catchup=False,
    max_active_runs=1,
    tags=["crime", "weekly", "report"],
)
def weekly_crime_report():

    @task(task_id="generate_weekly_summary")
    def generate_weekly_summary():
        processed_dir = os.path.join(PROJECT_ROOT, "data", "processed")
        files = glob.glob(os.path.join(processed_dir, "aggregated_*.csv"))

        if not files:
            raise Exception("No aggregated CSV files found")

        dfs = []
        for f in files:
            df = pd.read_csv(f)
            dfs.append(df)

        combined = pd.concat(dfs, ignore_index=True)
        summary = combined.groupby("crime_type").agg(
            total_crimes=("crime_count", "sum"),
            avg_severity=("avg_severity", "mean")
        ).reset_index().sort_values("total_crimes", ascending=False)

        output_path = os.path.join(processed_dir, f"weekly_summary_{datetime.now().strftime('%Y%m%d')}.csv")
        summary.to_csv(output_path, index=False)
        print(f"Weekly summary saved to {output_path}")
        print(summary.to_string())
        return {"status": "success", "output": output_path}

    @task(task_id="notify_weekly_report")
    def notify_weekly_report(summary_result):
        n8n_url = "http://host.docker.internal:5678/webhook/weekly-report"
        payload = {
            "message": "Weekly crime report generated",
            "source": "airflow",
            "report_file": summary_result.get("output"),
        }
        response = requests.post(n8n_url, json=payload, timeout=300)
        try:
            return response.json()
        except Exception:
            return {"status": "success"}

    summary = generate_weekly_summary()
    notify_weekly_report(summary)


weekly_crime_report()