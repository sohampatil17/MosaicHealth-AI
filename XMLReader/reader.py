import xml.etree.ElementTree as ET
import modin.pandas as pd
#Intel Modin significantly enhances the performance of data processing tasks by distributing 
#them across multiple CPU cores, enabling parallel execution. 

#This is especially beneficial for busy doctors analyzing patient data, 
# as it drastically reduces the time required to compute and analyze large datasets from Apple Watches. 

#The reason we chose Modin is that operations that are traditionally 
#time-consuming in Pandas, such as data aggregation, filtering, and statistical calculations, 
#are executed much faster. This allows doctors to quickly access critical patient insights, our AI tools to
#run more efficiently and quicker, and also therefore facilitating more efficient decision-making and patient care.

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

# Some categories need to be averaged, while others are cumulative
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

#This method processes the records in the XML file, storing them as datapoints with a date
#This allows for efficient usage for statistics calculations later.
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
                
                if sleep_stage == "SleepAwakeTime":
                    duration_minutes = (end_time - start_time).total_seconds() / 60
                    unit = 'minutes'
                else:
                    duration_hours = (end_time - start_time).total_seconds() / 3600
                    unit = 'hours'

                date = start_time.date()
                if sleep_stage not in data:
                    data[sleep_stage] = {'data_points': {}, 'unit': unit, 'type': 'cumulative'}
                
                if unit == 'hours':
                    data[sleep_stage]['data_points'][date] = data[sleep_stage]['data_points'].get(date, 0) + duration_hours
                else:
                    data[sleep_stage]['data_points'][date] = data[sleep_stage]['data_points'].get(date, 0) + duration_minutes

                if 'SleepTime' not in data and sleep_stage != 'SleepAwakeTime':
                    data['SleepTime'] = {'data_points': {}, 'unit': 'hours', 'type': 'cumulative'}
                if sleep_stage != 'SleepAwakeTime':
                    data['SleepTime']['data_points'][date] = data['SleepTime']['data_points'].get(date, 0) + duration_hours

        else:
            if rec_type == "OxygenSaturation":
                try:
                    value = float(record.get('value')) * 100
                except (ValueError, TypeError):
                    continue
            else:
                try:
                    value = float(record.get('value'))
                except (ValueError, TypeError):
                    continue

            date_str = record.get('startDate')
            date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S %z').date() if date_str else None

            if rec_type not in data:
                data[rec_type] = {
                    'data_points': {}, 'unit': record.get('unit'), 
                    'type': 'average' if rec_type in average_categories else 'cumulative'
                }

            if rec_type in average_categories:
                day_data = data[rec_type]['data_points'].setdefault(date, {'total': 0, 'count': 0})
                day_data['total'] += value
                day_data['count'] += 1
            else:
                day_data = data[rec_type]['data_points'].setdefault(date, 0)
                data[rec_type]['data_points'][date] += value

    return data

#This calculates important statistics for physicians to use such as averages, weekly and monthly trends, and maxes and minimums.
def calculate_statistics(data):
    for key, value in data.items():
        if not value['data_points']:  # Skip if no data points
            continue

        # Prepare data for DataFrame - Here, Intel Modin helps speed up the DataFrame process drastically
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
                'max': round(period_df['value'].max(), 2),
                'min': round(period_df['value'].min(), 2),
                'median': round(period_df['value'].median(), 2),
                'mean': round(period_df['value'].mean(), 2)
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
            #% and +
            if trend is None:
                return None
            trend = round(trend, 1)
            if trend > 0:
                return f"+{trend}%"
            return f"{trend}%"

        # Last 1 week statistics and trend
        value['1 week'] = calculate_period_stats(df, 7)
        value['1 week']['trend'] = calculate_trend(df, 7)

        # Last 1 month statistics and trend
        value['1 month'] = calculate_period_stats(df, 30)
        value['1 month']['trend'] = calculate_trend(df, 30)

        # Last 3 months statistics and trend
        value['3 month'] = calculate_period_stats(df, 90)
        value['3 month']['trend'] = calculate_trend(df, 90)

        # Last 6 months statistics and trend
        value['6 month'] = calculate_period_stats(df, 180)
        value['6 month']['trend'] = calculate_trend(df, 180)

        # All-time statistics
        value['All time'] = calculate_period_stats(df)


        # Convert NaNs and 'nan%' to None in the stats
        for period in ['1 week', '1 month', '3 month', '6 month', 'All time']:
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
    # except where it follows another capital letter, a number, or already has a space.

    formatted_name = ""  # Start with an empty string

    for i in range(len(category_name)):
        if i > 0 and category_name[i].isupper() and not category_name[i-1].isupper() and category_name[i-1] != ' ':
            formatted_name += ' ' + category_name[i]
        else:
            formatted_name += category_name[i]

    return formatted_name

def main():
    root = parse_xml('export.xml')
    data = process_records(root)
    data_with_stats = calculate_statistics(data)
    export_to_json(data_with_stats, 'sample_output.json')

if __name__ == "__main__":
    main()
