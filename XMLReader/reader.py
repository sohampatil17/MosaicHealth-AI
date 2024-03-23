import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime
import json
import numpy as np

def parse_xml(file_path):
    tree = ET.parse(file_path)
    return tree.getroot()

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

def process_records(root):
    data = {}

    for record in root.findall('.//Record'):
        rec_type = remove_prefix(record.get('type'), 'HKQuantityTypeIdentifier')
        rec_type = remove_prefix(rec_type, 'HKCategoryTypeIdentifier')

        if rec_type not in data:
            data[rec_type] = {'data_points': [], 'unit': record.get('unit')}

        value = record.get('value')
        try:
            value = float(value)
        except (ValueError, TypeError):
            continue

        date_str = record.get('startDate')
        date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S %z') if date_str else None

        data[rec_type]['data_points'].append({'date': date, 'value': value})

    return data

def calculate_trend(df, period_days):
    end_date = df.index.max()
    start_date = df.index.min()

    if end_date - start_date < pd.Timedelta(days=period_days * 2):
        return None  # Not enough data for the trend calculation

    current_period_end = end_date
    current_period_start = current_period_end - pd.Timedelta(days=period_days)
    previous_period_start = current_period_start - pd.Timedelta(days=period_days)
    previous_period_end = current_period_start

    current_period = df.loc[current_period_start:current_period_end]
    previous_period = df.loc[previous_period_start:previous_period_end]

    if previous_period['value'].mean() == 0:
        return None  # Avoid division by zero

    trend = ((current_period['value'].mean() - previous_period['value'].mean()) 
             / previous_period['value'].mean()) * 100
    return trend


def calculate_statistics(data):
    for key, value in data.items():
        if not value['data_points']:  # Skip if no data points
            continue

        df = pd.DataFrame(value['data_points'])
        if 'date' not in df.columns:  # Skip if 'date' column is missing
            continue

        df.set_index('date', inplace=True)
        df.sort_index(inplace=True)

        # Calculate basic statistics
        value['max'] = df['value'].max()
        value['min'] = df['value'].min()
        value['median'] = df['value'].median()
        value['mean'] = df['value'].mean()

        # Calculate trends
        value['1_month_trend'] = calculate_trend(df, 30)
        value['6_month_trend'] = calculate_trend(df, 180)

        # Convert NaNs to None
        for stat_key in ['max', 'min', 'median', 'mean', '1_month_trend', '6_month_trend']:
            if pd.isna(value[stat_key]):
                value[stat_key] = None

        # Remove raw data points if not needed
        del value['data_points']

    return data



def export_to_json(data, file_name):
    output = {
        "categories": list(data.keys()),
        "data": data
    }
    with open(file_name, 'w') as file:
        json.dump(output, file, indent=4, default=lambda x: x.isoformat() if isinstance(x, datetime) else x)

def main():
    root = parse_xml('export.xml')
    data = process_records(root)
    data_with_stats = calculate_statistics(data)
    export_to_json(data_with_stats, 'output.json')

if __name__ == "__main__":
    main()
