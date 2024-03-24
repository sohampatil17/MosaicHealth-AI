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
    watch_prioritized_categories = [
        "StepCount", "DistanceWalkingRunning", "ActiveEnergyBurned",
        "FlightsClimbed", "AppleExerciseTime", "DistanceCycling",
        "DistanceSwimming", "SwimmingStrokeCount", "WalkingSpeed",
        "WalkingStepLength", "RunningStrideLength", "RunningSpeed",
        "EnvironmentalAudioExposure", "HeadphoneAudioExposure"
    ]
    #Remove the average categories from this, as it doesn't matter that they are doubled
    watch_prioritized_categories = list(set(watch_prioritized_categories) - set(average_categories))

    prefixes = ["HKQuantityTypeIdentifier", "HKCategoryTypeIdentifier", "HKDataType"]

    for record in root.findall('.//Record'):
        rec_type = remove_prefix(record.get('type'), prefixes)
        device_info = record.get('device', '')

        # Skip data from non-Apple Watch sources for prioritized categories
        if rec_type in watch_prioritized_categories and "model:Watch" not in device_info:
            continue

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
            day_data = data[rec_type]['data_points'].setdefault(date, 0)
            data[rec_type]['data_points'][date] += value

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
            return round(trend, 3)

        # Last 1 week statistics and trend
        value['1_week'] = calculate_period_stats(df, 7)
        value['1_week']['trend'] = calculate_trend(df, 7)

        # Last 1 month statistics and trend
        value['1_month'] = calculate_period_stats(df, 30)
        value['1_month']['trend'] = calculate_trend(df, 30)

        # Last 3 months statistics and trend
        value['3_month'] = calculate_period_stats(df, 90)
        value['3_month']['trend'] = calculate_trend(df, 90)

        # Last 6 months statistics and trend
        value['6_month'] = calculate_period_stats(df, 180)
        value['6_month']['trend'] = calculate_trend(df, 180)

        # All-time statistics
        value['all_time'] = calculate_period_stats(df)


        # Convert NaNs to None in the stats
        for period in ['1_week', '1_month', '3_month', '6_month', 'all_time']:
            for stat_key in value[period]:
                if pd.isna(value[period][stat_key]):
                    value[period][stat_key] = None

        ## Count data points by year and recent periods
        #value['datapoint_count'] = df['value'].groupby(df.index.year).count().to_dict()
        #current_date = pd.to_datetime('today', utc=True) if df.index.tz is not None else pd.to_datetime('today')
        #value['datapoint_count']['last_6_months'] = df.loc[current_date - pd.DateOffset(months=6):].shape[0]
        #value['datapoint_count']['last_1_month'] = df.loc[current_date - pd.DateOffset(months=1):].shape[0]

        # Remove raw data points
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
