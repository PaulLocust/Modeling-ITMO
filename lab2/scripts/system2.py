# system2.py
import math

# Параметры для системы 2
lam = 0.4
b = 10.0
nu = 2.2
p = 0.3

# Расчет параметров гиперэкспоненциального распределения
term1 = (1 - p) / (2 * p) * (nu ** 2 - 1)
b1_prime = (1 + math.sqrt(term1)) * b
mu1 = 1 / b1_prime

term2 = p / (2 * (1 - p)) * (nu ** 2 - 1)
b2_prime = (1 - math.sqrt(term2)) * b
mu2 = 1 / b2_prime

# Вероятности фаз
q1 = p
q2 = 1 - p

print("Параметры гиперэкспоненциального распределения:")
print(f"  b1' = {b1_prime:.4f}, μ1 = {mu1:.4f}")
print(f"  b2' = {b2_prime:.4f}, μ2 = {mu2:.4f}")
print(f"  q1 = {q1:.2f}, q2 = {q2:.2f}")

# Стационарные вероятности из отчета
p_stationary = [0.0117, 0.0469, 0.0030, 0.1875, 0.0008, 0.7499, 0.0002]
codes = [
    (0, 0, 0),  # S0: прибор свободен, очередь пуста
    (1, 0, 0),  # S1: прибор на фазе П11, очередь пуста
    (0, 1, 0),  # S2: прибор на фазе П12, очередь пуста
    (1, 0, 1),  # S3: прибор на фазе П11, 1 заявка в очереди
    (0, 1, 1),  # S4: прибор на фазе П12, 1 заявка в очереди
    (1, 0, 2),  # S5: прибор на фазе П11, 2 заявки в очереди
    (0, 1, 2)  # S6: прибор на фазе П12, 2 заявки в очереди
]


def calculate_characteristics_system2():
    n_states = len(p_stationary)

    # Индексы состояний по характеристикам
    p_busy = []  # Прибор занят (любая фаза)
    p11_busy = []  # Прибор в фазе П11
    p12_busy = []  # Прибор в фазе П12
    o1_len = [[] for _ in range(3)]  # Длина очереди (0, 1, 2)
    loss_states = []  # Состояния с потерями

    for i, (p11, p12, o1) in enumerate(codes):
        if p11 == 1 or p12 == 1:
            p_busy.append(i)
        if p11 == 1:
            p11_busy.append(i)
        if p12 == 1:
            p12_busy.append(i)
        if o1 < len(o1_len):
            o1_len[o1].append(i)

        # Потери: очередь заполнена (O1=2)
        if o1 == 2:
            loss_states.append(i)

    def safe_sum(indices):
        return sum(p_stationary[i] for i in indices if i < n_states)

    print("\n=== СИСТЕМА 2 ХАРАКТЕРИСТИКИ ===\n")
    print("Архитектура: 1 прибор с гиперэкспоненциальным распределением времени обслуживания")
    print("Очередь: максимальная длина = 2 заявки\n")

    # 1. НАГРУЗКА
    y_total = lam * b  # Общая нагрузка системы

    print("Нагрузка:")
    print(f"  Y = λ × b = {lam} × {b} = {y_total:.4f}")

    # 2. ЗАГРУЗКА
    rho = safe_sum(p_busy)  # Доля времени занят прибор

    print("\nЗагрузка:")
    print(f"  ρ = Σπ(прибор занят) = {rho:.4f}")

    # 3. ДЛИНА ОЧЕРЕДИ
    l_q = 1 * safe_sum(o1_len[1]) + 2 * safe_sum(o1_len[2])

    print("\nДлина очереди:")
    print(f"  L_q = 1 × Σπ(O1=1) + 2 × Σπ(O1=2) = {l_q:.4f}")

    # 4. ЧИСЛО ЗАЯВОК В СИСТЕМЕ
    m_system = rho + l_q

    print("\nЧисло заявок:")
    print(f"  M = ρ + L_q = {rho:.4f} + {l_q:.4f} = {m_system:.4f}")

    # 5. ВЕРОЯТНОСТЬ ПОТЕРЬ
    p_loss = safe_sum(loss_states)

    print("\nВероятность потери:")
    print(f"  π = Σπ(O1=2) = {p_loss:.4f}")

    # 6. ПРОИЗВОДИТЕЛЬНОСТЬ
    lam_eff = lam * (1 - p_loss)

    print("\nПроизводительность:")
    print(f"  λ′ = λ × (1 - π) = {lam} × (1 - {p_loss:.4f}) = {lam_eff:.4f}")

    # 7. ВРЕМЯ ОЖИДАНИЯ
    if lam_eff > 0:
        w_q = l_q / lam_eff
    else:
        w_q = 0

    print("\nВремя ожидания:")
    print(f"  W_q = L_q / λ′ = {l_q:.4f} / {lam_eff:.4f} = {w_q:.4f} с")

    # 8. ВРЕМЯ ПРЕБЫВАНИЯ
    w_system = w_q + b  # Время пребывания = время ожидания + время обслуживания

    print("\nВремя пребывания:")
    print(f"  W = W_q + b = {w_q:.4f} + {b:.4f} = {w_system:.4f} с")

    # Дополнительная информация о фазах
    rho11 = safe_sum(p11_busy)  # Загрузка фазы П11
    rho12 = safe_sum(p12_busy)  # Загрузка фазы П12

    print("\nДополнительная информация по фазам:")
    print(f"  Загрузка фазы П11: ρ₁₁ = Σπ(П11=1) = {rho11:.4f}")
    print(f"  Загрузка фазы П12: ρ₁₂ = Σπ(П12=1) = {rho12:.4f}")
    print(f"  Проверка: ρ₁₁ + ρ₁₂ = {rho11 + rho12:.4f} (должно быть равно ρ)")

    # Проверка формулой Литтла
    print("\nПроверка формулой Литтла:")
    print(f"  M = {m_system:.4f}, λ′ × W = {lam_eff * w_system:.4f}")
    print(f"  L_q = {l_q:.4f}, λ′ × W_q = {lam_eff * w_q:.4f}")
    print(f"  Разница M: {abs(m_system - lam_eff * w_system):.6f}")
    print(f"  Разница L_q: {abs(l_q - lam_eff * w_q):.6f}")

    return {
        # Нагрузка
        'y_total': y_total,
        # Загрузка
        'rho': rho,
        # Длина очереди
        'l_q_total': l_q,
        # Число заявок
        'm_total': m_system,
        # Вероятность потерь
        'p_loss_total': p_loss,
        # Производительность
        'lam_eff_total': lam_eff,
        # Время ожидания
        'w_q': w_q,
        # Время пребывания
        'w_total': w_system
    }


if __name__ == "__main__":
    calculate_characteristics_system2()