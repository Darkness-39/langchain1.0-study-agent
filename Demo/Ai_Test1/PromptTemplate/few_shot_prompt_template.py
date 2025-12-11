# -*- coding: utf-8 -*-
"""
LangChain1.0 FewShotPromptTemplate案例
知识点：少样本提示模板（示例与模板解耦）
场景：电商Agent少样本学习，参考示例回答订单问题
"""
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

# ====================== 没用FewShotPromptTemplate的写法（痛点示例） ======================
def build_fewshot_prompt_without_template(new_question):
    """
    痛点：
    1. 示例硬编码，运营改示例需改代码；
    2. 示例格式不统一，易出错；
    3. 无法动态调整示例数量。
    """
    # 示例硬编码在代码中
    examples = """
问题：什么是订单退款？
答案：订单退款是指用户申请退回订单支付金额，审核通过后原路返还。

问题：物流超时怎么办？
答案：物流超时可联系商家催单，或申请售后补偿。
"""
    prompt = f"""
参考以下示例回答问题：
{examples}
问题：{new_question}
答案：
"""
    return prompt

# 测试：示例硬编码，灵活性差
print("=== 没用FewShotPromptTemplate的输出 ===")
prompt1 = build_fewshot_prompt_without_template("订单发货后能退款吗？")
print(prompt1)

# ====================== 用了FewShotPromptTemplate的写法（提升示例） ======================
# 1. 定义示例模板（标准化示例格式）
example_template = """
问题：{question}
答案：{answer}
"""
example_prompt = PromptTemplate.from_template(example_template)

# 2. 示例数据（可从YAML/数据库读取，运营可独立维护）
examples = [
    {"question": "什么是订单退款？", "answer": "订单退款是指用户申请退回订单支付金额，审核通过后原路返还。"},
    {"question": "物流超时怎么办？", "answer": "物流超时可联系商家催单，或申请售后补偿。"}
]

# 3. 构建少样本模板
few_shot_prompt = FewShotPromptTemplate(
    examples=examples,          # 示例数据
    example_prompt=example_prompt,  # 示例格式模板
    prefix="参考以下示例回答问题：",  # 示例前的引导语
    suffix="问题：{new_question}\n答案：",  # 示例后的用户问题
    input_variables=["new_question"],  # 仅需传新问题
    example_separator="\n\n"   # 示例之间的分隔符
)

# 4. 生成提示词（示例可动态调整）
print("\n=== 用了FewShotPromptTemplate的输出 ===")
prompt2 = few_shot_prompt.format(new_question="订单发货后能退款吗？")
print(prompt2)

# 扩展：动态添加示例（运营无需改代码，直接加数据）
examples.append({"question": "订单发货后能退款吗？", "answer": "发货后可申请退款，商家确认后会安排退货退款。"})
few_shot_prompt.examples = examples  # 更新示例
prompt3 = few_shot_prompt.format(new_question="订单发货后能退款吗？")
print("\n=== 动态添加示例后的输出 ===")
print(prompt3)

# ====================== 核心提升总结 ======================
"""
1. 可维护性：示例与模板解耦，运营可独立维护示例，无需依赖开发；
2. 标准化：示例格式统一，模型输出质量更稳定；
3. 复用性：示例模板可跨Agent复用（如电商客服/售后Agent共享示例）。
"""