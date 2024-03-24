# Mosiac Health AI

## 💡 Inspiration 
In a healthcare landscape awash with data, doctors often find themselves submerged under vast oceans of patient information. The critical insights that could transform patient care frequently remain buried. MosaicHealth AI emerges as a beacon of clarity, deftly sifting through this data deluge to highlight the information that truly matters. 🚑💡

## 🧙‍♂️ What it Does
Imagine a world where your fitness wearable isn't just a passive observer but an active participant in your health journey. MosaicHealth AI is that vision brought to life. As doctors and patients engage in conversation, our system listens in, displays key health insights from the patient's wearable data in real-time. This isn't just data collection; it's data revelation, assisting doctors in crafting medical reports with unparalleled precision and insight. 📊🩺 <br>

###Intel ODC - 
**Prediction Guard APIs** - Secure, compliant LLM<br>
**Intel Distribution of Modin** - improved inference speed for data analysis on wearable data using Modin<br>
**Phi-2 finetuning using IDC and medical dataset** - finetuned Phi-2 using one of HF's biggest medical datasets<br>
**Submitted to HF leaderboard** - submitted Intel optimized model on HF leaderboard<br>
**Int8 Quantization of Diaalo-GPT-large using IPEX** - (experimentation) faster inference speed after int8 quantization<br>

_HuggingFace submission_ - https://huggingface.co/sohampatil/msphi2-medical

## 🏗️ How We Built It
Understanding the hesitancy doctors have towards AI, we embraced Prediction Guard's HIPAA-compliant LLMs, combining compliance with cutting-edge technology. Though we stuck with PG due to its security, we also finetuned MS Phi-2 using the openlifesciences' medmcqa dataset (MedMCQA is a large-scale, Multiple-Choice Question Answering (MCQA) dataset designed to address real-world medical entrance exam questions) for our medical context🛡️🧠<br>
Through on-device WebAPIs, we listen patient-doctor dialogues, extracting salient points and meshing them with raw data from Apple Watches, all refined by Intel's Modin library and LLM APIs. 🍏⌚<br>
Then, using PredictionGuard, we combine narrative and numerical health data to generate a detailed medical report. 🧬💻

## 🧗‍♂️ Challenges We Ran Into
Navigating the labyrinth of medical privacy and data security, we chose Prediction Guard to shield our AI from the pitfalls of non-compliance and the specter of hallucinations, and to make doctors feel safer. 🛡️🔒<br>
Bridging the gap between spoken words and LLMs was a formidable challenge + the process of learning model fine-tuning. 🤖🎭  <br>

## 🤯 What We Learned
Our journey with MosaicHealth AI has been a profound learning experience, diving deep into the realms of Intel's Developer console, mastering the nuances of JavaScript, and unraveling the complexities of AI fine-tuning. We've harnessed the power of Large Language Models (LLMs) through advanced APIs, gaining invaluable insights and skills along the way.

## 🏆 Accomplishments That We're Proud Of
From a spark of an idea to a functioning MVP in a single day!!! 🌟🛠️<br>
The fine-tuning of Microsoft Phi-2, leveraging a trove of medical data, stands as a milestone in our journey, marking a leap forward in AI-powered healthcare. 🏆🧬

##  🔮 Next Steps
🛳️🛳️🛳️🛳️ ship....
