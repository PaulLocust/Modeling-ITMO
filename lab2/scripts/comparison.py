# comparison.py
import matplotlib.pyplot as plt
import numpy as np
from system1 import calculate_characteristics_system1
from system2 import calculate_characteristics_system2


def calculate_relative_difference(sys1, sys2):
    """Рассчитывает относительную разность характеристик в процентах"""

    print("\n" + "=" * 70)
    print("ОТНОСИТЕЛЬНАЯ РАЗНОСТЬ ХАРАКТЕРИСТИК (%)")
    print("=" * 70)

    print("РАСЧЕТ ОТНОСИТЕЛЬНОЙ РАЗНОСТИ:")
    print("• Для характеристик 'больше = лучше' (производительность, загрузка):")
    print("  Разность = ((лучшее - худшее) / худшее) × 100%")
    print("• Для характеристик 'меньше = лучше' (потери, время, заявки):")
    print("  Разность = ((худшее - лучшее) / лучшее) × 100%")
    print("• Положительная разность = СИСТЕМА 1 лучше")
    print("• Отрицательная разность = СИСТЕМА 2 лучше\n")

    # Для характеристик где больше значение лучше
    characteristics_better_higher = {
        'Производительность (λ′)': (sys1['lam_eff_total'], sys2['lam_eff_total']),
        'Загрузка системы (ρ)': (sys1['rho_avg'], sys2['rho']),
        'Нагрузка (Y)': (sys1['y_total'], sys2['y_total'])
    }

    # Для характеристик где меньше значение лучше
    characteristics_better_lower = {
        'Вероятность потерь (π)': (sys1['p_loss_total'], sys2['p_loss_total']),
        'Ср. время пребывания (W)': (sys1['w_total'], sys2['w_total']),
        'Ср. время ожидания (W_q)': (sys1['w_q2'], sys2['w_q']),
        'Ср. число заявок (M)': (sys1['m_total'], sys2['m_total']),
        'Длина очереди (L_q)': (sys1['l_q_total'], sys2['l_q_total'])
    }

    print(f"\n{'ХАРАКТЕРИСТИКА':<35} {'СИСТЕМА 1':<12} {'СИСТЕМА 2':<12} {'РАЗНОСТЬ':<15} {'ВЫИГРЫШ':<10}")
    print("-" * 85)

    # Характеристики где больше = лучше
    for name, (val1, val2) in characteristics_better_higher.items():
        if val1 > val2:
            diff = ((val1 - val2) / val2) * 100
            winner = "СИСТЕМА 1"
            sign = "+"
        else:
            diff = ((val2 - val1) / val1) * 100
            winner = "СИСТЕМА 2"
            sign = "-"

        print(f"{name:<35} {val1:<12.4f} {val2:<12.4f} {sign}{abs(diff):<13.1f}% {winner:<10}")

    # Характеристики где меньше = лучше
    for name, (val1, val2) in characteristics_better_lower.items():
        if val1 < val2:
            diff = ((val2 - val1) / val1) * 100
            winner = "СИСТЕМА 1"
            sign = "+"
        else:
            diff = ((val1 - val2) / val2) * 100
            winner = "СИСТЕМА 2"
            sign = "-"

        print(f"{name:<35} {val1:<12.4f} {val2:<12.4f} {sign}{abs(diff):<13.1f}% {winner:<10}")

    # Сводная статистика
    print("\n" + "=" * 85)
    print("СВОДНАЯ СТАТИСТИКА ПОБЕД:")
    print("=" * 85)

    wins_sys1 = 0
    wins_sys2 = 0

    # Подсчет побед для характеристик где больше = лучше
    for val1, val2 in characteristics_better_higher.values():
        if val1 > val2:
            wins_sys1 += 1
        else:
            wins_sys2 += 1

    # Подсчет побед для характеристик где меньше = лучше
    for val1, val2 in characteristics_better_lower.values():
        if val1 < val2:
            wins_sys1 += 1
        else:
            wins_sys2 += 1

    total_characteristics = len(characteristics_better_higher) + len(characteristics_better_lower)

    print(
        f"СИСТЕМА 1 выигрывает в: {wins_sys1} из {total_characteristics} характеристик ({wins_sys1 / total_characteristics * 100:.1f}%)")
    print(
        f"СИСТЕМА 2 выигрывает в: {wins_sys2} из {total_characteristics} характеристик ({wins_sys2 / total_characteristics * 100:.1f}%)")

    if wins_sys1 > wins_sys2:
        print(f"🏆 ОБЩИЙ ВЫИГРЫШ: СИСТЕМА 1")
    elif wins_sys2 > wins_sys1:
        print(f"🏆 ОБЩИЙ ВЫИГРЫШ: СИСТЕМА 2")
    else:
        print(f"⚖️ НИЧЬЯ")


