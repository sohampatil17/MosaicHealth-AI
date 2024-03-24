import os
import json
import predictionguard as pg


os.environ["PREDICTIONGUARD_TOKEN"] = "q1VuOjnffJ3NO2oFN8Q9m8vghYc84ld13jaqdF7E"

transcript = "good morning doctor its been a few weeks since my knee surgery and i wanted to check in on my recovery progress..."

messages = [
    {
        "role": "system",
        "content": """You are a helpful medical data assistant. Your job is to understand the doctor-patient interaction an array of two data objects to extract important health data relating to a patients condition
            Example1 input: "Patient looks pale and is experiencing shortness of breath"
            Example1 output:
            [
                {
                    reasoning: "Mentioned muscle pain which can be caused by vitamin d deficiency",
                    category: "Time In Daylight",
                    data1_time: "6 month",
                    data1_type: "mean",
                    data2_time: "3 month",
                    data2_type: "trend"
                },
                {
                    reasoning: "Shortness of breath might indicate oxygen issues",
                    category: "Oxygen Saturation",
                    data1_time: "1 week",
                    data1_type: "min",
                    data2_time: "6 month",
                    data2_type: "mean"
                }
            ]

            Example2 Input: "Patient is experiencing rapid weight gain and feels constantly tired"
            Example2 Output:
            [
                {
                    "reasoning": "Constant fatigue could be related to poor sleep quality",
                    "category": "Sleep Time",
                    "data1_time": "1 month",
                    "data1_type": "min",
                    "data2_time": "1 week",
                    "data2_type": "mean"
                },
                {
                    "reasoning": "Weight gain might also affect heart health",
                    "category": "Resting Heart Rate",
                    "data1_time": "3 month",
                    "data1_type": "max",
                    "data2_time": "1 month",
                    "data2_type": "mean"
                }
            ]

            Example3 Input: "Patient has been feeling very anxious and has trouble sleeping"
            Example3 Output:
            [
                {
                    "reasoning": "Anxiety can elevate heart rate",
                    "category": "Heart Rate",
                    "data1_time": "1 week",
                    "data1_type": "mean",
                    "data2_time": "1 month",
                    "data2_type": "trend"
                },
                {
                    "reasoning": "Trouble sleeping might indicate irregular sleep patterns",
                    "category": "Sleep Time",
                    "data1_time": "1 week",
                    "data1_type": "min",
                    "data2_time": "6 month",
                    "data2_type": "mean"
                }
            ]

            Format options of each object:
            {
                "reasoning": "short sentence explaining reasoning for ",
                "category":  
                    "Body Mass Index",
                    "Height",
                    "Body Mass",
                    "Heart Rate",
                    "Oxygen Saturation",
                    "Blood Pressure Systolic",
                    "Blood Pressure Diastolic",
                    "Respiratory Rate",
                    "Step Count",
                    "Distance Walking Running",
                    "Basal Energy Burned",
                    "Active Energy Burned",
                    "Flights Climbed",
                    "Number Of Times Fallen",
                    "Apple Exercise Time",
                    "Dietary Caffeine",
                    "Distance Cycling",
                    "Resting Heart Rate",
                    "VO2 Max",
                    "Walking Heart Rate Average",
                    "Environmental Audio Exposure",
                    "Headphone Audio Exposure",
                    "Walking Double Support Percentage",
                    "Six Minute Walk Test Distance",
                    "Apple Stand Time",
                    "Walking Speed",
                    "Walking Step Length",
                    "Walking Asymmetry Percentage",
                    "Stair Ascent Speed",
                    "Stair Descent Speed",
                    "Sleep Duration Goal",
                    "Apple Walking Steadiness",
                    "Running Stride Length",
                    "Running Vertical Oscillation",
                    "Running Ground Contact Time",
                    "Heart Rate Recovery One Minute",
                    "Running Power",
                    "Environmental Sound Reduction",
                    "Running Speed",
                    "Time In Daylight",
                    "Physical Effort",
                    "Core Sleep",
                    "Sleep Time",
                    "Sleep Awake Time",
                    "Deep Sleep",
                    "REM Sleep",
                    "Heart Rate Variability SDNN"
                "data1_time": "1 week", "1 month", "3 month", "6 month", "All time"
                "data1_type": "max", "min", "mean", "median", "trend" (if time is "all time" then type CANNOT be "trend")
                "data2_time": same options as data1_type
                "data2_type": same options as data2_type
            }
            Remember you can ONLY select data categories from the list above, and you should output an array of two objects.
            """
    },
    {
        "role": "user",
        "content": transcript
    }
]


result = pg.Chat.create(
model="Neural-Chat-7B",
messages=messages,
max_tokens=1000
)


content = result['choices'][0]['message']['content']
print(content)
# print(json.dumps(result['output'], sort_keys=True, indent=4, separators=(',', ': ')))
