import pyshark as ps
import streamlit as st
import os
import re
import asyncio

def remove_ansi_escape_sequences(input_string):
    # Define a regular expression pattern to match ANSI escape sequences
    ansi_escape_pattern = r'\x1B(?:[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]'
    
    # Use re.sub() to replace ANSI escape sequences with an empty string
    cleaned_string = re.sub(ansi_escape_pattern, '', input_string)
    
    return cleaned_string

def getPcapData(input_file:str = "", filter="", decode_info={}):
    try :
        if os.name == 'nt':
            eventloop = asyncio.ProactorEventLoop()
            asyncio.set_event_loop(eventloop)        
        cap : ps.FileCapture = ps.FileCapture(input_file=input_file, display_filter=filter)
        with open('out.txt', 'w') as f:
            for pkt in cap:
                print(pkt, file=f)
        out_string = open('out.txt', 'r').read()
        #os.remove('out.txt')
    except ps.tshark.tshark.TSharkNotFoundException:
        st.error(body='TShark/Wireshark is not installed. \n Please install [wireshark](https://tshark.dev/setup/install/#install-wireshark-with-a-package-manager) first', icon='🚨')
        st.warning(body='LPW is now stopped', icon='🛑')
        st.stop()
    return remove_ansi_escape_sequences(out_string)