from operator import itemgetter

from openai import OpenAI

class Chat_info:
    """定义chat初始化信息的类"""
    
    def __init__(self):
        """设定默认值 包含api-key、温度、是否流式输出、是否推理"""
        self.api = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        self.temperature = 1.4
        self.stream = False
        self.reasoner = False
    
    def info_set(
        self,
        **kwargs
        ):
        """
        改变chat的配置。
        只更新传入的设置，其他设置保持不变。
        有效形参名为：api、temperature、stream、reasoner
        分别指api-key、模型温度、是否启用流式输出、是否启用推理（R1）
        """
        for key, value in kwargs.items():
            if key == 'api':
                self.api = value
            elif key == 'temperature':
                self.temperature = value
            elif key == 'stream':
                self.stream = value
            elif key == 'reasoner':
                self.reasoner = value
            else:
                print("\ninfo参数传入错误！")
        # self.api = api
        # self.temperature = temperature
        # self.stream = stream
        # self.reasoner = reasoner
    
    def info_print(self):
        """输出当前chat的配置信息，包括api-key、模型温度、是否启用流式输出、是否启用推理（R1）"""
        print("\nThe info of the chat is as follows:")
        print(f"api_key:     {self.api}")
        print(f"temperature: {self.temperature}")
        print(f"stream:      {self.stream}")
        print(f"reasoner:    {self.reasoner}")
        if self.reasoner:
            print("model:       DeepSeek-R1")
        else:
            print("model:       DeepSeek-V3")

class Chat(Chat_info):
    """定义chat交互的类"""
    
    def __init__(self):
        """
        messages是包含message字典的列表
        message字典包含了角色和内容信息，角色system为系统设定，user为用户的提问，assisant为chat的回答
        """
        super().__init__()
        self.messages = []
    
    def system_append(self, message_text=''):
        """用于增加system设定的函数，传入一行设定字符串"""
        message = {'role': 'system', 'content': message_text}
        self.messages.append(message)
    
    def system_set(self, message_text_list=[]):
        """用于重置并设置system设定的函数，传入包含system设定字符串的列表"""
        self.messages = []
        for message_text in message_text_list:
            message = {'role': 'system', 'content': message_text}
            self.messages.append(message)
    
    def messages_print(self):
        """用于打印当前messages列表信息的函数，包含所有system设定、历史全部对话"""
        self.messages = sorted(self.messages, key=lambda x: x['role'] != 'system')
        print("\nThe contents of messages are as follows:")
        for message in self.messages:
            for key,value in message.items():
                print(f"{key:9}: {value}")
    
    def system_print(self):
        """用于打印当前system设定信息的函数"""
        print("\nThe contents of system are as follows:")
        for message in self.messages:
            if message['role'] == 'system':
                print(message['content'])
    
    def chat_clear(self):
        """用于清除当前历史对话数据的函数，不会清除sys设定"""
        for message in self.messages:
            if message['role'] != 'system':
                del(message)
    
    def chat_reset(self):
        """用于复位chat的函数，清除所有历史对话数据和system设定，不改变info"""
        self.messages = []
    
    def send_messages(self):
        """
        核心函数，向服务器发送当前的messages列表，返回包含响应信息的字典
        若流式开启，则会直接将结果打印在屏幕上，全部打印完毕后返回响应字典
        若流式关闭，不会打印结果，全部响应完毕后返回字典
        返回字典reply_dict的键值为'reply_reasoning'和'reply_content'，
        分别为思考过程和答复结果，当不启用推理时，返回的思考过程为空字符串
        """
        client = OpenAI(api_key=self.api, base_url="https://api.deepseek.com")
        reply_reasoning = ""
        reply_content = ""
        
        if self.reasoner:
            response = client.chat.completions.create(
            model="deepseek-reasoner",
            messages=self.messages,
            temperature=self.temperature,
            stream=self.stream
            )
            
            if self.stream:
                """两个flag用于标志第一次响应，以给出思考过程和最终结果的提示语"""
                flag_reasoning_start = False
                flag_content_start = False
                for chunk in response:
                    if chunk.choices[0].delta.reasoning_content:
                        if not flag_reasoning_start:
                            print("\n（思考过程）: ", end="", flush=True)
                            flag_reasoning_start = True
                        else:
                            pass
                        print(chunk.choices[0].delta.reasoning_content, end="", flush=True)
                        reply_reasoning += str(chunk.choices[0].delta.reasoning_content)
                    elif chunk.choices[0].delta.content:
                        if not flag_content_start:
                            print("\n\n\n（最终结果）: ", end="", flush=True)
                            flag_content_start = True
                        else:
                            pass
                        print(chunk.choices[0].delta.content, end="", flush=True)
                        reply_content += str(chunk.choices[0].delta.content)
                flag_reasoning_start = False
                flag_content_start = False
            
            else:
                reply_reasoning = response.choices[0].message.reasoning_content
                reply_content = response.choices[0].message.content
        
        else:
            response = client.chat.completions.create(
            model="deepseek-chat",
            messages=self.messages,
            temperature=self.temperature,
            stream=self.stream
            )
            
            if self.stream:
                flag_content_start = False
                for chunk in response:
                    if not flag_content_start:
                        print("\n（结果）: ", end="", flush=True)
                        flag_content_start = True
                    else:
                        pass
                    reply_content += str(chunk.choices[0].delta.content)
                    print(chunk.choices[0].delta.content, end="", flush=True)
                flag_content_start = False
            else:
                reply_content = response.choices[0].message.content
            reply_reasoning = ''
        
        message_reply = {'role': 'assistant', 'content': reply_content}
        self.messages.append(message_reply)
        
        reply_dict = {'reply_reasoning': reply_reasoning, 'reply_content': reply_content}
        
        return reply_dict
    
    def chat_once(self):
        """只进行一次对话，对话后清除对话历史记录，不清除sys设定"""
        prompt = "\nInput something:\n"
        message_text = input(prompt)
        message = {'role': 'user', 'content': message_text}
        self.messages.append(message)
        reply_dict = self.send_messages()
        if self.stream:
            print('\n')
        else:
            if reply_dict['reply_reasoning']:
                print(f"\n（思考过程）: {reply_dict['reply_reasoning']}")
                print(f"\n（最终回答）: {reply_dict['reply_content']}\n")
            else:
                print(f"\n（回答）: {reply_dict['reply_content']}\n")
        self.chat_clear()

    def chat_lasting(self):
        """开启循环对话模式，保留上下文，实现类似于网页版的chat交互"""
        while True:
            prompt = "\nInput something:\n"
            message_text = input(prompt)
            message = {'role': 'user', 'content': message_text}
            self.messages.append(message)
            reply_dict = self.send_messages()
            if self.stream:
                print('\n')
            else:
                if reply_dict['reply_reasoning']:
                    print(f"\n（思考过程）: {reply_dict['reply_reasoning']}\n")
                    print(f"\n（最终回答）: {reply_dict['reply_content']}\n")
                else:
                    print(f"\n（回答）: {reply_dict['reply_content']}\n")
