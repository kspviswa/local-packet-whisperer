import ollama
from typing import List

class OllamaClient():

    def __init__(self):
        self.messages = []
    
    def clear_history(self):
        self.messages.clear()
    
    def append_history(self, message):
        self.messages.append(message)
    
    def check_system_message(self) -> bool:
        try:
            if self.messages[0]['role'] == 'system':
                return True
            else:
                return False
        except:
            return False
    
    def set_system_message(self, system_message:str) -> None:
        sMessage = dict({'role' : 'system', 'content' : system_message})
        self.messages.append(sMessage)
    
    def edit_system_message(self, system_message:str) -> None:
        for m in self.messages:
            if m['role'] == 'system':
                m['content'] = system_message
    
    def chat(self, prompt:str, model: str, temp: float, system:str = "default") -> str:
        options = dict({'temperature' : temp})
        message = {}
        message['role'] = 'user'
        message['content'] = prompt
        self.messages.append(message)
        response = ollama.chat(model=model, messages=self.messages, options=options)
        self.messages.append(response['message'])
        return response['message']['content']

    def chat_stream(self, prompt:str, model: str, temp: float, system:str = "default"):
        options = dict({'temperature' : temp})
        message = {}
        if system != 'default' and not self.check_system_message():
            sMessage = dict({'role' : 'system', 'content' : system})
            self.messages.append(sMessage)
        message['role'] = 'user'
        message['content'] = prompt
        self.messages.append(message)
        stream = ollama.chat(model=model, messages=self.messages, options=options, stream=True)
        # the caller should call append_history
        return stream
    
    def getModelList(self) -> List[str]:
        retList = []
        model_list = ollama.list()
        models = model_list['models']
        for model in models:
            retList.append(model['name'])
        return retList


if __name__ == '__main__':
    client = OllamaClient()
    print(f'List of models are {client.getModelList()}')
    while True:
        print('You :')
        response = client.chat_stream(model='dolphin-mistral:latest', temp=0.8, prompt=input())
        contents = ""
        AiMessage = {}
        for chunk in response:
            content = chunk['message']['content']
            print(content, end='', flush=True)
            contents += content
        AiMessage['role'] = 'assistant'
        AiMessage['content'] = contents
        client.append_history(AiMessage)