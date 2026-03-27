import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Симулятор коробки передач", layout="wide")
st.title("🚗 Симулятор влияния передаточных чисел на разгон и максимальную скорость")

st.markdown("Вводи параметры автомобиля и смотри, как меняются графики в реальном времени.")

# ====================== Боковая панель для ввода ======================
with st.sidebar:
    st.header("Параметры двигателя")
    power_kw = st.slider("Мощность двигателя (кВт)", 50, 500, 150)
    torque_nm = st.slider("Крутящий момент (Нм)", 100, 600, 300)
    max_rpm = st.slider("Максимальные обороты (об/мин)", 4000, 9000, 7000)

    st.header("Параметры автомобиля")
    mass_kg = st.slider("Масса автомобиля (кг)", 800, 3000, 1400, step=50)
    wheel_radius = st.slider("Радиус колеса (м)", 0.25, 0.40, 0.32, step=0.01)
    final_drive = st.slider("Главная передача", 2.5, 5.0, 3.5, step=0.1)

    st.header("Передаточные числа")
    gear_ratios = []
    default_ratios = [4.2, 2.8, 1.9, 1.4, 1.1, 0.9]
    
    for i in range(6):
        ratio = st.number_input(f"{i+1} передача", 
                               value=default_ratios[i], 
                               min_value=0.5, 
                               max_value=6.0, 
                               step=0.05, 
                               format="%.2f")
        gear_ratios.append(ratio)

# ====================== Расчёты ======================
results = []
max_speeds = []
accels = []
colors = plt.cm.tab10(np.linspace(0, 1, 6))

fig1, ax1 = plt.subplots(figsize=(8, 5))
fig2, ax2 = plt.subplots(figsize=(6, 4))
fig3, ax3 = plt.subplots(figsize=(6, 4))

for i, ratio in enumerate(gear_ratios):
    total_ratio = ratio * final_drive
    
    # Максимальная скорость на передаче (км/ч)
    v_ms = (max_rpm * 2 * np.pi * wheel_radius) / (60 * total_ratio)
    v_kmh = v_ms * 3.6
    max_speeds.append(v_kmh)
    
    # Ускорение (м/с²)
    force = (torque_nm * total_ratio) / wheel_radius
    accel = force / mass_kg
    accels.append(accel)
    
    # График обороты vs скорость
    speeds = np.linspace(0, v_kmh * 1.05, 200)
    rpms = (speeds / 3.6 * total_ratio * 60) / (2 * np.pi * wheel_radius)
    ax1.plot(speeds, rpms, label=f"{i+1} пер. ({ratio:.2f})", color=colors[i])
    
    results.append({
        "Передача": i+1,
        "Передаточное число": round(ratio, 2),
        "Макс. скорость (км/ч)": round(v_kmh, 1),
        "Ускорение (м/с²)": round(accel, 2)
    })

# Оформление графиков
ax1.set_xlabel("Скорость (км/ч)")
ax1.set_ylabel("Обороты (об/мин)")
ax1.set_title("Обороты двигателя на разных передачах")
ax1.axhline(max_rpm, color='red', linestyle='--', label='Красная зона')
ax1.grid(True)
ax1.legend()

ax2.bar([f"{i+1}" for i in range(6)], max_speeds, color=colors)
ax2.set_xlabel("Передача")
ax2.set_ylabel("Макс. скорость (км/ч)")
ax2.set_title("Максимальная скорость на передаче")
ax2.grid(axis='y')

ax3.bar([f"{i+1}" for i in range(6)], accels, color=colors)
ax3.set_xlabel("Передача")
ax3.set_ylabel("Ускорение (м/с²)")
ax3.set_title("Ускорение на передаче")
ax3.grid(axis='y')

# ====================== Вывод на экран ======================
col1, col2 = st.columns([2, 1])

with col1:
    st.pyplot(fig1)

with col2:
    st.pyplot(fig2)
    st.pyplot(fig3)

st.subheader("Результаты расчёта")
st.dataframe(results, use_container_width=True, hide_index=True)

st.caption("Приложение пересчитывает всё автоматически при изменении любого параметра.")
