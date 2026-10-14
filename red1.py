from deepteam import red_team
from deepteam.vulnerabilities import Toxicity
from deepteam.attacks.single_turn import PromptInjection
from deepeval.models.llms.gemini_model import GeminiModel

ha = [PromptInjection()]       
vtypes =  ["insults","mockery"]
hv = [Toxicity(types=vtypes)]

from google import genai
client = genai.Client()
chat = client.chats.create(model="gemini-3.1-flash-lite")

def model_callback(prompt: str) -> str:
    response = chat.send_message(prompt)
    return response.text

results = red_team(
    model_callback=model_callback,
    attacks=ha,       
    vulnerabilities=hv,
    simulator_model=GeminiModel(model="gemini-3.5-flash-lite"),
    evaluation_model=GeminiModel(model="gemini-3.5-flash-lite"),
    async_mode=False
)
