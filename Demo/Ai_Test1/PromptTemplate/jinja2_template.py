# -*- coding: utf-8 -*-
"""
LangChain1.0 Jinja2模板语法案例（完全正常运行版）
知识点：正确适配Jinja2语法 + LangChain安全限制
"""
from langchain_core.prompts import PromptTemplate

# ====================== 没用Jinja2的写法（痛点示例） ======================
def build_prompt_without_jinja2(username, vip_level, chat_history, user_question):
    vip_rule = "优先处理，承诺1小时回复" if vip_level >= 3 else "常规处理，承诺24小时回复"

    # 对历史会话进行切片，如果长度超过3，则只取最后3条
    # 三元运算：条件成立时的值 if 条件 else 条件不成立时的值
    short_history = chat_history[-3:] if len(chat_history) > 3 else chat_history

    # 遍历 历史会话 short_history列表，并将每次遍历的列表数据 msg
    # 将 msg['role']和 msg['content']从列表中取出，重新拼接成 "角色 : 内容" 的格式
    string_list = [f"{msg['role']}：{msg['content']}" for msg in short_history]

    # 分隔符.join()：Python中的字符串方法，用于将序列中的元素，通过分隔符 连接成一个字符串
    # 此处为 将 short_history 列表中，取出的所有字符串，用换行分隔符 "\n" 连接起来，形成一个多行的字符串格式
    history_str = "\n".join(string_list)

    # 定义prompt模版
    prompt = f"""
用户：{username}（VIP等级：{vip_level}）
规则：{vip_rule}
历史会话：
{history_str}
用户问题：{user_question}
"""
    return prompt

# 测试“没用Jinja2”的部分
print("=== 没用Jinja2的输出 ===")

# 测试用的历史对话数据
chat_history = [
    {"role": "user", "content": "我的订单没收到"},
    {"role": "ai", "content": "请提供订单号"},
    {"role": "user", "content": "123456"},
    {"role": "ai", "content": "我帮你查询"}
]

# 调用函数进行测试
prompt1 = build_prompt_without_jinja2(
    username="张三", # 用户名
    vip_level=4, # VIP等级
    chat_history=chat_history, # 历史会话
    user_question="订单123456加急处理！" # 用户问题
)
print(prompt1)

# ====================== 用了Jinja2的写法（正确语法） ======================
# 定义 template 模版
tp = """
用户：{{username}}（VIP等级：{{vip_level}}）

规则：
{% if vip_level >= 3 %}
优先处理，承诺1小时回复
{% else %}
常规处理，承诺24小时回复
{% endif %}

历史会话：
{% for msg in chat_history[-3:] %}
{{msg['role']}}：{{msg['content']}}
{% endfor %}

用户问题：{{user_question}}
"""

# 实例化模板
prompt_template = PromptTemplate.from_template(
    template=tp, # 传参，将定义好的模版，传给参数 template
    template_format="jinja2" # 指定 template_format = "jinja2"
)

# 填充参数（变量会被Jinja2正确解析）
print("\n=== 用了Jinja2的输出 ===")
prompt2 = prompt_template.format(
    username="张三",
    vip_level=4,
    chat_history=chat_history,
    user_question="订单123456加急处理！"
)
print(prompt2)

# ====================== 核心提升总结 ======================
"""
1. 语法正确：Jinja2模板变量用{{变量名}}，条件/循环用{% ... %}；
2. 功能正常：变量、条件、循环都能被正确渲染；
3. 优势体现：替代手动字符串拼接，代码更简洁易维护。
"""


