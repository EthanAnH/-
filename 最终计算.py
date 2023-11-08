def calculate_crack_width(
    As, Ap, Ate, Mq, Es, cs, diameters, quantities, f_tk, structural_situation
):
    # 计算钢筋应力
    sigma_s = Mq / As

    # 计算钢筋配筋率
    rho_te = (As + Ap) / Ate

    # 计算裂缝形状系数ψ
    psi = 1.1 - 0.65 * (f_tk / (rho_te * sigma_s))
    psi = max(min(psi, 1), 0)  # 确保ψ的值在0和1之间

    # 计算deq
    d_eq = sum(n * d ** 2 for n, d in zip(quantities, diameters)) / sum(
        n * d for n, d in zip(quantities, diameters)
    )

    # αcr值根据结构情况确定
    alpha_cr_values = {"普通": 1.9, "偏心": 2.4, "悬挑": 2.7}
    alpha_cr = alpha_cr_values.get(
        structural_situation, 1.9
    )  # Default to "普通" if not found

    # 计算最大裂缝宽度wmax
    w_max = alpha_cr * psi * (sigma_s / Es) * (1.9 * cs + 0.08 * (d_eq / rho_te))

    return w_max


# ftk字典
f_tk_values = {
    "C20": 1.54,
    "C25": 1.78,
    "C30": 2.01,
    "C35": 2.2,
    "C40": 2.39,
    "C45": 2.51,
    "C50": 2.64,
    "C55": 2.74,
    "C60": 2.85,
}

# Prompt user for input values
As = float(input("请输入钢筋面积 As (mm^2): "))
Ap = float(input("请输入预应力筋面积 Ap (mm^2): "))
Ate = float(input("请输入混凝土受拉区面积 Ate (mm^2): "))
Mq = float(input("请输入弯矩 Mq (kN*m): "))
Es = float(input("请输入钢筋弹性模量 Es (GPa): "))
cs = float(input("请输入混凝土压缩应变 cs (microstrain): "))

# Ask for the number of different rebar sizes
num_bars = int(input("请输入不同直径钢筋的数量: "))
diameters = []
quantities = []
for i in range(num_bars):
    diameter = float(input(f"请输入第 {i+1} 根钢筋的直径 (mm): "))
    quantity = int(input(f"请输入第 {i+1} 根钢筋的数量: "))
    diameters.append(diameter)
    quantities.append(quantity)
# Prompt the user for the concrete grade
concrete_grade = input("请输入混凝土等级 (例如: C30): ").upper()
if concrete_grade in f_tk_values:
    f_tk = f_tk_values[concrete_grade]
else:
    print("未知的混凝土等级，请输入正确的等级。")
    # Optionally, you can loop here to ask again or exit the program
    raise ValueError("未知的混凝土等级。")
# Prompt the user for the structural situation
structural_situation = input("请输入结构情况 (普通/偏心/悬挑): ")

# Call the function with the user inputs
w_max = calculate_crack_width(
    As, Ap, Ate, Mq, Es, cs, diameters, quantities, f_tk, structural_situation
)
print(f"最大裂缝宽度 w_max: {w_max:.3f} mm")
