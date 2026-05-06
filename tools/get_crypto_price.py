import requests
from agentscope.tool import ToolResponse
from agentscope.message import TextBlock 
def get_crypto_price(coin:str, fiat: str) -> ToolResponse:
    try:    
        response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies={fiat}")
        data = response.json
        if data:
            return ToolResponse(content=[TextBlock(type="text", text=f"Result: {response.json()}")])
        else:
            return ToolResponse(content=[TextBlock(type="text", text=f"No data availible.")])
    except requests.exceptions.RequestException:
        return f"No data availible."