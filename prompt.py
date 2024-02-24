import streamlit as st
from ollamaClient import OllamaClient
from typing import List

def returnSystemText(pcap_data : str) -> str:
    PACKET_WHISPERER = f"""
        You are a helper assistant specialized in analysing packet captures used to troubleshooting & technical analysis. Use the information present in packet_capture_info to answer all the questions truthfully. If the user asks about a specific application layer protocol, use the following hints to inspect the packet_capture_info to answer the question. Format your response in markdown text with line breaks & emojis.

        hints :
        http means tcp.port = 80
        https means tcp.port = 443
        snmp means udp.port = 161 or udp.port = 162
        ntp means udp.port = 123
        ftp means tcp.port = 21
        ssh means tcp.port = 22

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
