from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
from dotenv import load_dotenv
import os
from tools.get_crypto_price import get_crypto_price
from agentscope.agent import ReActAgent, UserAgent
from agentscope.formatter import OpenAIChatFormatter
from agentscope.memory import InMemoryMemory
from agentscope.model import OpenAIChatModel
from agentscope.tool import (
    Toolkit
)
from agentscope.tool import ToolResponse
from agentscope.message import Msg

load_dotenv()

class AgentCreator(BaseModel):
    name: str
    prompt: str
    tools: list
    knowledge: list
    msg: str
        
agent_json=FastAPI()
@agent_json.post("/agents")

async def get_agent(agent: AgentCreator):
    """first prototipe"""
    toolkit = Toolkit()
    
    toolkit.register_tool_function(get_crypto_price)
    
    msg = Msg(name="User", content=agent.msg, role="user")
    
    cryptopeper = ReActAgent(
        name = "CryptoPeper",
        sys_prompt = """You are a cryptocurrency assistant. Follow these rules strictly:
        [TASK 1] - Analyze user intent:
        - If the user wants to chat or ask general questions: respond conversationally, DO NOT call any tools.
        - If the user wants price or technical data about any cryptocurrency: proceed to TASK 2.
        [TASK 2] - Fetch cryptocurrency data:
        1. Call the cryptocurrency price tool with the coin specified by the user.
        2. If the tool returns data: present it clearly to the user.
        3. If the tool fails or returns no data: inform the user that the information could not be retrieved and suggest they try again later.
        IMPORTANT: Never invent or estimate cryptocurrency prices. Only use data returned by the tool.""",
        model = OpenAIChatModel(
            api_key = os.environ.get("YOUR_PROVIDER_APIKEY"),
            model_name = "deepseek-chat",
            client_args={
                "base_url": "https://api.deepseek.com"
                },
            enable_thinking = True,
            stream = True,
            multimodality = False
        ),
        formatter = OpenAIChatFormatter(),
        toolkit = toolkit
    )
    
    response = await cryptopeper(msg)
    
    return response

