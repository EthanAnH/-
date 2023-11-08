# 定义混凝土拉应力极限值f_tk的字典
concrete_grades = {
    "C20": 1.54,
    "C25": 1.78,
    "C30": 2.01,
    "C35": 2.2,
    "C40": 2.39,
    "C45": 2.51,
    "C50": 2.64,
    "C55": 2.74,
    "C60": 2.85
}

# 定义一个函数来执行第二步的比较操作
def check_second_step(sigma_ck, concrete_type, 环境类别):
    """
    比较计算得到的σ_ck与相应混凝土类型的拉应力极限f_tk。

    """
    # 如果环境类别为2，则进行比较
    if 环境类别 == 2:
        f_tk = concrete_grades.get(concrete_type)  # 从字典中获取f_tk值
        if f_tk is None:
            return False, f"未找到混凝土类型 {concrete_type} 的f_tk值。"
        # 比较σ_ck与f_tk，并返回比较结果
        if sigma_ck <= f_tk:
            return True, f"σ_ck = {sigma_ck} <= f_tk = {f_tk}，满足条件。"
        else:
            return False, f"σ_ck = {sigma_ck} > f_tk = {f_tk}，不满足条件。"
    else:
        # 如果不是二级环境类别，则跳过此步骤
        return None, "非二级环境类别，跳过此步骤。"

# 获取用户输入
sigma_ck = float(input("请输入σ_ck的值："))
concrete_type = input("请输入混凝土类型（例如：'C30'）：")
环境类别 = int(input("请输入环境类别（例如：2）："))

# 执行函数并打印结果
satisfies, result_message = check_second_step(sigma_ck, concrete_type, 环境类别)
print(result_message)
