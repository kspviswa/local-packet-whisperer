import streamlit as st
from lpw_init import *
#from lpw_settings import loadDefaultSettings
import os
import time
from streamlit_extras.tags import tagger_component

#st.set_page_config(page_title='Local Packet Whisperer', page_icon='🗣️')

lpw_avatar = "https://raw.githubusercontent.com/kspviswa/local-packet-whisperer/main/gifs/lpw_logo_small.png"

#loadDefaultSettings()
#st.session_state['selected_model'] = getModelList()[0]

def getFiltersAndDecodeInfo():
    filters = []
    decodes = {}
    resp = ""
    if st.session_state['http']:
        filters.append("tcp.port == 80")
        decodes['tcp.port == 80'] = 'http'
    if st.session_state['snmp']:
        filters.append("udp.port == 161 || udp.port == 162")
        decodes['udp.port == 161'] = 'snmp'
        decodes['udp.port == 162'] = 'snmp'
    if st.session_state['https']:
        filters.append("tcp.port == 443")
        decodes['tcp.port == 443'] = 'https'
    if st.session_state['ntp']:
        filters.append("udp.port == 123")
        decodes['udp.port == 123'] = 'ntp'    
    if st.session_state['ftp']:
        filters.append("tcp.port == 21")
        decodes['tcp.port == 21'] = 'ftp'
    if st.session_state['ssh']:
        filters.append("tcp.port == 22")
        decodes['tcp.port == 22'] = 'ssh'
    if st.session_state['ngap']:
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
    st.session_state.messages.clear()
    clearHistory()

def getEnabledFilters():
    filters = []
    if st.session_state['http']:
        filters.append('http')
    if st.session_state['snmp']:
        filters.append('snmp')
    if st.session_state['https']:
        filters.append('https')
    if st.session_state['ntp']:
        filters.append('ntp')   
    if st.session_state['ftp']:
        filters.append('ftp')
    if st.session_state['ssh']:
        filters.append('ssh')
    if st.session_state['ngap']:
        filters.append('ngap')
    
    return tagger_component('Enabled Filters', tags=filters, color_name='blue')

with st.sidebar:
    st.metric("Selected Model ✅", st.session_state['selected_model'])
    st.metric("Connected to 🔌", st.session_state['llm_server'])
    getEnabledFilters()

col1, col2 = st.columns([3,1])
with col1:
    st.markdown('# :rainbow[Local Packet Whisperer] \n # :rainbow[🗣️🗣️🗣️]')
with col2:
    st.image(image=lpw_avatar, use_column_width=True)

st.markdown('#### Step 1️⃣ 👉🏻 Build a knowledge base')
packetFile = st.file_uploader(label='Upload either a PCAP or PCAPNG file to chat', accept_multiple_files=False, type=['pcap','pcapng'])
st.markdown('#### Step 2️⃣ 👉🏻 Chat with packets')
if packetFile == None:
    resetChat()
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
                full_response = chatWithModel(prompt=prompt, model=st.session_state['selected_model'])
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