def create_comparison_chart(sys1, sys2):
    """Создает график всех характеристик систем"""

    # Все 8 характеристик для сравнения
    characteristics = [
        'Нагрузка\n(Y)',
        'Загрузка\n(ρ)',
        'Длина\nочереди\n(L_q)',
        'Число\nзаявок\n(M)',
        'Вероятность\nпотерь\n(π)',
        'Производи-\nтельность\n(λ′)',
        'Время\nожидания\n(W_q)',
        'Время\nпребывания\n(W)'
    ]

    # Значения для System1
    sys1_values = [
        sys1['y_total'],  # Нагрузка суммарная
        sys1['rho_avg'],  # Загрузка средняя
        sys1['l_q_total'],  # Длина очереди суммарная
        sys1['m_total'],  # Число заявок суммарное
        sys1['p_loss_total'],  # Вероятность потерь общая
        sys1['lam_eff_total'],  # Производительность общая
        sys1['w_q2'],  # Время ожидания (для П2, где есть очередь)
        sys1['w_total']  # Время пребывания общее
    ]

    # Значения для System2
    sys2_values = [
        sys2['y_total'],  # Нагрузка суммарная
        sys2['rho'],  # Загрузка
        sys2['l_q_total'],  # Длина очереди суммарная
        sys2['m_total'],  # Число заявок суммарное
        sys2['p_loss_total'],  # Вероятность потерь общая
        sys2['lam_eff_total'],  # Производительность общая
        sys2['w_q'],  # Время ожидания
        sys2['w_total']  # Время пребывания общее
    ]

    # Создаем график
    fig, ax = plt.subplots(figsize=(18, 8))

    x = np.arange(len(characteristics))
    width = 0.35

    bars1 = ax.bar(x - width / 2, sys1_values, width, label='СИСТЕМА 1', color='blue', alpha=0.7)
    bars2 = ax.bar(x + width / 2, sys2_values, width, label='СИСТЕМА 2', color='red', alpha=0.7)

    ax.set_xlabel('Характеристики', fontsize=14, fontweight='bold')
    ax.set_ylabel('Значения', fontsize=14, fontweight='bold')
    ax.set_title('Сравнение характеристик систем массового обслуживания', fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(characteristics, rotation=45, ha='right', fontsize=11)
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3, linestyle='--')

    # Добавляем значения на столбцы
    max_val = max(max(sys1_values), max(sys2_values))
    offset = 0.02 * max_val

    for bar, value in zip(bars1, sys1_values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + offset,
                f'{value:.3f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

    for bar, value in zip(bars2, sys2_values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + offset,
                f'{value:.3f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

    plt.tight_layout()
    plt.savefig('comparison_chart.png', dpi=300, bbox_inches='tight')
    plt.show()


def compare_systems():
    sys1 = calculate_characteristics_system1()
    sys2 = calculate_characteristics_system2()

    print("\n" + "=" * 70)
    print("СРАВНИТЕЛЬНЫЙ АНАЛИЗ СИСТЕМ")
    print("=" * 70)

    print(f"\n{'ХАРАКТЕРИСТИКА':<25} {'СИСТЕМА 1':<12} {'СИСТЕМА 2':<12}")
    print("-" * 50)
    print(f"{'Нагрузка (Y)':<25} {sys1['y_total']:<12.4f} {sys2['y_total']:<12.4f}")
    print(f"{'Загрузка (ρ)':<25} {sys1['rho_avg']:<12.4f} {sys2['rho']:<12.4f}")
    print(f"{'Длина очереди (L_q)':<25} {sys1['l_q_total']:<12.4f} {sys2['l_q_total']:<12.4f}")
    print(f"{'Число заявок (M)':<25} {sys1['m_total']:<12.4f} {sys2['m_total']:<12.4f}")
    print(f"{'Вероятность потерь (π)':<25} {sys1['p_loss_total']:<12.4f} {sys2['p_loss_total']:<12.4f}")
    print(f"{'Производительность (λ′)':<25} {sys1['lam_eff_total']:<12.4f} {sys2['lam_eff_total']:<12.4f}")
    print(f"{'Время ожидания (W_q)':<25} {sys1['w_q2']:<12.4f} {sys2['w_q']:<12.4f}")
    print(f"{'Время пребывания (W)':<25} {sys1['w_total']:<12.4f} {sys2['w_total']:<12.4f}")

    # Расчет относительной разности
    calculate_relative_difference(sys1, sys2)

    # Критерий эффективности
    print("\n" + "=" * 70)
    print("КРИТЕРИЙ ЭФФЕКТИВНОСТИ:")
    print("=" * 70)

    n1, n2 = 21, 30
    if (n1 + n2) % 2 == 1:
        criterion = "Максимальная производительность"
        formula = "max(λ′)"
        if sys1['lam_eff_total'] > sys2['lam_eff_total']:
            best = "СИСТЕМА 1"
            diff_percent = ((sys1['lam_eff_total'] - sys2['lam_eff_total']) / sys2['lam_eff_total']) * 100
            values = f"({sys1['lam_eff_total']:.4f} > {sys2['lam_eff_total']:.4f}, +{diff_percent:.1f}%)"
        else:
            best = "СИСТЕМА 2"
            diff_percent = ((sys2['lam_eff_total'] - sys1['lam_eff_total']) / sys1['lam_eff_total']) * 100
            values = f"({sys2['lam_eff_total']:.4f} > {sys1['lam_eff_total']:.4f}, +{diff_percent:.1f}%)"
    else:
        criterion = "Минимальные потери заявок"
        formula = "min(π)"
        if sys1['p_loss_total'] < sys2['p_loss_total']:
            best = "СИСТЕМА 1"
            diff_percent = ((sys2['p_loss_total'] - sys1['p_loss_total']) / sys1['p_loss_total']) * 100
            values = f"({sys1['p_loss_total']:.4f} < {sys2['p_loss_total']:.4f}, +{diff_percent:.1f}%)"
        else:
            best = "СИСТЕМА 2"
            diff_percent = ((sys1['p_loss_total'] - sys2['p_loss_total']) / sys2['p_loss_total']) * 100
            values = f"({sys2['p_loss_total']:.4f} < {sys1['p_loss_total']:.4f}, +{diff_percent:.1f}%)"

    print(f"\nКритерий: {criterion}")
    print(f"Формула выбора: {formula}")
    print(f"Лучшая система: {best} {values}")

    # Обоснование выбора
    print("\n" + "=" * 70)
    print("ОБОСНОВАНИЕ ВЫБОРА:")
    print("=" * 70)

    if best == "СИСТЕМА 1":
        print("Система 1 выбрана как лучшая, потому что:")
        if criterion == "Максимальная производительность":
            print(
                f"- Имеет более высокую производительность: {sys1['lam_eff_total']:.4f} против {sys2['lam_eff_total']:.4f}")
            print(f"- Обрабатывает на {diff_percent:.1f}% больше заявок в единицу времени")
        else:
            print(f"- Имеет меньшую вероятность потерь: {sys1['p_loss_total']:.4f} против {sys2['p_loss_total']:.4f}")
            print(f"- Теряет на {diff_percent:.1f}% меньше заявок")
    else:
        print("Система 2 выбрана как лучшая, потому что:")
        if criterion == "Максимальная производительность":
            print(
                f"- Имеет более высокую производительность: {sys2['lam_eff_total']:.4f} против {sys1['lam_eff_total']:.4f}")
            print(f"- Обрабатывает на {diff_percent:.1f}% больше заявок в единицу времени")
        else:
            print(f"- Имеет меньшую вероятность потерь: {sys2['p_loss_total']:.4f} против {sys1['p_loss_total']:.4f}")
            print(f"- Теряет на {diff_percent:.1f}% меньше заявок")

    # Создаем график сравнения
    print("\n" + "=" * 70)
    print("ГРАФИК СРАВНЕНИЯ:")
    print("=" * 70)
    print("Создается график сравнения характеристик...")

    create_comparison_chart(sys1, sys2)

    print("\nГрафик сохранен как 'comparison_chart.png'")


if __name__ == "__main__":
    compare_systems()