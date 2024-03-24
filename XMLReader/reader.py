import xml.etree.ElementTree as ET
import modin.pandas as pd
from datetime import datetime
import json
import numpy as np

def parse_xml(file_path):
    tree = ET.parse(file_path)
    return tree.getroot()

def remove_prefix(text, prefixes):
    for prefix in prefixes:
        if text.startswith(prefix):
            return text[len(prefix):]
    return text


average_categories = [
    "BodyMassIndex", "Height", "BodyMass", "HeartRate", "OxygenSaturation",
    "BloodPressureSystolic", "BloodPressureDiastolic", "RespiratoryRate", 
    "RestingHeartRate", "VO2Max", "WalkingHeartRateAverage", "EnvironmentalAudioExposure",
    "HeadphoneAudioExposure", "WalkingDoubleSupportPercentage", "SixMinuteWalkTestDistance", 
    "WalkingSpeed", "WalkingStepLength", "WalkingAsymmetryPercentage",
    "StairAscentSpeed", "StairDescentSpeed", "HKDataTypeSleepDurationGoal",
    "AppleWalkingSteadiness", "RunningStrideLength", "RunningVerticalOscillation",
    "RunningGroundContactTime", "HeartRateRecoveryOneMinute", "RunningPower",
    "EnvironmentalSoundReduction", "RunningSpeed", "PhysicalEffort",
    "SleepAnalysis", "AppleStandHour", "MindfulSession", "HighHeartRateEvent",
    "LowHeartRateEvent", "AudioExposureEvent",
    "HeadphoneAudioExposureEvent", "HeartRateVariabilitySDNN"
]

def process_records(root):
    data = {}
    watch_prioritized_categories = [
        "StepCount", "DistanceWalkingRunning", "ActiveEnergyBurned",
        "FlightsClimbed", "AppleExerciseTime", "DistanceCycling",
        "DistanceSwimming", "SwimmingStrokeCount", "WalkingSpeed",
        "WalkingStepLength", "RunningStrideLength", "RunningSpeed",
        "EnvironmentalAudioExposure", "HeadphoneAudioExposure"
    ]
    watch_prioritized_categories = list(set(watch_prioritized_categories) - set(average_categories))

    prefixes = ["HKQuantityTypeIdentifier", "HKCategoryTypeIdentifier", "HKDataType"]

    sleep_stage_mapping = {
        "HKCategoryValueSleepAnalysisAsleepREM": "REM Sleep",
        "HKCategoryValueSleepAnalysisAsleepDeep": "DeepSleep",
        "HKCategoryValueSleepAnalysisAsleepCore": "CoreSleep",
        "HKCategoryValueSleepAnalysisAwake": "SleepAwakeTime"
    }

    for record in root.findall('.//Record'):
        rec_type = remove_prefix(record.get('type'), prefixes)
        device_info = record.get('device', '')

        if rec_type in watch_prioritized_categories and "model:Watch" not in device_info:
            continue

        if 'SleepAnalysis' in rec_type and record.get('sourceVersion', '') >= "9.1":
            sleep_stage_key = record.get('value')
            sleep_stage = sleep_stage_mapping.get(sleep_stage_key, None)
            if sleep_stage:
                start_time = datetime.strptime(record.get('startDate'), '%Y-%m-%d %H:%M:%S %z')
                end_time = datetime.strptime(record.get('endDate'), '%Y-%m-%d %H:%M:%S %z')
                duration_hours = (end_time - start_time).total_seconds() / 3600

                if sleep_stage not in data:
                    data[sleep_stage] = {'data_points': {}, 'unit': 'hours', 'type': 'cumulative'}
                
                date = start_time.date()
                data[sleep_stage]['data_points'][date] = data[sleep_stage]['data_points'].get(date, 0) + duration_hours

        else:
            rec_type = remove_prefix(record.get('type'), prefixes)

            if rec_type not in data:
                data[rec_type] = {
                    'data_points': {}, 'unit': record.get('unit'), 
                    'type': 'average' if rec_type in average_categories else 'cumulative'
                }

            value = record.get('value')
            try:
                value = float(value)
            except (ValueError, TypeError):
                continue

            date_str = record.get('startDate')
            date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S %z').date() if date_str else None

            if rec_type in average_categories:
                day_data = data[rec_type]['data_points'].setdefault(date, {'total': 0, 'count': 0})
                day_data['total'] += value
                day_data['count'] += 1
            else:
                day_data = data[rec_type]['data_points'].setdefault(date, 0)
                data[rec_type]['data_points'][date] += value

    # Calculate total sleep time
    total_sleep_categories = ["REMSleep", "DeepSleep", "CoreSleep"]
    for date in data.get("REMSleep", {'data_points': {}})['data_points']:
        total_sleep = sum(data[cat]['data_points'].get(date, 0) for cat in total_sleep_categories)
        if "SleepTime" not in data:
            data["SleepTime"] = {'data_points': {}, 'unit': 'hours', 'type': 'cumulative'}
        data["SleepTime"]['data_points'][date] = total_sleep

    return data



