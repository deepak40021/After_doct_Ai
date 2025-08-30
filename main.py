
'''''
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="openai/gpt-oss-120b",
    task="conversational"
)

model = ChatHuggingFace(llm=llm)

#1st promt -> detailed report 
template1 = PromptTemplate(
    template="You are an experienced doctor and health advisor Your task is to give the most practical, safe, and optimistic solution based on the patient's problem , and the patient forgot the tips and suggestions of the doct on the topic : {topic}",
    input_variables=["topic"]
)
#2nd prompt -> summary
template2 = PromptTemplate(
    template=" Give everything in multiple paragraphs without tables , but in a very clean and organised way with proper 4-5 lines of spacing so that it is very easy to real with motivating and happy sentiments and  emojis ,  Start with a short, reassuring , very motivating and  positive statement. Explain the likely cause in very simple words.Give 3-5 practical steps that students, elderly people, and normal adults can actually follow.Prefer simple remedies, healthy lifestyle changes, or basic medicines (if necessary). Avoid complex treatments or anything unsafe without doctor supervision.End with a motivational line to give hope.  Based on the doctor's description and your understanding give the  The main health tips a patient should follow with Home remedies that can act as natural alternatives (like ORS = salt + sugar water) with other tips related to the patient and doctor's prescription: {report}",
    input_variables=["report"]
)

output_parser = StrOutputParser()

chain = template1 | model | output_parser | template2 | model | output_parser

result = chain.invoke({"topic": "Patient complains of mild fever (99.5°F), sore throat, and occasional dry cough for the past 3 days. No difficulty in breathing. Appetite slightly reduced. No history of chronic illness.Examination reveals mild redness in the throat, no pus points. Lungs clear on auscultation.Diagnosis: Viral upper respiratory tract infection (common cold).Advice: Rest, adequate hydration, and symptomatic management. Paracetamol 500 mg SOS for fever/body ache. Avoid cold drinks and oily food"})
print(result)




'''






from fastapi import FastAPI
from pydantic import BaseModel
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables (HuggingFace key etc.)
load_dotenv()

# Initialize FastAPI
app = FastAPI(
    title="Health Advisor API",
    description="An AI-powered doctor-like assistant that gives health advice and summaries",
    version="1.0.0",
)

# Input schema for request
class HealthRequest(BaseModel):
    topic: str


# Initialize HuggingFace model
llm = HuggingFaceEndpoint(
    repo_id="NousResearch/Hermes-4-70B",  # ya phir koi chhota model test ke liye
    task="conversational" ,
    max_new_tokens=512,
    temperature=0.7
)

model = ChatHuggingFace(llm=llm)

# First prompt (doctor’s detailed report)
template1 = PromptTemplate(
    template=(
        
        "You are an experienced doctor and health advisor. "
        "Your task is to give the most practical, safe, and optimistic solution based on the patient's problem. "
        "The patient forgot the tips and suggestions of the doctor on the topic: {topic}"
    ),
    input_variables=["topic"],
)

# Second prompt (summary + health tips)
template2 = PromptTemplate(
    template=(
        "Give everything in multiple paragraphs without tables, but in a very clean and organised way with proper "
        "4-5 lines of spacing so that it is very easy to read with motivating and happy sentiments and emojis. "
        "Start with a short, reassuring, very motivating, and positive statement. "
        "Explain the likely cause in very simple words. "
        "Give 3-5 practical steps that students, elderly people, and normal adults can actually follow. "
        "Prefer simple remedies, healthy lifestyle changes, or basic medicines (if necessary). "
        "Avoid complex treatments or anything unsafe without doctor supervision. "
        "End with a motivational line to give hope. "
        "Based on the doctor's description and your understanding, give the main health tips a patient should follow "
        "with home remedies that can act as natural alternatives (like ORS = salt + sugar water) with other tips "
        " Also dont show any things which the user gives , like behave as a friendly doctor who can help anyone and best in conversation , so give response accordingly"
        "related to the patient and doctor's prescription: {report}"
    ),
    input_variables=["report"],
)

output_parser = StrOutputParser()

# Define chain
chain = template1 | model | output_parser | template2 | model | output_parser


@app.post("/generate")
async def generate_health_advice(request: HealthRequest):
    """
    Generate health advice & tips based on patient's symptoms
    """
    result = chain.invoke({"topic": request.topic})
    return {"advice": result}


@app.get("/")
async def root():
    return {"message": "Welcome to Health Advisor API. Go to /docs to test the API."}
