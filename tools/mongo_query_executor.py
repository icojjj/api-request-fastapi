from pymongo import MongoClient
from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

client = MongoClient("mongodb://127.0.0.1:27017")
db = client["gas"]
collection = db["cilindro"]

def formatted_id(document: dict) -> dict:
    document["_id"] = str(document["_id"])
    return document

def query_find(query: dict) -> ToolResponse:
    try:
        response = collection.find(query)
        response_formatted_id = [formatted_id(doc) for doc in response]
        final_query = response_formatted_id
        if response_formatted_id:
            return ToolResponse(content=[TextBlock(type= "text", text=f"Result: {final_query}")])
        else:
            return ToolResponse(content=[TextBlock(type="text", text="No Data Earned")])
    except ConnectionError:
        return ToolResponse(content=[TextBlock(type="text", text=f"Connection error, please verify your endpoint")])
