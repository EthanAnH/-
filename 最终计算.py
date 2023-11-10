def calculate_total_rebar_area(diameters, quantities):
    total_area = 0
    for diameter, quantity in zip(diameters, quantities):
        area_per_rebar = 3.1416 * (diameter / 2) ** 2
        total_area += area_per_rebar * quantity
    return total_area


def calculate_sigma_sq(Nq, Mq, As, h0, type_of_case, e0, gamma_f, b_p, b, a_s):
    if type_of_case == 1:
        sigma_sq = Nq / As
    elif type_of_case == 2:
        e_prime = e0 + 0.5 * h0 - a_s
        sigma_sq = (Nq * e_prime) / (As * (h0 - a_s))
    elif type_of_case == 3:
        sigma_sq = Mq / (0.87 * h0 * As)
    elif type_of_case == 4:
        eta_s = 1  # Assuming l0/h <= 14, hence η_s = 1
        e = eta_s * e0 + gamma_f
        z = 0.87 * h0 - 0.12 * (1 - gamma_f) * (h0 / e) ** 2
        z = min(z, 0.87 * h0)
        sigma_sq = Nq * (e - z) / (As * z)
    else:
        raise ValueError("Invalid type_of_case. Must be 1, 2, 3, or 4.")
    return sigma_sq


def calculate_crack_width(
    As,
    Ap,
    Ate,
    sigma_s,
    Es,
    cs,
    diameters,
    quantities,
    f_tk,
    structural_situation,
    alpha_cr_dict,
):
    rho_te = (As + Ap) / Ate
    psi = 1.1 - 0.65 * (f_tk / (rho_te * sigma_s))
    psi = max(min(psi, 1), 0)
    d_eq = sum(n * d ** 2 for n, d in zip(quantities, diameters)) / sum(
        n * d for n, d in zip(quantities, diameters)
    )
    alpha_cr = alpha_cr_dict.get(structural_situation, 1.9)
    Es_MPa = Es * 1000
    w_max = alpha_cr * psi * (sigma_s / Es_MPa) * (1.9 * cs + 0.08 * (d_eq / rho_te))
    return w_max


def main():
    # User inputs for rebar configuration
    is_single_diameter = int(
        input("Is the rebar of a single diameter? (1 for yes / 2 for no): ")
    )
    diameters = []
    quantities = []

    if is_single_diameter == 1:
        num_bars = int(input("Enter the number of rebars: "))
        diameter = float(input("Enter the diameter of the rebars (mm): "))
        diameters.append(diameter)
        quantities.append(num_bars)
    elif is_single_diameter == 2:
        num_diameters = int(input("Enter the number of different rebar diameters: "))
        for i in range(num_diameters):
            diameter = float(input(f"Enter the diameter of rebar #{i+1} (mm): "))
            quantity = int(input("Enter the quantity for this diameter: "))
            diameters.append(diameter)
            quantities.append(quantity)
    else:
        print("Invalid input.")
        return
    As = calculate_total_rebar_area(diameters, quantities)

    # User inputs for sigma_sq calculation
    Nq = float(input("Enter the axial force Nq (kN): "))
    Mq = float(input("Enter the bending moment Mq (kN*m): "))
    h0 = float(input("Enter the effective depth h0 (mm): "))
    e0 = float(input("Enter the initial eccentricity e0 (mm): "))
    gamma_f = float(input("Enter the safety factor gamma_f: "))
    b_p = float(input("Enter the width of the compressed zone of the beam b_p: "))
    b = float(input("Enter the width of the beam b: "))
    a_s = float(input("请输入as: "))
    type_of_case = int(input("Enter the type of case (1, 2, 3, or 4): "))
    sigma_s = calculate_sigma_sq(Nq, Mq, As, h0, type_of_case, e0, gamma_f, b_p, b, a_s)

    # User inputs for crack width calculation
    Ate = float(input("Enter the area of the tensile concrete zone Ate (mm^2): "))
    Es = float(input("Enter the modulus of elasticity of the rebar Es (GPa): "))
    cs = float(input("Enter the concrete strain cs (microstrain): "))
    f_tk = float(
        input("Enter the characteristic tensile strength of concrete f_tk (MPa): ")
    )
    structural_situation = input(
        "Enter the structural situation (normal, eccentric, cantilever): "
    )
    alpha_cr_dict = {"normal": 1.9, "eccentric": 2.4, "cantilever": 2.7}

    # Calculate and print the crack width
    w_max = calculate_crack_width(
        As,
        Nq,
        Ate,
        sigma_s,
        Es,
        cs,
        diameters,
        quantities,
        f_tk,
        structural_situation,
        alpha_cr_dict,
    )
    print(f"The maximum crack width w_max is: {w_max:.3f} mm")


if __name__ == "__main__":
    main()
