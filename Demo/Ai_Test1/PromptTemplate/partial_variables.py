# -*- coding: utf-8 -*-
"""
LangChain1.0 partial_variables案例
知识点：模板默认值设置
场景：电商客服Agent，固定"工具列表"和"回复规则"，仅动态传用户问题
"""
from langchain_core.prompts import PromptTemplate

# ====================== 没用partial_variables的写法（痛点示例） ======================
def build_tool_prompt_without_partial(user_question, tools, reply_rule):
    """
    痛点：
    1. 工具列表、回复规则是固定值，但每次调用都要传；
    2. 传参冗余，易漏传reply_rule导致模型回复不规范。
    """
    template = f"""
你是电商客服Agent，规则：
1. 仅能调用工具：{tools}
2. {reply_rule}
用户问题：{user_question}
"""
    return template

# 测试：每次调用都要传固定参数
print("=== 没用partial_variables的输出 ===")
prompt1 = build_tool_prompt_without_partial(
    user_question="查订单123456的物流",
    tools="查订单、查物流、售后申请",  # 调用工具：固定值，每次都要传
    reply_rule="回复不超过100字，口语化"  # 回复规则：固定值，每次都要传
)
print(prompt1)

# ====================== 用了partial_variables的写法（提升示例） ======================
# 1. 定义基础模板（包含固定变量+动态变量）
template = """
你是电商客服Agent，规则：
1. 仅能调用工具：{tools}
2. {reply_rule}
用户问题：{user_question}
"""
# 2. 实例化 template 模板
prompt_template = PromptTemplate.from_template(template)

# .partial_variables(): 为实例化模版 设置固定变量的默认值
prompt_template = prompt_template.partial(
    tools="查订单、查物流、售后申请",  # 固化工具列表
    reply_rule="回复不超过100字，口语化"  # 固化回复规则
)

# 3. 调用时仅需传动态变量（user_question）
print("\n=== 用了partial_variables的输出 ===")
prompt2 = prompt_template.format(
    user_question="查订单123456的物流"  # 仅传动态参数，简洁
)
print(prompt2)

# 扩展：动态覆盖默认值（如需临时调整工具列表）
prompt3 = prompt_template.format(
    user_question="申请售后",
    tools="查订单、售后申请"  # 临时覆盖默认值
)
print("\n=== 动态覆盖默认值的输出 ===")
print(prompt3)

# ====================== 核心提升总结 ======================
"""
1. 简洁性：固定参数设默认值，调用仅传动态参数，代码量减少30%+；
2. 稳定性：避免漏传固定参数导致模型行为异常；
3. 灵活性：支持临时覆盖默认值，适配特殊场景。
"""


