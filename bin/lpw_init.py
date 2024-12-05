import streamlit as st
from pkg_resources import resource_filename
import os

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

DEFAULT_AGENT_CONFIG_YAML = """
---
name: 5G_Signaling_Protocol_Specialist
role: 5G Signaling Protocol Specialist
goal: Analyze and interpret all 5G signaling messages within PCAP files, providing detailed insights into the communication between various 5G network elements, with a focus on NGAP and related protocols.
backstory: >
  A veteran telecommunications expert with over a decade of experience in mobile network protocols. 
  Has been at the forefront of 5G technology since its inception, contributing to the development and 
  implementation of 5G standards. Possesses in-depth knowledge of 3GPP specifications, including 
  TS 38.413 (NGAP), TS 38.331 (RRC), and TS 24.501 (NAS), and has a comprehensive understanding 
  of 5G network architecture and signaling procedures.
tasks:
  - name: Comprehensive Analysis
    description: >
      Perform a thorough analysis of 5G signaling messages in packet_capture_info available below, including:
      1. Analyze the packet capture information to identify and decode all 5G signaling messages, including NGAP, NAS, and RRC protocols.
      2. Dissect complex message structures such as NGAP PDUs, Path Transfer Requests, and PDU Session Resource Setup Requests. Unearth important insights like gNodeB Name, SUCI, SUPI, IMSI, PLMN, MNC, MCC, IMEI, PEI etc from the messages.
      3. Interpret signaling procedures and message flows, explaining their significance in 5G network operations.
      4. Identify and explain key procedures such as NG Setup, Initial Context Setup, UE Context Release, and Path Transfer.
      5. Verify protocol compliance against 3GPP specifications, flagging any deviations or potential issues.
      6. Correlate messages across different interfaces (e.g., N1, N2) to provide a holistic view of signaling exchanges. You can use ASCII diagrams to illustrate the flow of exchanges between different network elements present in this packet capture.
      7. Detect anomalies or unusual patterns in the signaling traffic that might indicate performance issues or security threats.
      8. Generate detailed reports on signaling behavior, including message sequence diagrams and explanations of observed procedures.
      9. Provide insights on potential optimizations or troubleshooting recommendations based on the analyzed signaling patterns.
      10. Collaborate with other specialized agents to contribute to a comprehensive understanding of the 5G network's behavior and performance.

      packet_capture_info : {pcap_data}
    expected_output: >
      A comprehensive analysis report in a well-formatted markdown document
"""

default_settings = {
    'streaming_enabled' : False,
    'messages' : [],
    'system_message' : DEFAULT_SYSTEM_MESSAGE,
    'selected_model' : 'Undefined',
    'llm_server' : "127.0.0.1",
    'llm_server_port' : 11434,
    'llm_server_connection_status' : 'False',
    'http' : False,
    'https' : False,
    'snmp' : False,
    'ftp' : False,
    'ngap' : False,
    'ssh' : False,
    'ntp' : False,
    'pcap_fname' : "None 🚫",
    'pcap_data' : "",
    'pcap_filters' : "",
    'insights_done' : False,
    'insights_file_done' : False,
    'agent_config_file' : None,
    'default_agent_config' : DEFAULT_AGENT_CONFIG_YAML,
    'insights_raw' : ""
}

def returnValue(key):
    if key not in st.session_state:
        st.session_state[key] = default_settings[key]
    return st.session_state[key]

def getLpwPath(dirname):
    usr_home_dir = os.path.expanduser("~")
    lpw_home_dir = os.path.join(usr_home_dir, '.lpw')
    dirname_path = os.path.join(lpw_home_dir, dirname)
    if not os.path.exists(dirname_path):
        os.makedirs(dirname_path)
    return dirname_path