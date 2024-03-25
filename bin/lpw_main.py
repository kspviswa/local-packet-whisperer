import streamlit as st
from lpw_prompt import *
from lpw_packet import *
import os
import time

st.set_page_config(page_title='Local Packet Whisperer', page_icon='🗣️')

lpw_avatar = "https://raw.githubusercontent.com/kspviswa/local-packet-whisperer/main/gifs/lpw_logo_small.png"

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

if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'system_message' not in st.session_state:
    st.session_state['system_message'] = DEFAULT_SYSTEM_MESSAGE

if 'streaming_enabled' not in st.session_state:
    st.session_state['streaming_enabled'] = False

def resetChat():
    st.session_state.messages.clear()
    clearHistory()

options = getModelList()
selected_model = ""

def save_sm() -> None:
    modifySM(st.session_state['system_message'])

with st.sidebar:
    #st.markdown('## Enter OLLAMA endpoint:')
    #st.text_input("Ollama endpoint", placeholder="Eg localhost", label_visibility='hidden')
    st.markdown('# LPW Settings ⚙️', unsafe_allow_html=True)
    st.markdown('## Syster Message:')
    with st.expander(label='**Set System Message** *(optional)*', expanded=False):
        st.session_state['system_message'] = st.text_area(label='Override system message', value=st.session_state['system_message'], label_visibility="hidden", height=500, on_change=save_sm)
    st.session_state['streaming_enabled'] = st.toggle(label='Enable Streaming')
    st.markdown('## Select a local model to use:')
    selected_model = st.selectbox('Models', placeholder="Choose an Option", options=options)
    if selected_model != "":
        st.markdown(f"### :rainbow[Selected {selected_model}]")
    st.markdown('## Select protocols to filter in analysis')
    http = st.checkbox("HTTP") #80
    snmp = st.checkbox("SNMP") #161, 162
    ntp = st.checkbox("NTP") #123
    https = st.checkbox("HTTPS") #443
    ftp = st.checkbox("FTP") #21
    ssh = st.checkbox("SSH") #22
    ngap = st.checkbox("NGAP") #38412

def getFiltersAndDecodeInfo():
    filters = []
    decodes = {}
    resp = ""
    if http:
        filters.append("tcp.port == 80")
        decodes['tcp.port == 80'] = 'http'
    if snmp:
        filters.append("udp.port == 161 || udp.port == 162")
        decodes['udp.port == 161'] = 'snmp'
        decodes['udp.port == 162'] = 'snmp'
    if https:
        filters.append("tcp.port == 443")
        decodes['tcp.port == 443'] = 'https'
    if ntp:
        filters.append("udp.port == 123")
        decodes['udp.port == 123'] = 'ntp'    
    if ftp:
        filters.append("tcp.port == 21")
        decodes['tcp.port == 21'] = 'ftp'
    if ssh:
        filters.append("tcp.port == 22")
        decodes['tcp.port == 22'] = 'ssh'
    if ngap:
        filters.append("sctp.port == 38412")
        decodes['stcp.port == 38412'] = 'ngap'
    
    l = len(filters)
    i=0
    for f in filters:
        resp += f 
        i += 1
        if i != l:
            resp += " || "
    return resp, decodes

col1, col2 = st.columns([3,1])
with col1:
    st.markdown('# :rainbow[Local Packet Whisperer] \n # :rainbow[🗣️🗣️🗣️]')
with col2:
    st.image(image=lpw_avatar, use_column_width=True)

st.markdown('#### Step 1️⃣ 👉🏻 Build a knowledge base')
packetFile = st.file_uploader(label='Upload either a PCAP or PCAPNG file to chat', accept_multiple_files=False, type=['pcap','pcapng'])
st.markdown('#### Step 2️⃣ 👉🏻 Chat with packets')
if packetFile == None:
    st.markdown('#### Waiting for packets 🧘🏻🧘🏻🧘🏻🧘🏻')
else:
    with st.spinner('#### Crunching the packets... 🥣🥣🥣'):
        with open(f'{packetFile.name}', 'wb') as f:
            f.write(packetFile.read())
        filters, decodes = getFiltersAndDecodeInfo()
        initLLM(pcap_data=getPcapData(input_file=f'{packetFile.name}', filter=filters, decode_info=decodes))
        os.remove(f'{packetFile.name}')
    with st.chat_message(name='assistant', avatar=lpw_avatar):
        st.markdown('Chat with me..')
    for message in st.session_state.messages:
        with st.chat_message(name=message['role'], avatar = lpw_avatar if message['role'] == 'assistant' else None):
            st.markdown(message['content'])
    if prompt := st.chat_input('Enter your prompt'):
        st.session_state.messages.append({'role' : 'user', 'content' : prompt})
        with st.chat_message(name='user'):
            st.markdown(prompt)
        with st.chat_message(name='assistant', avatar=lpw_avatar):
            with st.spinner('Processing....'):
                full_response = chatWithModel(prompt=prompt, model=selected_model)
                st.session_state.messages.append({'role' : 'assistant', 'content' : full_response})
                if st.session_state['streaming_enabled']:
                    message_placeholder = st.empty()
                    streaming_response = ""
                    # Simulate stream of response with milliseconds delay
                    for chunk in full_response.split():
                        streaming_response += chunk + " "
                        time.sleep(0.05)
                        # Add a blinking cursor to simulate typing
                        message_placeholder.markdown(streaming_response + "▌", unsafe_allow_html=True)
                    message_placeholder.markdown(full_response, unsafe_allow_html=True)
                else:
                    st.markdown(full_response)
        st.button('Reset Chat 🗑️', use_container_width=True, on_click=resetChat)