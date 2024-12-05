import streamlit as st
from lpw_init import *
from crewai import Agent, Task, Crew, LLM
import yaml

class LPWCrew:
    def __init__(self, llm_host="127.0.0.1", llm_port="11434", model="llama3.1:latest"):
        self.llm_host = llm_host
        self.llm_port = llm_port
        self.model = model
        self.llm = LLM(model=f'ollama/{model}', base_url=f'http://{llm_host}:{llm_port}', api_key='could be anything')
        self.loadConfig()
        self.crew = Crew(
            agents = [self.sne_agent],
            tasks = [self.caTask]
        )
        print('#### Crew initialized')
    
    def kickoff(self, data, protocol) -> str:
        result = self.crew.kickoff(inputs={'pcap_data' : data, 'protocol' : protocol})
        return result.raw
    
    def loadConfig(self):
        agent_data = yaml.safe_load(returnValue('agent_config_file')) if returnValue('agent_config_file') else yaml.safe_load(returnValue('default_agent_config'))
        self.sne_agent = Agent(
            role = agent_data['role'],
            goal = agent_data['goal'],
            backstory=agent_data['backstory'],
            llm=self.llm,
            #verbose=True
        )
        print(f'##### {getLpwPath('temp')}/insights.md')
        self.caTask = Task(
            description=agent_data['tasks'][0]['description'],
            expected_output=agent_data['tasks'][0]['expected_output'],
            #output_file=f'{getLpwPath('temp')}/insights.md',
            agent=self.sne_agent
        )


if __name__ == '__main__':
    with open('temp/out.txt', 'r') as f:
        ac = LPWCrew()
        result = ac.kickoff(f.read(), 'ngap')
        print(f'Result : {result}')