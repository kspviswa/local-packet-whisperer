import streamlit as st
from lpw_prompt import *
from lpw_packet import *

DEFAULT_SYSTEM_MESSAGE = """
        You are a helper assistant specialized in analysing packet captures used to troubleshooting & technical analysis. Use the information present in packet_capture_info to answer all the questions truthfully. If the user asks about a specific application layer protocol, use the following hints to inspect the packet_capture_info to answer the question.
        
        If the user asks for general analysis, extract information about every layer (such as ethernet, IP, transport layer), source and destination IPs, port numbers and other possible insights. Provide your response in a structured bullet response, easy to understand for a network engineer.

        Format your response in markdown text with line breaks. You are encouraged to use emojis to make your response more presentable and fun.

        hints :
        http means tcp.port = 80
        https means tcp.port = 443
        snmp means udp.port = 161 or udp.port = 162
        ntp means udp.port = 123
        ftp means tcp.port = 21
        ssh means tcp.port = 22
        ngap means sctp.port = 38412
"""

if 'streaming_enabled' not in st.session_state:
    st.session_state['streaming_enabled'] = False

if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'system_message' not in st.session_state:
    st.session_state['system_message'] = DEFAULT_SYSTEM_MESSAGE

if 'selected_model' not in st.session_state:
    st.session_state['selected_model'] = getModelList()[0]

if 'llm_server' not in st.session_state:
    st.session_state['llm_server'] = "127.0.0.1"

if 'http' not in st.session_state:
    st.session_state['http'] = False

if 'https' not in st.session_state:
    st.session_state['https'] = False

if 'ftp' not in st.session_state:
    st.session_state['ftp'] = False

if 'ntp' not in st.session_state:
    st.session_state['ntp'] = False

if 'ngap' not in st.session_state:
    st.session_state['ngap'] = False

if 'ssh' not in st.session_state:
    st.session_state['ssh'] = False

if 'snmp' not in st.session_state:
    st.session_state['snmp'] = False