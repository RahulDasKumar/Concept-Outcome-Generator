from typing import List, Tuple
from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain_openai import ChatOpenAI
from layer import InformationTool
import pandas as pd
import os
from query import get_learning_concepts_prompt, get_learning_outcomes_prompt
from neo4j_database import graph
import time
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
# ive tried the deepseek.com url as well
llm = ChatOpenAI(
    model="deepseek-r1:70b",  
    temperature=0,  
    base_url="http://cci-siscluster1.charlotte.edu:5002",
)




tools = [InformationTool()]


llm_with_tools = llm.bind(functions=[convert_to_openai_function(t) for t in tools])


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant that identifies and suggests learning concepts "
            "related to coding questions. Only return fundamental concepts or "
            "topics necessary to understand and solve the problem.",
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)


def _format_chat_history(chat_history: List[Tuple[str, str]]):
    buffer = []
    for human, ai in chat_history:
        buffer.append(HumanMessage(content=human))
        buffer.append(AIMessage(content=ai))
    return buffer


agent = (
    {
        "input": lambda x: x["input"],
        "chat_history": lambda x: _format_chat_history(x["chat_history"])
        if x.get("chat_history")
        else [],
        "agent_scratchpad": lambda x: format_to_openai_function_messages(
            x["intermediate_steps"]
        ),
    }
    | prompt
    | llm_with_tools
    | OpenAIFunctionsAgentOutputParser()
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
question_mapping  = pd.read_csv('CodeWorkoutMapping.csv')
for id, row in question_mapping.iterrows():
    print(get_learning_concepts_prompt(graph.schema,row['CodeWorkoutQuestionTitle'],row['Description']))
    learning_concepts = agent_executor.invoke({"input":get_learning_concepts_prompt(graph.schema,row['CodeWorkoutQuestionTitle'],row['Description'])})
    print(learning_concepts)

