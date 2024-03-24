import os
import json
import predictionguard as pg


os.environ["PREDICTIONGUARD_TOKEN"] = "q1VuOjnffJ3NO2oFN8Q9m8vghYc84ld13jaqdF7E"

messages = [
    {
        "role": "system",
        "content": """You are a helpful medical data assistant. Your job is to understand the doctor-patient interaction and output relevant data needed strictly in the format of- 
            {
                "reasoning": "",
                "category": "",
                "data1_time": "",
                "data1_type": "",
                "data2_time": "",
                "data2_type": ""
            }. Possible data types are "max", "min", "mean", "median", "trend" and possible data times are "1_week", "1_month", "3_month", "6_month", "all_time" and possible categories are "DietaryWater" or
            "BodyMassIndex" or
            "Height" or
            "BodyMass" or
            "HeartRate" or
            "OxygenSaturation" or
            "BloodPressureSystolic" or
            "BloodPressureDiastolic" or
            "RespiratoryRate" or
            "StepCount" or
            "DistanceWalkingRunning" or
            "BasalEnergyBurned" or
            "ActiveEnergyBurned" or
            "FlightsClimbed" or
            "DietaryFatTotal" or
            "DietaryFatPolyunsaturated" or
            "DietaryFatMonounsaturated" or
            "DietaryFatSaturated" or
            "DietaryCholesterol" or
            "DietarySodium" or
            "DietaryCarbohydrates" or
            "DietaryFiber" or
            "DietarySugar" or
            "DietaryEnergyConsumed" or
            "DietaryProtein" or
            "DietaryVitaminC" or
            "DietaryCalcium" or
            "DietaryIron" or
            "DietaryPotassium" or
            "NumberOfTimesFallen" or
            "AppleExerciseTime" or
            "DietaryCaffeine" or
            "DistanceCycling" or
            "DistanceSwimming" or
            "SwimmingStrokeCount" or
            "RestingHeartRate" or
            "VO2Max" or
            "WalkingHeartRateAverage" or
            "EnvironmentalAudioExposure" or
            "WalkingDoubleSupportPercentage" or
            "SixMinuteWalkTestDistance" or
            "AppleStandTime" or
            "WalkingAsymmetryPercentage" or
            "StairAscentSpeed" or
            "StairDescentSpeed" or
            "SleepDurationGoal" or
            "AppleWalkingSteadiness" or
            "RunningStrideLength" or
            "RunningVerticalOscillation" or
            "RunningGroundContactTime" or
            "HeartRateRecoveryOneMinute" or
            "RunningPower" or
            "EnvironmentalSoundReduction" or
            "RunningSpeed" or
            "TimeInDaylight" or
            "PhysicalEffort" or
            "SleepAnalysis" or
            "AppleStandHour" or
            "MindfulSession" or
            "HighHeartRateEvent" or
            "LowHeartRateEvent" or
            "AudioExposureEvent" or
            "ToothbrushingEvent" or
            "HeadphoneAudioExposureEvent" or
            "HandwashingEvent" or
            "HeartRateVariabilitySDNN"
            . Ensure outputted data is in the format of {
                "reasoning": "add reason here",
                "category": "add category from the list I gave you earlier",
                "data1_time": "add data time from options I gave you here",
                "data1_type": "add data type from options I gave you here",
                "data2_time": "add data time from options I gave you here",
                "data2_type": "add data type from options I gave you here"
            } and that categories are only from the ones I listed."""
    },
    {
        "role": "user",
        "content": "Good morning! I understand you've been concerned about your sugar levels recently. Can you tell me more about what's been happening? Good morning, Doctor. Yes, I've noticed some unusual fluctuations in my sugar levels since yesterday. It's been quite erratic, and I'm worried because it usually stays within a normal range. I see. Have there been any changes in your diet, exercise routine, or stress levels that might have influenced your sugar levels? Not significantly. I've been sticking to my usual diet and exercise regimen. The only difference is I've been under a bit of stress at work lately. Stress can indeed impact your sugar levels. Have you been monitoring your levels regularly at home? Yes, I've been checking my sugar levels, and I noticed the fluctuations started yesterday morning. The readings were higher than usual. It's good that you're keeping a close eye on it. For now, I recommend continuing to monitor your sugar levels closely. Let's also explore some stress management techniques to see if that helps stabilize your levels. I can do that. Should I be making any immediate changes to my diet or exercise routine? For now, stick to your current routine, but let's review it during your next visit to ensure it's optimal for managing your sugar levels. If your readings continue to be erratic or if they increase, please let me know immediately. Will do, Doctor. Thank you for your guidance. You're welcome! Remember, managing stress is just as important as diet and exercise in controlling your sugar levels. If there's anything else you're concerned about or if you notice any other unusual symptoms, don't hesitate to get in touch. Take care!" }
]


result = pg.Chat.create(
model="Neural-Chat-7B",
messages=messages
)


content = result['choices'][0]['message']['content']
print(content)
# print(json.dumps(result['output'], sort_keys=True, indent=4, separators=(',', ': ')))