def calculate_statistics(data):
    for key, value in data.items():
        if not value['data_points']:  # Skip if no data points
            continue

        # Prepare data for DataFrame
        prepared_data = []
        for date, stats in value['data_points'].items():
            if value['type'] == 'average':
                avg_value = stats['total'] / stats['count'] if stats['count'] > 0 else 0
                prepared_data.append({'date': date, 'value': avg_value})
            else:
                prepared_data.append({'date': date, 'value': stats})

        df = pd.DataFrame(prepared_data)
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        df.sort_index(inplace=True)

        # Function to calculate statistics for a given time period
        def calculate_period_stats(df, days=None):
            if days:
                period_df = df.last(f"{days}D")
            else:
                period_df = df

            return {
                'max': round(period_df['value'].max(), 3),
                'min': round(period_df['value'].min(), 3),
                'median': round(period_df['value'].median(), 3),
                'mean': round(period_df['value'].mean(), 3)
            }

        # Function to calculate trend
        def calculate_trend(df, days):
            current_date = pd.to_datetime('today')
            prev_date = current_date - pd.DateOffset(days=days)
            earlier_date = prev_date - pd.DateOffset(days=days)

            current_period = df.loc[prev_date:current_date]
            earlier_period = df.loc[earlier_date:prev_date]

            if earlier_period['value'].mean() == 0:
                return None  # Avoid division by zero

            trend = ((current_period['value'].mean() - earlier_period['value'].mean()) 
                     / earlier_period['value'].mean()) * 100
            return f"{round(trend, 1)}%"

        # Last 1 week statistics and trend
        value['Previous week'] = calculate_period_stats(df, 7)
        value['Previous week']['trend'] = calculate_trend(df, 7)

        # Last 1 month statistics and trend
        value['Last month'] = calculate_period_stats(df, 30)
        value['Last month']['trend'] = calculate_trend(df, 30)

        # Last 3 months statistics and trend
        value['Last three months'] = calculate_period_stats(df, 90)
        value['Last three months']['trend'] = calculate_trend(df, 90)

        # Last 6 months statistics and trend
        value['Last six months'] = calculate_period_stats(df, 180)
        value['Last six months']['trend'] = calculate_trend(df, 180)

        # All-time statistics
        value['All time'] = calculate_period_stats(df)


        # Convert NaNs and 'nan%' to None in the stats
        for period in ['Previous week', 'Last month', 'Last three months', 'Last six months', 'All time']:
            for stat_key in value[period]:
                if pd.isna(value[period][stat_key]) or value[period][stat_key] == 'nan%':
                    value[period][stat_key] = None


        # Remove raw data points
        del value['data_points']

    return data

def export_to_json(data, file_name):
    # Exports the data to a JSON file
    output = {
        "categories": [format_category_name(cat) for cat in data.keys()],
        "data": {format_category_name(cat): value for cat, value in data.items()}
    }
    with open(file_name, 'w') as file:
        json.dump(output, file, indent=4, default=lambda x: x.isoformat() if isinstance(x, datetime) else x)

def format_category_name(category_name):
    # Adds spaces before each capital letter in the category name,
    # except where it follows another capital letter or a number.

    formatted_name = ""  # Start with an empty string

    for i in range(len(category_name)):
        if i > 0 and category_name[i].isupper() and not category_name[i-1].isupper():
            formatted_name += ' ' + category_name[i]
        else:
            formatted_name += category_name[i]

    return formatted_name

def main():
    root = parse_xml('export.xml')
    data = process_records(root)
    data_with_stats = calculate_statistics(data)
    export_to_json(data_with_stats, 'output.json')

if __name__ == "__main__":
    main()
