import predictionguard as pg
from sentence_transformers import SentenceTransformer
import faiss

knowledge_base = [
    "In the interaction, the patient expresses concern about recent unusual fluctuations in their sugar levels. The doctor inquires about any potential changes in the patient's diet, exercise, or stress levels that might have impacted these levels. The patient acknowledges experiencing stress at work but has not made significant changes to their diet or exercise routine. The doctor advises the patient to continue monitoring their sugar levels closely and suggests exploring stress management techniques. The patient is advised to maintain their current diet and exercise routine and to inform the doctor if the sugar level fluctuations persist or worsen. The doctor emphasizes the importance of managing stress to control sugar levels and encourages the patient to report any new or unusual symptoms."
]

prompt_template = f"""
### Instruction:
Read the below input context and generate a detailed medical report.
Use the information in the below input and external knowledge to answer the question."

### Input:
Context: {{}}
Question: {{}}

### Response:
"""

model = SentenceTransformer("all-MiniLM-L6-v2")

kb_embeddings = model.encode(knowledge_base)

index = faiss.IndexFlatL2(kb_embeddings.shape[1]) # 384
index.add(kb_embeddings)

def rag_answer(question):
    try:
        # Generate embedding for the question
        question_embedding = model.encode([question])

        # Find the most similar text from the knowledge base using FAISS
        _, most_relevant_idx = index.search(question_embedding, 1)
        relevant_chunk = knowledge_base[most_relevant_idx[0][0]]
        # Format our prompt with the question and relevant context using f-strings
        prompt=prompt_template.format(relevant_chunk, question)

        # Get a response from the language model
        result = pg.Completion.create(
            model="Neural-Chat-7B", #"Nous-Hermes-Llama2-13B",
            prompt=prompt
        )
        return result['choices'][0]['text']
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return "Sorry, something went wrong. Please try again later."

question1 = "Generate a detailed medical report"
response1 = rag_answer(question1)
print(f"Dr Khan's Report: {response1}")


































# import os
# import json
# import predictionguard as pg


# os.environ["PREDICTIONGUARD_TOKEN"] = "q1VuOjnffJ3NO2oFN8Q9m8vghYc84ld13jaqdF7E"

# messages = [
#     {
#         "role": "system",
#         "content": "Create a medical report for the doctor using the information given"
#     },
#     {
#         "role": "user",
#         "content": "In the doctor-patient interaction, the patient expressed concerns about recent erratic fluctuations in their blood sugar levels, which are usually stable. Despite adhering to their regular diet and exercise routine, the patient noted these unusual changes and mentioned experiencing increased stress at work. The doctor acknowledged the potential impact of stress on blood sugar levels and advised the patient to continue monitoring their sugar levels closely. The doctor also suggested exploring stress management techniques and emphasized the importance of maintaining the current diet and exercise routine. The patient was advised to inform the doctor if the sugar levels continue to be erratic or increase. The doctor highlighted the significance of managing stress in controlling sugar levels and encouraged the patient to report any new symptoms or concerns." }
# ]


# result = pg.Chat.create(
# model="Neural-Chat-7B",
# messages=messages
# )


# content = result['choices'][0]['message']['content']
# print(content)
# # print(json.dumps(result['output'], sort_keys=True, indent=4, separators=(',', ': ')))
