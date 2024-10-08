![](gifs/lpw_logo_small.png)

# Local Packet Whisperer (LPW)

### A Fun project using [Ollama](https://github.com/ollama), [Streamlit](https://streamlit.io) & [PyShark](https://github.com/KimiNewt/pyshark) to chat with PCAP/PCAG NG files locally, privately!

[![Downloads](https://static.pepy.tech/badge/lpw)](https://pepy.tech/project/lpw) [![Downloads](https://static.pepy.tech/badge/lpw/month)](https://pepy.tech/project/lpw)

## Features & Background

1) 100% local, private PCAP assistant powered by range of local LLMs at your control, powered by Ollama
2) Purely based on promp engg without any fancy libraries & dependencies. 100% vanilla
3) Uses streamlit for the FE and pyshark for the pcap parsing needs
4) Available as a pip installable package. So just *pip it away!* 😎
5) As of **v0.2.3**, you can also connect LPW to a Ollama server running over a network.

![](gifs/lpw_latest_cover.png)

Refer [Release History](https://github.com/kspviswa/local-packet-whisperer/releases) for more details info on what each release contains.

## Requirements

1) Download & Install [Ollama](https://ollama.ai) by referring to instructions according to your OS [here](https://ollama.com/download)

2) Pull any Chat based LLM models to use with LPW.
```
ollama pull dolphin-mistral:latest
```
3) If not running the desktop application, Start Ollama Server (refer [here](https://github.com/ollama/ollama?tab=readme-ov-file#start-ollama))

4) You also need to install `tshark` executable. You could either install the [Wireshark Application](https://www.wireshark.org/download.html) or simply use `brew install tshark`. 

    <details>
    <summary>⚠️Warning⚠️ If you don't perform this step, you may see below error</summary>

    ```
    TSharkNotFoundException: TShark not found. Try adding its location to the configuration file.
    ```
    </details> 



## Usage

1) Install *LPW* using pip
```
pip install lpw
```

2) This will install `lpw` CLI in your machine. Now simply Start or Stop LPW as follows:

```
lpw {start or stop}
lpw -h #for help
```

3) LPW will automatically fetch the local models from Ollama local repo and populate the dropdown. Select a model to start your test. You can play with more than 1 model to compare the results 😎

![](gifs/select_models.gif)

4) Now upload a PCAP/PCAPNG file.

![](gifs/upload_pcap.gif)

5) You can now start to chat with LPW and ask questions about the packet. **Please Note: The performance of LPW depends on the underlying model. So feel free to download as many local LLMs from Ollama and try it.** It is fun to see different response 🤩🤩🤩.

![](gifs/packet_chat.gif)
*(This is a long gif. You will find LLM response at the end of the gif)*

6) By default *PyShark* parse the pcap till transport layer. If you want, you can help the LLM to parse application layer by selecting protocol filter in the analysis *(just like how we would do in wireshark)* .

![](gifs/chat_with_ntp.gif)

## Local Development

1) Clone this repo and install requirements
```
git clone https://github.com/kspviswa/local-packet-whisperer.git
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
2) Run streamlit app & point to `http://localhost:8501`
```
streamlit run bin/lpw_main.py
```
or simply
```
<lpw dir>/bin/lpw {start or stop}
```

## Contributions

I just created this project based on inspiration from similar project called [Packet Buddy](https://github.com/automateyournetwork/packet_buddy) which used open AI. But if you find this useful and wanna contribute bug fixes, additional features feel free to do so by raising a PR or open issues for me to fix. I intend to work on this as a hobby unless there is some interest in the community.
