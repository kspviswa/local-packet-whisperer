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
    setLLMServer(st.session_state['llm_server'])
    #st.markdown('#### Select a model to use:')
    st.session_state['selected_model'] = st.selectbox('**Available Models**', placeholder="Choose an Option", options=getModelList())
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
    st.session_state['ngap'] = st.checkbox("NGAP",value=returnValue('ngap')) #38412

def loadDefaultSettings():
    st.session_state['selected_model'] = st.selectbox('Models', placeholder="Choose an Option", options=getModelList(),label_visibility='hidden')