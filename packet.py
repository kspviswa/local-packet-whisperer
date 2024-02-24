import pyshark as ps


def getPcapData(input_file:str = "", filter=""):
    #print(f'incoming pcap name {input_file}')
    #print(f'Filters => {filter}')
    cap = ps.FileCapture(input_file=input_file, display_filter=filter)
    #print(cap)
    out = ""
    for c in cap:
        #print(c)
        out += c.__str__()
    #print(out)
    return out