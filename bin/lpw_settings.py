import streamlit as st
from lpw_init import *
from lpw_prompt import *
from lpw_packet import *

def save_sm() -> None:
    modifySM(returnValue('system_message'))

#st.markdown('## Enter OLLAMA endpoint:')
#st.text_input("Ollama endpoint", placeholder="Eg localhost", label_visibility='hidden')
st.title('LPW Settings ⚙️')
#st.markdown('## System Message:')
with st.expander(label='**Set System Message** *(optional)*', expanded=False):
    st.session_state['system_message'] = st.text_area(label='Override system message', value=returnValue('system_message'), label_visibility="hidden", height=500, on_change=save_sm)
st.session_state['streaming_enabled'] = st.toggle(label='Enable Streaming', value=returnValue('streaming_enabled'))

with st.expander(label='**LLM Server Settings**', expanded=False, icon=":material/neurology:"):
    st.session_state['llm_server'] = st.text_input(label="LLM Server Host", value=returnValue('llm_server'))
    st.session_state['llm_server_port'] = st.number_input(label="LLM Server Host Port", value=returnValue('llm_server_port'), min_value=1024, max_value=65525, step=1)
    setLLMServer(st.session_state['llm_server'], st.session_state['llm_server_port'])
    st.session_state['selected_model'] = st.selectbox('**Available Models**', placeholder="Choose an Option", options=getModelList()[0])
st.markdown('#### Select protocols to filter in analysis')
col1, col2, col3 = st.columns(3)
with col1:
    st.session_state['http'] = st.checkbox("HTTP",value=returnValue('http')) #80
    st.session_state['snmp'] = st.checkbox("SNMP",value=returnValue('snmp')) #161, 162
    st.session_state['ntp'] = st.checkbox("NTP",value=returnValue('ntp')) #123
with col2:
    st.session_state['https'] = st.checkbox("HTTPS",value=returnValue('https')) #443
    st.session_state['ftp'] = st.checkbox("FTP",value=returnValue('ftp')) #21
    st.session_state['ssh'] = st.checkbox("SSH",value=returnValue('ssh')) #22
with col3:
    st.session_state['sip'] = st.checkbox("SIP",value=returnValue('sip')) #5060
    st.session_state['ngap'] = st.checkbox("NGAP",value=returnValue('ngap')) #38412

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

with st.expander(label="**NGAP Agent Settings** ⚠️Experimental⚠️", expanded=False, icon=":material/robot_2:"):
    glowing_header_text('Config YAML', 'Available for 5G NGAP only')
    st.markdown('Refer [here](https://github.com/kspviswa/local-packet-whisperer/blob/main/config/5g_agent.yaml) for more details to how to create this file.')
    st.session_state['agent_config_file'] = st.file_uploader(label='Agent Config YAML', type='yaml', label_visibility="hidden")

def loadDefaultSettings():
    st.session_state['selected_model'] = st.selectbox('Models', placeholder="Choose an Option", options=getModelList(),label_visibility='hidden')