def calculate_sigma_sq(Nq, Mq, As, h0, type_of_case, e0, gamma_f=0, b_p=0, b=0, a_s=0):
    """
    计算σ_sq值。

    :param Nq: 准永久组合下的轴力
    :param Mq: 准永久组合下的弯矩
    :param As: 钢筋截面积
    :param h0: 有效高度
    :param type_of_case: 计算情况的类型（1:轴拉，2:偏拉，3:受弯构件，4:偏压）
    :param e0: 原始偏心距
    :param gamma_f: 安全系数
    :param b_p: 梁的受压区宽度
    :param b: 梁的宽度
    :param a_s: 受拉钢筋合力点到截面受压边缘的距离
    :return: σ_sq值
    """

    if type_of_case == 1:
        # 第一种情况：轴拉
        sigma_sq = Nq / As
    elif type_of_case == 2:
        # 第二种情况：偏拉
        e_prime = e0 + 0.5 * h0 - a_s
        sigma_sq = (Nq * e_prime) / (As * (h0 - a_s))
    elif type_of_case == 3:
        # 第三种情况：受弯构件
        sigma_sq = Mq / (0.87 * h0 * As)
    elif type_of_case == 4:
        # 第四种情况：偏压
        # 计算η_s和e的值
        eta_s = 1  # 假设l0/h <= 14，则η_s = 1，对于l0/h > 14的情况，需要另外计算
        e = eta_s * e0 + gamma_f  # γs初步假设为0，如果有具体值需进行计算
        # 计算z的值
        z = 0.87 * h0 - 0.12 * (1 - gamma_f) * (h0 / e) ** 2
        # 确保z不超过限制
        z = min(z, 0.87 * h0)
        # 计算σ_sq的值
        sigma_sq = Nq * (e - z) / (As * z)
    else:
        raise ValueError("Invalid type_of_case. Must be 1, 2, 3, or 4.")

    return sigma_sq


# 示例使用函数
# 在实际应用中，需要将 ... 替换为具体数值或者通过用户输入获取
Nq = float(input("请输入准永久组合下的轴力 Nq (kN): "))  # 从用户那里获得或计算得到的准永久组合下的轴力
Mq = float(input("请输入准永久组合下的弯矩 Mq (kN·m): "))  # 从用户那里获得或计算得到的准永久组合下的弯矩
As = float(input("请输入钢筋截面积 As (mm^2): "))  # 钢筋截面积
h0 = float(input("请输入有效高度 h0 (mm): "))  # 有效高度

# 获取用户定义的计算情况类型
type_of_case = input("请输入计算情况类型（例如 '普通', '偏心', '悬挑'）: ")

# 根据 type_of_case 的值，接下来的代码会进行相应的计算
# ...


sigma_sq_result = calculate_sigma_sq(Nq, Mq, As, h0, type_of_case)
print(f"σ_sq = {sigma_sq_result}")
