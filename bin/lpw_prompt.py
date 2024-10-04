import streamlit as st
from lpw_ollamaClient import OllamaClient
from typing import List
from lpw_init import returnValue
from lpw_prompt import *
from lpw_packet import *

def returnSystemText(pcap_data : str) -> str:
    PACKET_WHISPERER = f"""
        {returnValue('system_message')}
        packet_capture_info : {pcap_data}
    """
    return PACKET_WHISPERER

oClient = OllamaClient()

def setLLMServer(server):
    oClient.setServer(server)

def initLLM(pcap_data) -> None:
    oClient.set_system_message(system_message=returnSystemText(pcap_data)) 

def getModelList() -> List[str]:
    return oClient.getModelList()

def chatWithModel(prompt:str, model: str):
    return oClient.chat(prompt=prompt, model=model, temp=0.4)

def clearHistory():
    oClient.clear_history()

def modifySM(new_sm: str) -> None:
    oClient.edit_system_message(new_sm)
