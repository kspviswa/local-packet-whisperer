import streamlit as st
from lpw_init import *
from lpw_prompt import *
from lpw_packet import *
from lpw_agent import LPWCrew
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

def show_beta_ribbon():
    st.markdown("""
        <style>
            .ribbon {
                position: absolute;
                top: 0;
                right: 0;
                width: 150px;
                height: 22px;
                margin-right: -50px;
                transform: rotate(45deg);
                background-color: #ff4b4b;
                color: white;
                text-align: center;
                font-weight: bold;
                font-size: 0.8em;
                line-height: 22px;
                z-index: 999;
            }
        </style>
        <div class="ribbon">Experimental BETA</div>
    """, unsafe_allow_html=True)

def glowing_header_text(header, text):
    st.markdown(f"""
        <div style="display: flex; align-items: center;">
            <h1> {header} </h1>
            <span style="
                background-color: #4CAF50;
                color: white;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 0.8em;
                box-shadow: 0 0 10px #4CAF50;
                animation: glow 1.5s ease-in-out infinite alternate;">
                {text}
            </span>
        </div>
        <style>
            @keyframes glow {{
                from {{
                    box-shadow: 0 0 5px #4CAF50;
                }}
                to {{
                    box-shadow: 0 0 20px #4CAF50;
                }}
            }}
        </style>
    """, unsafe_allow_html=True)

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
    st.metric("Plugged to 🔌 & connection status 🚦", f"{returnValue('llm_server')} {renderConnection(returnValue('llm_server_connection_status'))}")
    getEnabledFilters()
    st.metric("Streaming 〰️", returnValue('streaming_enabled'))
    packetFile = st.file_uploader(label='Upload either a PCAP or PCAPNG file to chat', accept_multiple_files=False, type=['pcap','pcapng'])
    if packetFile:
        st.session_state['pcap_fname'] = packetFile.name
        with st.spinner('#### Crunching the packets... 🥣🥣🥣'):
            with open(f'{packetFile.name}', 'wb') as f:
                f.write(packetFile.read())
            filters, decodes = getFiltersAndDecodeInfo()
            st.session_state['pcap_filters'] = filters
            # print(f'#### {st.session_state['pcap_filters']}')
            st.session_state['pcap_data'] = getPcapData(input_file=f'{packetFile.name}', filter=filters, decode_info=decodes)
            initLLM(pcap_data=returnValue('pcap_data'))
            #os.remove(f'{packetFile.name}')
    else:
        st.session_state['pcap_fname'] = "None 🚫"

col1, col2 = st.columns([2,1])
with col1:
    st.title('Local Packet Whisperer (LPW)')
    st.markdown('`Your local network assistant!`')
    st.markdown(f'`Version : {get_lpw_version()}`')
with col2:
    st.image(image=lpw_avatar, use_container_width=True)



if not returnValue('llm_server_connection_status'):
    st.error('LPW Cannot talk to the remote 🦙 Ollama Server 🦙', icon='🚨')
    st.info('Please troubleshoot the **connection** or Update the **LLM Server Settings** in LPW Setting ⚙️ Page', icon='💡')
else :
    #st.markdown('#### Step 1️⃣ 👉🏻 Build a knowledge base')
    #packetFile = st.file_uploader(label='Upload either a PCAP or PCAPNG file to chat', accept_multiple_files=False, type=['pcap','pcapng'])
    #st.markdown('#### Step 2️⃣ 👉🏻 Chat with packets')
    chat, insights = st.tabs(['Chat 💬', 'Insights ✨'])
    with chat:
        st.header('Whisper with LPW')
        if st.session_state['pcap_fname'] == "None 🚫":
            resetChat()
            st.markdown('#### Waiting for packets 🧘🏻🧘🏻🧘🏻🧘🏻')
        else:
            chat_container = st.container(height=500)
            prompt = st.chat_input('Enter your prompt', key='prompt_ctrl', disabled=False)
            st.sidebar.metric("Whispering with 🗣️", returnValue('pcap_fname'))
            with chat_container.chat_message(name='assistant', avatar=lpw_avatar):
                st.markdown('Chat with me..')
            for message in returnValue('messages'):
                with chat_container.chat_message(name=message['role'], avatar = lpw_avatar if message['role'] == 'assistant' else None):
                    st.markdown(message['content'])
            if prompt:
                returnValue('messages').append({'role' : 'user', 'content' : prompt})
                with chat_container.chat_message(name='user'):
                    st.markdown(prompt)
                with chat_container.chat_message(name='assistant', avatar=lpw_avatar):
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
    with insights:
        show_beta_ribbon()
        glowing_header_text('Agentic Insights', 'Available for 5G NGAP only')
        st.markdown('`Get a comprehensive report on PCAPs. Powered by LPW Agents!`')
        if st.session_state['pcap_fname'] == "None 🚫":
            st.markdown('#### Waiting for packets 🧘🏻🧘🏻🧘🏻🧘🏻')
            st.session_state['insights_done'] = False
        else:
            if not returnValue('insights_done'):
                st.markdown('Packet Capture Processed. Click below to generate insights')
                if st.button(label='Generate Insights 🫰🏻', type='primary', use_container_width=True):
                    st.session_state['insights_done'] = True
                    st.session_state['insights_file_done'] = False
                    st.rerun()
            else:
                if not returnValue('insights_file_done'):
                    with st.spinner('#### Generating Insights 🪄🪄🪄'):
                        st.session_state['insights_raw'] = LPWCrew(llm_host=returnValue('llm_server'),
                                llm_port=returnValue('llm_server_port'),
                                model=returnValue('selected_model')).kickoff(returnValue('pcap_data'), returnValue('pcap_filters'))
                        st.session_state['insights_file_done'] = True
                        st.rerun()
                else:
                    #markdown_path = os.path.join(getLpwPath('temp'), 'insights.md')
                    #st.markdown(open(markdown_path).read())
                    st.markdown(returnValue('insights_raw'))
                    st.download_button(label='Download Insights markdown',
                                        data = returnValue('insights_raw'),
                                        type='primary',
                                        use_container_width=True)