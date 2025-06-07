import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Параметры цилиндров
diameter = 150  # диаметр горизонтального цилиндра (мм)
radius = diameter / 2  # радиус горизонтального цилиндра (мм)
height = 300  # высота цилиндра (мм)
R_vertical = 75  # радиус вертикального цилиндра (принимаем такой же)

# Создаем фигуру
fig, ax = plt.subplots(figsize=(10, 8))

# 1. Развертка горизонтального цилиндра (прямоугольник)
cylinder_circumference = np.pi * diameter  # Правильная формула: πD
rect = Rectangle((0, -height/2), cylinder_circumference, height,
                 linewidth=1, edgecolor='blue', facecolor='none', linestyle='--')
ax.add_patch(rect)

# 2. Вычисляем кривую пересечения (только входящая часть)
theta = np.linspace(0, 2*np.pi, 24)
x_curve = radius * theta  # Используем радиус для параметризации
y_curve = np.sqrt(R_vertical**2 - radius**2 * np.cos(theta)**2)



# Фильтруем только действительные значения
valid_mask = ~np.isnan(y_curve)
x_curve = x_curve[valid_mask]
y_curve = y_curve[valid_mask]

# Центрируем вырез по высоте
y_curve_centered = y_curve - y_curve.mean()

# Строим кривую выреза
ax.plot(x_curve, y_curve_centered, 'r-', linewidth=2)

for i, x in enumerate(y_curve):
    print(f"{i+1}: {x}")

# 3. Добавляем вспомогательные линии
ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
for fold in [0, cylinder_circumference/2, cylinder_circumference]:
    ax.axvline(x=fold, color='black', linestyle=':', alpha=0.5)

# 4. Настройка графика
ax.set_xlim(-10, cylinder_circumference + 10)
ax.set_ylim(-height/2-10, height/2+10)
ax.set_aspect('equal')
ax.grid(True, linestyle='--', alpha=0.5)
ax.set_title(f'Шаблон развертки цилиндра (D={diameter}мм, H={height}мм)\nс центральным вырезом', pad=20)
ax.set_xlabel(f'Длина развертки: {cylinder_circumference:.1f} мм')
ax.set_ylabel('Высота (мм)')

# 5. Добавляем параметры
param_text = (f'Параметры:\n'
              f'Диаметр цилиндра = {diameter} мм\n'
              f'Радиус вертикального цилиндра = {R_vertical} мм\n'
              f'Высота цилиндров = {height} мм\n'
              f'Длина развертки = π×D = {cylinder_circumference:.1f} мм')
ax.text(0.02, 0.98, param_text, transform=ax.transAxes,
        verticalalignment='top', bbox=dict(facecolor='white', alpha=0.8))

plt.tight_layout()
plt.savefig('cylinder_template_correct.png', dpi=300, bbox_inches='tight')
plt.show()