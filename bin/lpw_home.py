import streamlit as st
from lpw_init import *
from lpw_prompt import *
from lpw_packet import *
import os
import time
from streamlit_extras.tags import tagger_component
from importlib.metadata import version, PackageNotFoundError
import os

def get_lpw_version():
    try:
        return version("lpw")
    except PackageNotFoundError:
        # Fallback to reading from version.txt
        current_dir = os.path.dirname(os.path.abspath(__file__))
        version_file = os.path.join(current_dir, "../VERSION.txt")
        with open(version_file, "r") as f:
            return f.read().strip()

lpw_avatar = "https://raw.githubusercontent.com/kspviswa/local-packet-whisperer/main/gifs/lpw_logo_small.png"

def loadDefaultSettings():
    model_list, server_connected = getModelList()
    if server_connected:
        st.session_state['selected_model'] = model_list[0]
    st.session_state['llm_server_connection_status'] = server_connected

def renderConnection(is_connected: bool):
    return '🟢' if is_connected else '🔴'

def getFiltersAndDecodeInfo():
    filters = []
    decodes = {}
    resp = ""
    if returnValue('http'):
        filters.append("tcp.port == 80")
        decodes['tcp.port == 80'] = 'http'
    if returnValue('snmp'):
        filters.append("udp.port == 161 || udp.port == 162")
        decodes['udp.port == 161'] = 'snmp'
        decodes['udp.port == 162'] = 'snmp'
    if returnValue('https'):
        filters.append("tcp.port == 443")
        decodes['tcp.port == 443'] = 'https'
    if returnValue('ntp'):
        filters.append("udp.port == 123")
        decodes['udp.port == 123'] = 'ntp'    
    if returnValue('ftp'):
        filters.append("tcp.port == 21")
        decodes['tcp.port == 21'] = 'ftp'
    if returnValue('ssh'):
        filters.append("tcp.port == 22")
        decodes['tcp.port == 22'] = 'ssh'
    if returnValue('ngap'):
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

def resetChat():
    returnValue('messages').clear()
    clearHistory()

def getEnabledFilters():
    filters = []
    if returnValue('http'):
        filters.append('http')
    if returnValue('snmp'):
        filters.append('snmp')
    if returnValue('https'):
        filters.append('https')
    if returnValue('ntp'):
        filters.append('ntp')   
    if returnValue('ftp'):
        filters.append('ftp')
    if returnValue('ssh'):
        filters.append('ssh')
    if returnValue('ngap'):
        filters.append('ngap')
    
    if len(filters) < 1:
        return None
    return tagger_component('Enabled Filters', tags=filters, color_name='blue')

with st.sidebar:
    if returnValue('selected_model') == 'Undefined':
        loadDefaultSettings()
    st.metric("Selected Model ✅", returnValue('selected_model'))
    st.metric("Plugged to 🔌 & connection status 🚦", f'{returnValue('llm_server')} {renderConnection(returnValue('llm_server_connection_status'))}')
    getEnabledFilters()
    st.metric("Streaming 〰️", returnValue('streaming_enabled'))

col1, col2 = st.columns([7,3])
with col1:
    st.title('Local Packet Whisperer (LPW)')
    st.markdown('`Your local network assistant!`')
    st.markdown(f'`Version : {get_lpw_version()}`')
with col2:
    st.image(image=lpw_avatar, use_column_width=True)



if not returnValue('llm_server_connection_status'):
    st.error('LPW Cannot talk to the remote 🦙 Ollama Server 🦙', icon='🚨')
    st.info('Please troubleshoot the **connection** or Update the **LLM Server Settings** in LPW Setting ⚙️ Page', icon='💡')
else :
    st.markdown('#### Step 1️⃣ 👉🏻 Build a knowledge base')
    packetFile = st.file_uploader(label='Upload either a PCAP or PCAPNG file to chat', accept_multiple_files=False, type=['pcap','pcapng'])
    st.markdown('#### Step 2️⃣ 👉🏻 Chat with packets')
    if packetFile == None:
        st.session_state['pcap_fname'] = "None 🚫"
        resetChat()
        st.markdown('#### Waiting for packets 🧘🏻🧘🏻🧘🏻🧘🏻')
    else:
        st.session_state['pcap_fname'] = packetFile.name
        st.sidebar.metric("Whispering with 🗣️", returnValue('pcap_fname'))
        with st.spinner('#### Crunching the packets... 🥣🥣🥣'):
            with open(f'{packetFile.name}', 'wb') as f:
                f.write(packetFile.read())
            filters, decodes = getFiltersAndDecodeInfo()
            initLLM(pcap_data=getPcapData(input_file=f'{packetFile.name}', filter=filters, decode_info=decodes))
            os.remove(f'{packetFile.name}')
        with st.chat_message(name='assistant', avatar=lpw_avatar):
            st.markdown('Chat with me..')
        for message in returnValue('messages'):
            with st.chat_message(name=message['role'], avatar = lpw_avatar if message['role'] == 'assistant' else None):
                st.markdown(message['content'])
        if prompt := st.chat_input('Enter your prompt'):
            returnValue('messages').append({'role' : 'user', 'content' : prompt})
            with st.chat_message(name='user'):
                st.markdown(prompt)
            with st.chat_message(name='assistant', avatar=lpw_avatar):
                with st.spinner('Processing....'):
                    full_response = chatWithModel(prompt=prompt, model=returnValue('selected_model'))
                    returnValue('messages').append({'role' : 'assistant', 'content' : full_response})
                    if returnValue('streaming_enabled'):
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