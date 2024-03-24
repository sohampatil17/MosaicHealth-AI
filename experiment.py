import os
import json
import predictionguard as pg


os.environ["PREDICTIONGUARD_TOKEN"] = "q1VuOjnffJ3NO2oFN8Q9m8vghYc84ld13jaqdF7E"


messages = [
{
"role": "system",
"content": "You are a helpful assistant. Your model is hosted by Prediction Guard, a leading AI company."
},
{
"role": "user",
"content": "Where can I access the LLMs in a safe and secure environment?"
}
]


result = pg.Chat.create(
model="Neural-Chat-7B",
messages=messages
)


print(json.dumps(
result,
sort_keys=True,
indent=4,
separators=(',', ': ')
))

