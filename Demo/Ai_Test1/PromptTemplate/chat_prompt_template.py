# -*- coding: utf-8 -*-
"""
LangChain1.0 ChatPromptTemplate完整案例
包含：没用ChatPromptTemplate的痛点 + 用了后的提升
知识点：聊天模型专属模板（结构化角色）
"""
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate
)

# ====================== 没用ChatPromptTemplate的写法（痛点示例） ======================
def build_chat_prompt_without_template(system_role, ai_history, user_question):
    """
    手动拼接聊天提示词的痛点：
    1. 角色前缀硬编码（如"System: "），换模型需改代码；
    2. 无法直接生成模型需要的Message对象，需额外转换；
    3. 角色顺序易混乱（如system放在最后，影响模型理解）。
    """
    # 手动拼接GPT风格的提示词（前缀固定死）
    # 额外问题：若切换到Claude模型，需要手动改前缀为"Human: "和"Assistant: "，非常麻烦
    prompt = f"System: {system_role}\nAI: {ai_history}\nHuman: {user_question}"
    return prompt

# 测试：手动拼接的问题
print("=== 没用ChatPromptTemplate的输出（手动拼接） ===")
manual_prompt = build_chat_prompt_without_template(
    system_role="你是电商客服，回复不超过100字",
    ai_history="请提供订单号",
    user_question="查订单123456的物流"
)
print(manual_prompt)



# ====================== 用了ChatPromptTemplate的写法（提升示例） ======================
# 1. 定义各角色模板（与模型无关，自动适配所有聊天模型）
# 系统角色（核心规则，优先放在最前面）
system_template = "你是电商客服，回复不超过100字"
system_prompt = SystemMessagePromptTemplate.from_template(system_template)

# AI历史回复（上下文）
ai_template = "{ai_history}"
ai_prompt = AIMessagePromptTemplate.from_template(ai_template)

# 人类用户问题
human_template = "{user_question}"
human_prompt = HumanMessagePromptTemplate.from_template(human_template)


# 2. 组合聊天模板（固定角色顺序：system → ai → human，符合模型理解习惯）
chat_prompt = ChatPromptTemplate.from_messages([
    system_prompt, # 系统角色
    ai_prompt, # AI历史回复
    human_prompt # 人类用户问题
])


# 3. 生成Message对象（可直接传给任何聊天大模型，切换调用其他模型时，无需修改模版）
print("\n=== 用了ChatPromptTemplate的输出（结构化Message） ===")
messages = chat_prompt.format_prompt(
    ai_history="请提供订单号",  # 填充变量值，传给 chat_prompt 模板中 ai_prompt 的占位符 ai_template = "{ai_history}"
    user_question="查订单123456的物流" # 填充变量值，传给 chat_prompt 模板中 human_prompt 的占位符 human_template = "{user_question}"
).to_messages() # LangChain 中 messages 对象的核心方法，用于将格式化后的提示词，转换为 聊天模型可直接使用的 标准消息列表对象
# 每个消息对象包含:
# type 属性: 自动匹配生成 调用大模型时兼容的 默认角色类型(如 system、human、ai)，便于调用大模型时自动识别、切换模型无需修改模板
# content 属性: 包含实际的消息内容

print(messages)

# 打印Message结构（模型可直接识别的格式）
for msg in messages:
    # 对 messages列表中的每个对象 进行遍历
    # msg.type会自动匹配生成 调用大模型时兼容的 默认角色类型(如 system、human、ai)，便于调用大模型时自动识别、切换模型无需修改模板
    print(f"{msg.type}: {msg.content}")



"""
# 4. 直接调用GPT-3.5（无需手动转换格式）
print("\n=== 调用GPT-3.5的输出 ===")
llm = ChatOpenAI(model="gpt-3.5-turbo", api_key="你的API_KEY")
response = llm.invoke(messages)
print(f"模型回复：{response.content}")

"""


# ====================== 核心差异总结 ======================
"""
1. 适配性：
   - 没用：手动写死角色前缀（如"System: "），换模型（GPT→Claude）需改代码；
   - 用了：自动生成模型兼容的角色类型，切换模型无需修改模板。

2. 结构化：
   - 没用：输出是字符串，需手动拆分为角色+内容；
   - 用了：直接生成Message对象（含type和content），可直接传给模型。

3. 稳定性：
   - 没用：角色顺序易混乱（如system放最后），影响模型理解；
   - 用了：固定system→ai→human 的 msg.type 顺序，符合模型最优输入格式。
"""


