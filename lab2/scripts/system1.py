# system1.py
import math

# Параметры для варианта 21/30, NG=9
lam = 0.4
b = 10.0
mu = 1 / b
P1, P2, P3 = 0.6, 0.1, 0.3

p = [0.0805, 0.1933, 0.0322, 0.0967, 0.0773, 0.2320, 0.0387, 0.0129, 0.0928, 0.0309, 0.0155, 0.0052, 0.0371, 0.0124,
     0.0062, 0.0021, 0.0148, 0.0049, 0.0025, 0.0008, 0.0059, 0.0020, 0.0010, 0.0024]

codes = [(0, 0, 0, 0), (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 1), (1, 1, 0, 0), (1, 0, 0, 1), (0, 1, 0, 1), (0, 1, 1, 0),
         (1, 1, 0, 1), (1, 1, 1, 0), (0, 1, 1, 1), (0, 1, 2, 0), (1, 1, 1, 1), (1, 1, 2, 0), (0, 1, 2, 1), (0, 1, 3, 0),
         (1, 1, 2, 1), (1, 1, 3, 0), (0, 1, 3, 1), (0, 1, 4, 0), (1, 1, 3, 1), (1, 1, 4, 0), (0, 1, 4, 1), (1, 1, 4, 1)]


def calculate_characteristics_system1():
    n_states = len(p)

    # Индексы состояний по характеристикам
    p1_busy = []  # Прибор 1 занят
    p2_busy = []  # Прибор 2 занят
    p3_busy = []  # Прибор 3 занят
    o2_len = [[] for _ in range(5)]  # Длина очереди к прибору 2 (0-4)

    # Состояния с потерями по типам заявок
    loss_P1 = []  # Потери для заявок на П1
    loss_P2 = []  # Потери для заявок на П2
    loss_P3 = []  # Потери для заявок на П3

    for i, (n1, n2, o2, n3) in enumerate(codes):
        if n1 == 1: p1_busy.append(i)
        if n2 == 1: p2_busy.append(i)
        if n3 == 1: p3_busy.append(i)
        if o2 < len(o2_len): o2_len[o2].append(i)

        # ПРАВИЛЬНЫЙ РАСЧЕТ ПОТЕРЬ:
        # Потери для заявок на П1: если П1 занят
        if n1 == 1:
            loss_P1.append(i)

        # Потери для заявок на П2: если П2 занят И очередь заполнена (o2=4)
        if n2 == 1 and o2 == 4:
            loss_P2.append(i)

        # Потери для заявок на П3: если П3 занят
        if n3 == 1:
            loss_P3.append(i)

    def safe_sum(indices):
        return sum(p[i] for i in indices if i < n_states)

    print("=== СИСТЕМА 1 ХАРАКТЕРИСТИКИ ===\n")

    # 1. НАГРУЗКА
    y_total = lam * b  # Общая нагрузка системы
    y1 = lam * b * P1  # Нагрузка на прибор 1
    y2 = lam * b * P2  # Нагрузка на прибор 2
    y3 = lam * b * P3  # Нагрузка на прибор 3

    print("Нагрузка:")
    print(f"  П1: Y₁ = λ × b × P1 = {lam} × {b} × {P1} = {y1:.4f}")
    print(f"  П2: Y₂ = λ × b × P2 = {lam} × {b} × {P2} = {y2:.4f}")
    print(f"  П3: Y₃ = λ × b × P3 = {lam} × {b} × {P3} = {y3:.4f}")
    print(f"  Суммарная: Y = Y₁ + Y₂ + Y₃ = {y1 + y2 + y3:.4f}")

    # 2. ЗАГРУЗКА
    rho1 = safe_sum(p1_busy)  # Доля времени занят прибор 1
    rho2 = safe_sum(p2_busy)  # Доля времени занят прибор 2
    rho3 = safe_sum(p3_busy)  # Доля времени занят прибор 3
    rho_avg = (rho1 + rho2 + rho3) / 3

    print("\nЗагрузка:")
    print(f"  П1: ρ₁ = Σπ(П1=1) = {rho1:.4f}")
    print(f"  П2: ρ₂ = Σπ(П2=1) = {rho2:.4f}")
    print(f"  П3: ρ₃ = Σπ(П3=1) = {rho3:.4f}")
    print(f"  Средняя: ρ = (ρ₁ + ρ₂ + ρ₃)/3 = {rho_avg:.4f}")

    # 3. ДЛИНА ОЧЕРЕДИ
    l_q2 = sum(k * safe_sum(o2_len[k]) for k in range(1, 5))  # Очередь только у П2
    l_q1 = 0.0  # У П1 нет очереди
    l_q3 = 0.0  # У П3 нет очереди
    l_q_total = l_q1 + l_q2 + l_q3

    print("\nДлина очереди:")
    print(f"  П1: L_q1 = 0 (нет очереди)")
    print(f"  П2: L_q2 = Σ(k × Σπ(O2=k)) = {l_q2:.4f}")
    print(f"  П3: L_q3 = 0 (нет очереди)")
    print(f"  Суммарная: L_q = L_q1 + L_q2 + L_q3 = {l_q_total:.4f}")

    # 4. ЧИСЛО ЗАЯВОК В СИСТЕМЕ
    m1 = rho1 + l_q1  # Число заявок у П1
    m2 = rho2 + l_q2  # Число заявок у П2
    m3 = rho3 + l_q3  # Число заявок у П3
    m_total = m1 + m2 + m3

    print("\nЧисло заявок:")
    print(f"  П1: M₁ = ρ₁ + L_q1 = {rho1:.4f} + {l_q1:.4f} = {m1:.4f}")
    print(f"  П2: M₂ = ρ₂ + L_q2 = {rho2:.4f} + {l_q2:.4f} = {m2:.4f}")
    print(f"  П3: M₃ = ρ₃ + L_q3 = {rho3:.4f} + {l_q3:.4f} = {m3:.4f}")
    print(f"  Суммарное: M = M₁ + M₂ + M₃ = {m_total:.4f}")

    # 5. ВЕРОЯТНОСТЬ ПОТЕРЬ
    p_loss_P1 = safe_sum(loss_P1)  # Вероятность потерь для заявок на П1
    p_loss_P2 = safe_sum(loss_P2)  # Вероятность потерь для заявок на П2
    p_loss_P3 = safe_sum(loss_P3)  # Вероятность потерь для заявок на П3
    p_loss_total = P1 * p_loss_P1 + P2 * p_loss_P2 + P3 * p_loss_P3

    print("\nВероятность потери:")
    print(f"  П1: π₁ = Σπ(П1=1) = {p_loss_P1:.4f}")
    print(f"  П2: π₂ = Σπ(П2=1 и O2=4) = {p_loss_P2:.4f}")
    print(f"  П3: π₃ = Σπ(П3=1) = {p_loss_P3:.4f}")
    print(f"  Общая: π = P1×π₁ + P2×π₂ + P3×π₃ = {p_loss_total:.4f}")

    # 6. ПРОИЗВОДИТЕЛЬНОСТЬ
    lam_eff_total = lam * (1 - p_loss_total)  # Общая производительность
    lam_eff1 = lam * P1 * (1 - p_loss_P1)  # Производительность П1
    lam_eff2 = lam * P2 * (1 - p_loss_P2)  # Производительность П2
    lam_eff3 = lam * P3 * (1 - p_loss_P3)  # Производительность П3

    print("\nПроизводительность:")
    print(f"  П1: λ′₁ = λ × P1 × (1 - π₁) = {lam} × {P1} × (1 - {p_loss_P1:.4f}) = {lam_eff1:.4f}")
    print(f"  П2: λ′₂ = λ × P2 × (1 - π₂) = {lam} × {P2} × (1 - {p_loss_P2:.4f}) = {lam_eff2:.4f}")
    print(f"  П3: λ′₃ = λ × P3 × (1 - π₃) = {lam} × {P3} × (1 - {p_loss_P3:.4f}) = {lam_eff3:.4f}")
    print(f"  Общая: λ′ = λ × (1 - π) = {lam} × (1 - {p_loss_total:.4f}) = {lam_eff_total:.4f}")

    # 7. ВРЕМЯ ОЖИДАНИЯ
    w_q1 = 0.0  # У П1 нет очереди
    w_q2 = l_q2 / lam_eff2 if lam_eff2 > 0 else 0.0  # Время ожидания у П2
    w_q3 = 0.0  # У П3 нет очереди
    w_q_total = l_q_total / lam_eff_total

    print("\nВремя ожидания:")
    print(f"  П1: W_q1 = 0 (нет очереди)")
    print(f"  П2: W_q2 = L_q2 / λ′₂ = {l_q2:.4f} / {lam_eff2:.4f} = {w_q2:.4f} с")
    print(f"  П3: W_q3 = 0 (нет очереди)")
    print(f"  Общее: Wq = L_q / λ′ = {l_q_total:.4f} / {lam_eff_total:.4f} = {w_q_total:.4f} с")

    # 8. ВРЕМЯ ПРЕБЫВАНИЯ
    w1 = m1 / lam_eff1 if lam_eff1 > 0 else 0.0  # Время пребывания у П1
    w2 = m2 / lam_eff2 if lam_eff2 > 0 else 0.0  # Время пребывания у П2
    w3 = m3 / lam_eff3 if lam_eff3 > 0 else 0.0  # Время пребывания у П3
    w_total = m_total / lam_eff_total if lam_eff_total > 0 else 0.0

    print("\nВремя пребывания:")
    print(f"  П1: W₁ = W_q1 + b = {w_q1:.4f} + {b:.4f} = {w1:.4f} с")
    print(f"  П2: W₂ = W_q2 + b = {w_q2:.4f} + {b:.4f} = {w2:.4f} с")
    print(f"  П3: W₃ = W_q3 + b = {w_q3:.4f} + {b:.4f} = {w3:.4f} с")
    print(f"  Общее: W = W_q + b = {w_q_total:.4f} + {b:.4f} = {w_total:.4f} с")

    # Проверка формулой Литтла
    print("\nПроверка формулой Литтла:")
    print(f"  M = {m_total:.4f}, λ′ × W = {lam_eff_total * w_total:.4f}")
    print(f"  L_q = {l_q_total:.4f}, λ′ × W_q2 = {lam_eff_total * w_q2:.4f}")
    print(f"  Разница M: {abs(m_total - lam_eff_total * w_total):.6f}")

    return {
        # Нагрузка
        'y1': y1, 'y2': y2, 'y3': y3, 'y_total': y_total,
        # Загрузка
        'rho1': rho1, 'rho2': rho2, 'rho3': rho3, 'rho_avg': rho_avg,
        # Длина очереди
        'l_q1': l_q1, 'l_q2': l_q2, 'l_q3': l_q3, 'l_q_total': l_q_total,
        # Число заявок
        'm1': m1, 'm2': m2, 'm3': m3, 'm_total': m_total,
        # Вероятность потерь
        'p_loss1': p_loss_P1, 'p_loss2': p_loss_P2, 'p_loss3': p_loss_P3, 'p_loss_total': p_loss_total,
        # Производительность
        'lam_eff1': lam_eff1, 'lam_eff2': lam_eff2, 'lam_eff3': lam_eff3, 'lam_eff_total': lam_eff_total,
        # Время ожидания
        'w_q1': w_q1, 'w_q2': w_q2, 'w_q3': w_q3, 'w_q_total': w_q_total,
        # Время пребывания
        'w1': w1, 'w2': w2, 'w3': w3, 'w_total': w_total
    }


if __name__ == "__main__":
    calculate_characteristics_system1()