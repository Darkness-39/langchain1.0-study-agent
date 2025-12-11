# -*- coding: utf-8 -*-
"""
LangChain1.0 分阶段提示词（替代PipelinePromptTemplate）
知识点：分阶段拼接提示词（职责分离）
场景：电商Agent分阶段构建提示词：系统规则→VIP规则→用户问题
"""
from langchain_core.prompts import PromptTemplate


# ====================== 没用分阶段模板的写法（痛点示例） ======================
def build_prompt_without_pipeline(system_rule, vip_rule, user_question):
    """
    痛点：
    1. 多阶段提示词手动拼接，逻辑混乱；
    2. 改某一阶段需动整个提示词，易影响其他部分；
    3. 无法单独调试某一阶段。
    """
    prompt = f"""
{system_rule}
{vip_rule}
用户问题：{user_question}
"""
    return prompt


# 测试：手动拼接的输出
print("=== 没用分阶段模板的输出 ===")
prompt1 = build_prompt_without_pipeline(
    system_rule="你是电商客服Agent，回复不超过100字",
    vip_rule="VIP4用户优先处理，承诺1小时回复",
    user_question="查订单123456的物流"
)
print(prompt1)

# ====================== 用分阶段模板的写法 ====================================
# 1. 定义各阶段模板（职责分离，可单独调试）
# 阶段1：系统核心规则
system_template = PromptTemplate.from_template("你是电商客服Agent，规则：{system_rule}")
# 阶段2：VIP分级规则
vip_template = PromptTemplate.from_template("VIP规则：{vip_rule}")
# 阶段3：用户问题
user_template = PromptTemplate.from_template("用户问题：{user_question}")


# 2. 分阶段生成各部分内容
def build_prompt_with_pipeline(system_rule, vip_rule, user_question):
    # 单独生成各阶段内容
    system_part = system_template.format(system_rule=system_rule)
    vip_part = vip_template.format(vip_rule=vip_rule)
    user_part = user_template.format(user_question=user_question)

    # 按顺序拼接（可灵活调整顺序）
    final_prompt = f"{system_part}\n{vip_part}\n{user_part}"
    return final_prompt


# 测试：分阶段拼接的输出
print("\n=== 用分阶段模板的输出 ===")
prompt2 = build_prompt_with_pipeline(
    system_rule="你是电商客服Agent，回复不超过100字",
    vip_rule="VIP4用户优先处理，承诺1小时回复",
    user_question="查订单123456的物流"
)
print(prompt2)

# ====================== 核心提升总结 ======================
"""
1. 可维护性：分阶段定义模板，改某一阶段（如VIP规则）不影响其他部分；
2. 可调试性：可单独生成某一阶段的内容（如system_part），定位问题更高效；
3. 灵活性：可自由调整各阶段的拼接顺序，适配不同场景。
"""