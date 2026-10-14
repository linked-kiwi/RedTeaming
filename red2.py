import streamlit as st
st.set_page_config(page_title="CyberconRed",layout="wide")
st.subheader("Cybercon 2026 Red Team Tool")

alist = ["prompt Injection", "roleplay"]
vlist1 = {
    "bias":["race","gender"],
    "toxicity":["insults","profanity"]
}
vlist2   = list(vlist1)

from deepteam import red_team
from deepeval.models.llms.gemini_model import GeminiModel

from google import genai
client = genai.Client()
chat = client.chats.create(model="gemini-3.1-flash-lite")

def model_callback(prompt: str) -> str:
    response = chat.send_message(prompt)
    return response.text

st1,st2,st3,st4 = st.columns([0.2,0.2,0.2,0.4])
attack   = st1.selectbox("Attack",alist)
vulnerability = st2.selectbox("Vulnerability", vlist2)
vlist3  = vlist1[vulnerability]
vtype = st3.selectbox("Subtype",vlist3)

if st.button("Run"):
    if attack=="prompt-injection":
       from deepteam.attacks.single_turn import PromptInjection
       ha = [PromptInjection()]
   
    if attack=="roleplay":
       from deepteam.attacks.single_turn import Roleplay
       ha = [Roleplay()]
    
    if vulnerability=="bias":
       from deepteam.vulnerabilities import Bias
       hv = [Bias(types=[vtype])]

    if vulnerability=="toxicity":
       from deepteam.vulnerabilities import Toxicity
       hv = [Toxicity(types=[vtype])]

    with st.spinner("Testing…"):
       results = red_team(
         model_callback=model_callback,
         attacks=ha,       
         vulnerabilities=hv,
         attacks_per_vulnerability_type=3,
         simulator_model=GeminiModel(model="gemini-3.5-flash-lite"),
         evaluation_model=GeminiModel(model="gemini-3.5-flash-lite"),
         async_mode=False
       )

    with st.expander("Results"):
     for tested in results.test_cases:
        st1,st2,st3 = st.columns(3)
        st1.write(tested.input)
        st2.write(tested.actual_output)
        st3.write(tested.reason)
