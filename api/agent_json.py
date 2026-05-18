from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
from dotenv import load_dotenv
import os
from agentscope.agent import ReActAgent, UserAgent
from agentscope.formatter import OpenAIChatFormatter
from agentscope.memory import InMemoryMemory
from agentscope.model import OpenAIChatModel
from agentscope.tool import (
    Toolkit
)
from agentscope.tool import ToolResponse
from agentscope.message import Msg
from tools.registry import REGISTRY_TOOLS, registry_tool

load_dotenv()

class AgentCreator(BaseModel):
    name: str
    prompt: str
    agent_tools: list
    knowledge: list
    msg: str
    user_id: int
    memory : dict
    
memorys = {}
        
agent_json=FastAPI()
@agent_json.post("/agents")

async def get_agent(agent: AgentCreator):
    """first prototipe"""
    
    functions_list = [REGISTRY_TOOLS[tool] for tool in agent.agent_tools if tool in REGISTRY_TOOLS] 
    
    toolkit = registry_tool(functions_list)
    
    msg = Msg(name="User", content=agent.msg, role="user")
    
    cryptopeper = ReActAgent(
        name = agent.name,
        sys_prompt= agent.prompt,
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

