# -*- coding: utf-8 -*-
"""
LangChain1.0 基础PromptTemplate案例（修正版）
知识点：参数化模板 + 自动验证变量缺失
场景：电商Agent解释订单相关概念，面向不同用户（新手/商家），控制字数
"""
from langchain_core.prompts import PromptTemplate



# ====================== 没用PromptTemplate的写法（痛点示例） ======================
def build_prompt_without_template(concept, audience, word_count):
    """
    硬编码+手动拼接，痛点：
    1. 提示词规则硬编码，改"面向xx群体"为"针对xx用户"需改函数；
    2. 参数类型错误（如word_count传字符串）无法提前发现；
    3. 漏传参数（如少传audience）运行时才报错。
    """
    # 硬编码提示词，规则耦合在代码中
    prompt = f"请解释{concept}的核心概念，面向{audience}群体，控制在{word_count}字以内。"
    return prompt


# 测试：看似正常，但隐藏风险。
print("=== 没用PromptTemplate的输出 ===")
try:
    # 正常传参
    prompt1 = build_prompt_without_template("订单退款规则", "新手用户", 200)
    print(prompt1)
    # 错误传参（word_count传字符串，语法不报错，但模型理解错）
    prompt2 = build_prompt_without_template("订单退款规则", "新手用户", "200字")
    print(prompt2)  # 输出包含"200字"，模型会误解字数要求
except Exception as e:
    print(f"错误：{e}")

# ====================== 用了PromptTemplate的写法（提升示例） ======================
# 1. 定义字符串模板（规则与代码解耦，可抽离到配置文件）
template = "请解释{concept}的核心概念，面向{audience}群体，控制在{word_count}字以内。"

# 2. 实例化 template 模板
# PromptTemplate.from_template() :
# LangChain 提供的一个类方法，用于 从字符串模板快速创建 PromptTemplate 实例
# 能 自动提取模板字符串中的占位符（花括号 {} 内的变量）
# 避免了手动定义输入变量时的拼写错误或遗漏
prompt_template = PromptTemplate.from_template(template)


# 3. 填充参数生成提示词（参数类型错误/漏传直接报错）
print("\n=== 用了PromptTemplate的输出 ===")
try:
    # 正常传参
    # .format()：
    # LangChain1.0中，PromptTemplate类 的核心方法
    # 用于将模板中的占位符 替换为实际参数值。调用时，会将键值对参数 填入 template模板 的对应位置，返回 最终生成的提示词字符串
    # 漏传参数时，format()方法会直接抛出KeyError，提示参数缺失（实现了变量缺失的自动验证）
    prompt3 = prompt_template.format(
        concept="订单退款规则",
        audience="新手用户",
        word_count=200
    )
    print(prompt3)

    # 错误传参（漏传audience，直接报错，提前规避线上问题）
    prompt4 = prompt_template.format(concept="订单退款规则", word_count=200)
except Exception as e:
    print(f"参数错误（提前发现）：{e}")

# ====================== 核心提升总结 ======================
"""
1. 维护性：模板字符串可抽离到YAML/数据库，运营无需改代码即可调整规则；
2. 稳定性：format()方法自动检查变量缺失，避免线上崩溃；
3. 易用性：参数化注入，无需手动拼接字符串，减少格式错误。
"""