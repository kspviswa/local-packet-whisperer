import streamlit as st
from ollamaClient import OllamaClient
from typing import List

def returnSystemText(pcap_data : str) -> str:
    PACKET_WHISPERER = f"""
        {st.session_state['system_message']}
        packet_capture_info : {pcap_data}
    """
    return PACKET_WHISPERER

oClient = OllamaClient()

def initLLM(pcap_data) -> None:
    oClient.set_system_message(system_message=returnSystemText(pcap_data)) 

@st.cache_resource
def getModelList() -> List[str]:
    return oClient.getModelList()

def chatWithModel(prompt:str, model: str):
    return oClient.chat(prompt=prompt, model=model, temp=0.4)

def clearHistory():
    oClient.clear_history()

def modifySM(new_sm: str) -> None:
    oClient.edit_system_message(new_sm)
