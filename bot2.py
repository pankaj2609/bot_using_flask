
#you need to run upload.py once to create the vector_db in mongodb(for the database that you have)
import os
os.environ["HF_TOKEN"] = "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"
import google.generativeai as genai

from pymongo import MongoClient
from langchain_mongodb import MongoDBAtlasVectorSearch

from langchain_community.embeddings import HuggingFaceHubEmbeddings
from langchain_community.tools import DuckDuckGoSearchRun



mongo_uri = "mongodb+srv://jangra2609:1234@cluster101.jhizg9j.mongodb.net/?retryWrites=true&w=majority&appName=Cluster101"
client = MongoClient(mongo_uri)
db_name = "food_data"
collection_name = "nutrient_level_vectors"
my_collection = client[db_name][collection_name]

embeddings = HuggingFaceHubEmbeddings()
vector_store = MongoDBAtlasVectorSearch(collection = my_collection,embedding=embeddings)

search = DuckDuckGoSearchRun()


def get_result(query_typed):

    genai.configure(api_key="AIzaSyBdb1Jwz9j8s8PkOxa0FXkmzN2V7wNCifc")
    # Set up the model
    generation_config = {
    "temperature": 0.1,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
    }

    safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    ]

    model = genai.GenerativeModel(model_name="gemini-pro",
                                generation_config=generation_config,
                                safety_settings=safety_settings)
    user_typed = query_typed

    docs = vector_store.similarity_search(user_typed,k=5) #relevant info from database
    temp_docs = "" #relevant info as combined string
    for each in docs:
        temp_docs += (str(each) + ". ")

    # ddg_result = search.run(user_typed) #result from duckduckgo search

    ques = user_typed
    context1 = temp_docs
    prompt1 = f"Read this thoroughly:- {context1}.  Now, you are supposed to give nutritional information (if mentioned in context give those values, else give all information you find) of the food mentioned:- {ques}. Assume that this is the only source of info you have. Get me the best possible answer from here.If you are unable to get answer, simply return \"did_not_find_answer\" "

    response = model.generate_content(prompt1)
    # print(response.text)
    #use try, catch before response.text
    op_data = response.text

    if(op_data == "did_not_find_answer"):
        ddg_result = search.run(user_typed) #result from duckduckgo search
        context2 = ddg_result
        prompt2 = f"Read this thoroughly:- {context2}.  Using this context, you are supposed to give answer for this query:- {ques}. "
        response = model.generate_content(prompt2)
        # print(response.text)
        try:
            op_data = response.text
        except ValueError:
            op_data = "some error occured"
            # response = model.generate_content(prompt2)
            # op_data = response.text
            # print(response)
    return op_data
    # print(op_data)