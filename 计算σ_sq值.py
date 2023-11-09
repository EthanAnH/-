def calculate_sigma_sq(Nq, Mq, As, h0, type_of_case, e0, gamma_f, b_p, b, a_s):
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
        eta_s = 1  # 这里假设l0/h <= 14，则η_s = 1
        e = eta_s * e0 + gamma_f
        z = 0.87 * h0 - 0.12 * (1 - gamma_f) * (h0 / e) ** 2
        z = min(z, 0.87 * h0)
        sigma_sq = Nq * (e - z) / (As * z)
    else:
        raise ValueError("Invalid type_of_case. Must be 1, 2, 3, or 4.")
    return sigma_sq


# 以下是函数使用示例
# 获取用户输入的参数
Nq = float(input("请输入准永久组合下的轴力 Nq (kN): "))
Mq = float(input("请输入准永久组合下的弯矩 Mq (kN·m): "))
As = float(input("请输入钢筋截面积 As (mm^2): "))
h0 = float(input("请输入有效高度 h0 (mm): "))
e0 = float(input("请输入原始偏心距 e0 (mm): "))
gamma_f = float(input("请输入安全系数 gamma_f: "))
b_p = float(input("请输入梁的受压区宽度 b_p: "))
b = float(input("请输入梁的宽度 b: "))
a_s = float(input("请输入受拉钢筋合力点到截面受压边缘的距离 a_s: "))

# 提示用户输入计算情况类型
print("请选择计算情况类型：")
print("1 - 普通")
print("2 - 偏心")
print("3 - 悬挑")
print("4 - 偏压")
type_of_case = int(input("请输入对应的数字 (1, 2, 3, 或 4): "))

# 检查用户输入是否有效
if type_of_case not in [1, 2, 3, 4]:
    raise ValueError("Invalid type_of_case. Must be 1, 2, 3, or 4.")
# 调用函数并传递所有必要的参数
sigma_sq_result = calculate_sigma_sq(
    Nq, Mq, As, h0, type_of_case, e0, gamma_f, b_p, b, a_s
)
print(f"σ_sq = {sigma_sq_result}")

# 调用函数并传递所有必要的参数
sigma_sq_result = calculate_sigma_sq(
    Nq, Mq, As, h0, type_of_case, e0, gamma_f, b_p, b, a_s
)
print(f"σ_sq = {sigma_sq_result}")
