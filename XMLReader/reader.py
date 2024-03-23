import xml.etree.ElementTree as ET
import modin.pandas as pd
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

average_categories = [
    "BodyMassIndex", "Height", "BodyMass", "HeartRate", "OxygenSaturation",
    "BloodPressureSystolic", "BloodPressureDiastolic", "RespiratoryRate", 
    "DietaryFatTotal", "DietaryFatPolyunsaturated", "DietaryFatMonounsaturated", 
    "DietaryFatSaturated", "DietaryCholesterol", "DietarySodium", "DietaryCarbohydrates",
    "DietaryFiber", "DietarySugar", "DietaryEnergyConsumed", "DietaryProtein", 
    "DietaryVitaminC", "DietaryCalcium", "DietaryIron", "DietaryPotassium", 
    "RestingHeartRate", "VO2Max", "WalkingHeartRateAverage", "EnvironmentalAudioExposure",
    "HeadphoneAudioExposure", "WalkingDoubleSupportPercentage", "SixMinuteWalkTestDistance",
    "AppleStandTime", "WalkingSpeed", "WalkingStepLength", "WalkingAsymmetryPercentage",
    "StairAscentSpeed", "StairDescentSpeed", "HKDataTypeSleepDurationGoal",
    "AppleWalkingSteadiness", "RunningStrideLength", "RunningVerticalOscillation",
    "RunningGroundContactTime", "HeartRateRecoveryOneMinute", "RunningPower",
    "EnvironmentalSoundReduction", "RunningSpeed", "TimeInDaylight", "PhysicalEffort",
    "SleepAnalysis", "AppleStandHour", "MindfulSession", "HighHeartRateEvent",
    "LowHeartRateEvent", "AudioExposureEvent", "ToothbrushingEvent",
    "HeadphoneAudioExposureEvent", "HandwashingEvent", "HeartRateVariabilitySDNN"
]

def process_records(root):
    data = {}

    for record in root.findall('.//Record'):
        rec_type = remove_prefix(record.get('type'), 'HKQuantityTypeIdentifier')
        rec_type = remove_prefix(rec_type, 'HKCategoryTypeIdentifier')

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
            # Average: Recalculate the average for the day
            day_data = data[rec_type]['data_points'].setdefault(date, {'total': 0, 'count': 0})
            day_data['total'] += value
            day_data['count'] += 1
        else:
            # Cumulative: Add to the day's total
            data[rec_type]['data_points'][date] = data[rec_type]['data_points'].get(date, 0) + value

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

        # Count data points by year and recent periods
        value['datapoint_count'] = df['value'].groupby(df.index.year).count().to_dict()
        current_date = pd.to_datetime('today', utc=True) if df.index.tz is not None else pd.to_datetime('today')
        value['datapoint_count']['last_6_months'] = df.loc[current_date - pd.DateOffset(months=6):].shape[0]
        value['datapoint_count']['last_1_month'] = df.loc[current_date - pd.DateOffset(months=1):].shape[0]

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
