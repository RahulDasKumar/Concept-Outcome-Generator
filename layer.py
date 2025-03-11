from typing import Optional, Type
from neo4j_database import graph
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)

from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool


# finding LLM 
description_query = """
MATCH (n:Learning_Concept) WHERE n.name CONTAINS $learning_concept MATCH (n)-[r:HAS_OUTCOME]-(t:Learning_Outcome) RETURN n,t
"""
# understand 

def get_concept(entity: str) -> str:
    try:
        data = graph.query(description_query, params={"learning_concept": entity})
        return data
    except IndexError:
        return "No information was found"
    
from typing import Optional, Type

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)



class InformationInput(BaseModel):
    entity: str = Field(description="learning concept relevant to the coding question")


class InformationTool(BaseTool):
    name: str = "Information"
    description: str = (
        "This tool is used to categorize and find learning concepts based on coding question title and coding question description"
    )
    args_schema: Type[BaseModel] = InformationInput

    def _run(
        self,
        entity: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        return get_concept(entity)

    async def _arun(
        self,
        entity: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """ Use the tool asynchronously. """
        return get_concept(entity)
    
    
