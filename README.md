# deepseek_api_try
**一个python初学者根据deepseek官网的API接口文档编写的简单API调用实现程序，作为一段时间python学习的练手项目。**

**本仓库仅作为python新手进行项目实践练习的一次记录和分享，编写方法和思路等还存在许多不足，欢迎提出意见和建议！**

## 用前准备
使用该模块前需要安装openai库，在命令行输入：

  `python -m pip install openai`

## 第一次运行：
  修改sample.py文件的chat.info_set()函数的api参数，即可使用默认参数运行。

## 使用方法：
  *可参考给出的*sample.py*文件进行使用，具体步骤如下，可根据需要参考后文函数列表进行修改。*
  
  1. 定义一个Chat类实例如chat=Chat()，然后用chat.info_set()函数配置api_key、温度、是否启用流式输出、是否启用推理（R1）；
  
  2. 配置完成后，用chat.system_append()函数添加chat的system设定，如“你是一个通用助手”
  
  3. 最后用chat.chat_lasting()函数即可启动循环对话

## Chat类可用函数及说明（以类实例chat为例）：

  `chat.info_set(**kwargs): 改变chat的配置。只更新传入的设置，其他设置保持不变。有效形参名为：api、temperature、stream、reasoner，分别指api-key、模型温度、是否启用流式输出、是否启用推理（R1）`
  
  `chat.info_print()：输出当前chat的配置信息，包括api-key、模型温度、是否启用流式输出、是否启用推理（R1）`

  
  `chat.system_append(message_text='')：用于增加system设定的函数，传入一行设定字符串`
  
  `chat.system_set(message_text_list=[])：用于重置并设置system设定的函数，传入包含system设定字符串的列表`
  
  `chat.messages_print()：用于打印当前messages列表信息的函数，包含所有system设定、历史全部对话`
  
  `chat.chat_clear()：用于清除当前历史对话数据的函数，不会清除sys设定`
  
  `chat.chat_reset()：用于复位chat的函数，清除所有历史对话数据和system设定，不改变info`
  
  `chat.send_messages()：核心函数，向服务器发送当前的messages列表，返回包含响应信息的字典;
                        若流式输出开启，则会直接将结果打印在屏幕上，全部打印完毕后返回响应字典;
                        若流式输出关闭，不会打印结果，全部响应完毕后返回字典;
                        返回字典reply_dict的键值为'reply_reasoning'和'reply_content'，分别为思考过程和答复结果，当不启用推理时，返回的思考过程为空字符串`
                        
  `chat.chat_once()：只进行一次对话，对话后清除对话历史记录，不清除sys设定`
  
  `chat.chat_lasting()：开启循环对话模式，保留上下文，实现类似于网页版的chat交互`
