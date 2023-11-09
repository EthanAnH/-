def calculate_total_rebar_area(diameters, quantities):
    """
    计算钢筋的总面积 As。

    :param diameters: 钢筋直径的列表。
    :param quantities: 对应每种直径钢筋的数量的列表。
    :return: 钢筋的总面积 As。
    """
    total_area = 0
    for diameter, quantity in zip(diameters, quantities):
        # 计算单根钢筋的面积
        area_per_rebar = 3.1416 * (diameter / 2) ** 2
        # 累加钢筋面积
        if quantity > 1:
            total_area += area_per_rebar * quantity
        else:
            total_area += area_per_rebar
    return total_area


def main():
    # 询问用户钢筋是否单一直径
    is_single_diameter = int(input("钢筋是否单一直径？(1是/2否): "))

    # 处理用户输入
    if is_single_diameter == 1:
        # 用户选择了单一直径
        # 获取钢筋根数和直径
        num_bars = int(input("请输入钢筋根数: "))
        diameter = float(input("请输入钢筋直径 (mm): "))
        # 计算钢筋面积
        As = calculate_total_rebar_area([diameter], [num_bars])

    elif is_single_diameter == 2:
        # 用户选择了多种直径
        # 获取不同直径钢筋的数量和直径
        num_bars = int(input("请输入不同直径钢筋的数量: "))
        diameters = []
        quantities = []
        for i in range(num_bars):
            diameter = float(input(f"请输入第 {i+1} 根钢筋的直径 (mm): "))
            quantity = int(input(f"请输入第 {i+1} 根钢筋的数量: "))
            diameters.append(diameter)
            quantities.append(quantity)
        # 计算钢筋面积
        As = calculate_total_rebar_area(diameters, quantities)

    else:
        # 用户输入错误
        print("请输入正确的选项。")
        return

    # 输出结果
    print(f"钢筋的总面积 As: {As:.3f} mm^2")


if __name__ == "__main__":
    main()
    # 其他输入
    Ap = float(input("请输入预应力筋面积 Ap (mm^2): "))
    Ate = float(input("请输入混凝土受拉区面积 Ate (mm^2): "))
    Mq = float(input("请输入弯矩 Mq (kN*m): "))
    Es = float(input("请输入钢筋弹性模量 Es (GPa): "))
    cs = float(input("请输入混凝土压缩应变 cs (microstrain): "))


def calculate_crack_width(
    As, Ap, Ate, Mq, Es, cs, diameters, quantities, f_tk, structural_situation
):
    """
    计算最大裂缝宽度 wmax。

    :param As: 钢筋面积 As (mm^2)。
    :param Ap: 预应力筋面积 Ap (mm^2)。
    :param Ate: 混凝土受拉区面积 Ate (mm^2)。
    :param Mq: 弯矩 Mq (kN*m)。
    :param Es: 钢筋弹性模量 Es (GPa)。
    :param cs: 混凝土压缩应变 cs (microstrain)。
    :param diameters: 钢筋直径的列表。
    :param quantities: 对应每种直径钢筋的数量的列表。
    :param f_tk: 钢筋屈服强度 ftk (MPa)。
    :param structural_situation: 结构情况 (普通/偏心/悬挑)。
    :return: 最大裂缝宽度 wmax (mm)。
    """

    # 计算钢筋总面积
    total_area = calculate_total_rebar_area(diameters, quantities)

    # 计算钢筋应力
    sigma_s = Mq / total_area

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
