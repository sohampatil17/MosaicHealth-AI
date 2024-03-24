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
            }. Possible data types are "max", "min", "mean", "median", "trend" and possible data times are "1_week", "1_month", "3_month", "6_month", "all_time".
            Possible categories are "DietaryWater" or
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
        "content": "Good morning! I understand you've been experiencing some neck pain since yesterday. Could you describe the pain for me? Good morning. Yes, it started yesterday morning. It's a sharp pain, mostly at the back of my neck. It gets worse when I turn my head. I see. Have you done anything unusual that might have triggered this pain? Perhaps new exercises or a change in your sleeping position? Not that I can recall. I've been following my usual routine, though I did spend a few extra hours at my desk working on my computer yesterday. That could be a contributing factor. Poor posture or prolonged periods in one position can lead to neck strain. Have you taken any medication for the pain? I took some over-the-counter pain relief last night. It helped a little, but the pain is still there, especially when I move. Alright. It's good that you took steps to manage the pain. For now, I recommend continuing with the pain relief as needed, but let's also add some gentle neck stretches to your routine. Additionally, ensure your workstation is ergonomically set up to prevent straining your neck further. I'll do that. Should I be worried about the pain, or will it likely go away on its own? Neck pain like this is often due to muscle strain and usually resolves with proper care. However, if the pain persists for more than a week or worsens, I'd like you to come back for a follow-up. We may need to conduct further tests to rule out other causes. Got it. I'll follow your advice and keep an eye on the pain. Thank you for your help. You're welcome! Remember to take breaks, stretch, and adjust your posture while working. If there's anything else or if the pain intensifies, don't hesitate to contact me. Take care!"
    }
]


result = pg.Chat.create(
model="Neural-Chat-7B",
messages=messages
)


content = result['choices'][0]['message']['content']
print(content)
# print(json.dumps(result['output'], sort_keys=True, indent=4, separators=(',', ': ')))
