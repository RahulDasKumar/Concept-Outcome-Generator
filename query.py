from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

def get_learning_concepts_prompt(schema,QuestionTitle, QuestionDescription):
    prompt = ChatPromptTemplate.from_messages([
        ("system", 
         "You are an AI assistant specializing in programming learning concepts classification.\n"
         "Your task is to identify relevant Learning_Concepts for a given coding problem based on its title and description.\n"
         "Use only the provided relationship types, node labels, and properties from the schema.\n"
         "Ensure that all names come directly from the Neo4j database query results."),
        ("human", 
         "### Task:\n"
         "- Extract relevant **Learning_Concepts** based on the given question.\n"
         "- Return **ONLY** a list of relevant Learning_Concepts (do not include Learning_Outcomes yet)."),
        
        ("human", 
         "### Example Input:\n"
         "**Question Title:** Implementing Binary Search in Java\n"
         "**Question Description:** Student needs to implement a binary search algorithm in Java to find an element in a sorted array."),
        
        ("ai", 
         "**Learning_Concepts:** Binary Search, Algorithm Efficiency, Divide and Conquer"),
                
        ("human", 
         "### Actual Input:\n"
         "**Question Title:** {QuestionTitle}\n"
         "**Question Description:** {QuestionDescription}")
    ])
    
    return prompt.format(schema=schema, QuestionTitle=QuestionTitle, QuestionDescription=QuestionDescription)


def get_learning_outcomes_prompt(schema, coding_solution, learning_concepts):
    prompt = ChatPromptTemplate.from_messages([
        ("system", 
         "You are an AI assistant that maps programming Learning_Concepts to their associated Learning_Outcomes.\n"
         "Based on a given coding solution and associated learning concept, return a list of all Learning_Outcomes that best match the coding solution.\n"
         "Ensure all Learning_Concept names come directly from the database query results."),
        ("human", 
         "### Task:\n"
         "- Use the extracted Learning_Concepts to find their respective Learning_Outcomes.\n"
         "- Return a list of all associated Learning_Outcomes from most relavant to least relevant. At most select 5 learning outcomes"),
        
        ("human", 
         "### Example Input:\n"
         "**Learning_Concepts:** Binary Search, Algorithm Efficiency, Divide and Conquer\n"
         "**Coding Solution:**\n"
         "```java\n"
         "public int binarySearch(int[] array, int target) {\n"
         "    int l = 0;\n"
         "    int r = array.length;\n"
         "    while (l <= r) {\n"
         "        int m = (r + l) / 2;\n"
         "        if (target > array[m]) {\n"
         "            l = m + 1;\n"
         "        } else if (target < array[m]) {\n"
         "            r = m - 1;\n"
         "        } else {\n"
         "            return m;\n"
         "        }\n"
         "    }\n"
         "    return -1;\n"
         "}\n"
         "```"),
        
        ("ai", 
        "Learning_Outcomes:  Demonstrate an understanding of binary search ,Analyze time complexity of binary search",),
        
        ("human", 
         "### Actual Input:\n"
         "**Learning_Concepts:** {learning_concepts}\n"
         "**Coding Solution:**\n"
         "```{coding_solution}```")
    ])
    
    return prompt.format(schema=schema, coding_solution=coding_solution, learning_concepts=learning_concepts)
