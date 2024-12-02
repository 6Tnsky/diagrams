import numpy as np
import matplotlib.pyplot as plt

# Генерация двух наборов случайных данных
num_points = 100  # Количество точек
x = np.random.rand(num_points)  # Случайные значения для оси X (от 0 до 1)
y = np.random.rand(num_points)  # Случайные значения для оси Y (от 0 до 1)

# Построение диаграммы рассеяния
plt.scatter(x, y, color='blue', alpha=0.7, edgecolor='black')

# Настройка графика
plt.title('Диаграмма рассеяния случайных данных')
plt.xlabel('Значения X')
plt.ylabel('Значения Y')

# Отображение графика
plt.show()