KNIME ETL Workflow — Pakistan Crime Pipeline

Input:  data/processed/extracted_YYYYMMDD.csv
Output: data/processed/cleaned_YYYYMMDD.csv
        data/processed/aggregated_YYYYMMDD.csv

Nodes in order:
1. CSV Reader
2. Rule Engine (fill missing city)
3. String Manipulation (standardize crime_type)
4. Duplicate Row Filter
5. Joiner (geo-tag from cities reference)
6. GroupBy (aggregate by city)
7. CSV Writer x2