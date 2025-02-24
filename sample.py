from deepseek_api import Chat

chat = Chat()

system_setting = "你是一个python高手"
chat.system_append(system_setting)

chat.info_set(temperature=1, stream=True, reasoner=True)

chat.info_print()
chat.system_print()

# chat_once(chat)
# chat.messages_print()

chat.chat_lasting()