import pandas as pd
import os
from query import get_learning_concepts_prompt
from neo4j_database import graph
import time
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.graph_qa.cypher_utils import CypherQueryCorrector, Schema
from langchain.chains import GraphCypherQAChain
import pickle
# ive tried the deepseek.com url as well
# llm = ChatOpenAI(
#     model_name="Qwen/Qwen2.5-7B-Instruct-1M",
#     openai_api_base="http://cci-siscluster1.charlotte.edu:5000/v1",
#     openai_api_key="NULL",  
#     temperature=0
# )


load_dotenv()
print(os.getenv('GOOGLE_API_KEY'))
os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')

llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash',temperature=0)



chain = GraphCypherQAChain.from_llm(graph=graph, llm=llm, verbose=True,validate_cypher=True,allow_dangerous_requests=True)
mapping = {}
qa_prompt_mistakes = 0
question_mapping  = pd.read_csv('CodeWorkoutMapping.csv')
for id, row in question_mapping.iterrows():
    try:
        print(row)
        print(get_learning_concepts_prompt(graph.schema,row['CodeWorkoutQuestionTitle'],row['Description']))
        learning_concepts = chain.invoke({"query":get_learning_concepts_prompt(graph.schema,row['CodeWorkoutQuestionTitle'],row['Description'])})
        print(learning_concepts)
        mapping[row['QuestionID']] = learning_concepts
    except:
        qa_prompt_mistakes +=1
        continue
    time.sleep(10)
print("mistakes :",qa_prompt_mistakes)
with open('mapping.pickle','wb') as file:
    pickle.dump(mapping,file)
    