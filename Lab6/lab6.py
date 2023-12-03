import numpy as np
import matplotlib.pyplot as plt

# Завдання 1 (2б):
# 1. Згенеруйте двовимірні дані (x, y) за допомогою numpy.random : бажано, щоб розподіл
# точок був навколо деякої наперед заданої прямої (y = k*x + b) для подальшого аналізу
# результатів.
# 2. Напишіть функцію, яка реалізує метод найменших квадратів для пошуку оптимальних
# оцінок kk� та bb�.
# 3. Порівняйте знайдені параметри з оцінкою np.polyfit(x,y,1) (оцінка полінома
# степеню 1 методом найменших квадратів), та з початковими параметрами прямої (якщо
# такі є).
# 4. Відобразіть на графіку знайдені оцінки лінії регресії (вашої та numpy). Якщо ви
# генерували вхідні дані навколо лінії, відобразіть також її.

# Завдання 2 (2б):
# 1. Напишіть функцію, яка реалізує метод градієнтного спуску для пошуку оптимальних
# оцінок kk� та bb�. Визначіть оптимальні вхідні параметри: learning_rate, n_iter
# 2. Додайте отриману лінію регресії на загальний графік
# 3. Побудуйте графік похибки від кількості ітерацій, зробіть висновки
# 4. Порівняйте отримані результати з результатами попереднього завдання

# Корисні посилання
# 1. https://uk.wikipedia.org/wiki/Проста_лінійна_регресія
# 2. https://uk.wikipedia.org/wiki/Градієнтний_спуск
# 3. https://numpy.org/doc/stable/reference/generated/numpy.polyfit.html
# 4. https://numpy.org/doc/stable/reference/arrays.html
# 5. McKinney Wes. 2012. Python for data analysis (1st. ed.). O'Reilly Media, Inc.
k_s = 2.5
b_s = 10
n = 1000
x = np.linspace(0, 1000, n)
y = k_s*x + b_s + np.random.normal(0, 100, x.shape[0])

def least_squares(x, y):
    k, b, sum_up, sum_down = 0, 0, 0, 0
    
    for i in range(x.shape[0]):
        sum_up += (x[i]-x.mean())*(y[i]-y.mean())
    for j in range(x.shape[0]):
        sum_down += (x[j]-x.mean())**2
    k = sum_up/sum_down
    b = y.mean() - k*x.mean()
    return k, b

print(f"Початкові параметри: k = {k_s}, b = {b_s}")

# Знайдемо оцінки параметрів
ks, bs = least_squares(x, y)
print(f"Оцінка методом найменших квадратів: k = {ks}, b = {bs}")

# Порівняння з np.polyfit
polyfit_k, polyfit_b = np.polyfit(x, y, 1)
print(f"Оцінка за допомогою np.polyfit: k = {polyfit_k}, b = {polyfit_b}")


plt.scatter(x, y, label='Згенеровані дані')
plt.plot(x, k_s * x + b_s, color='red', label='Справжня пряма')
plt.plot(x, ks * x + bs, color='green', label='Оцінка методом найменших квадратів')
plt.plot(x, polyfit_k * x + polyfit_b, color='purple', label='Оцінка за допомогою np.polyfit')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()

"""
def gradient_descent(x, y, learning_rate=0.01, n_iter=1000):
    k, b = 0, 0
    m = len(x)

    for _ in range(n_iter):
        y_pred = k * x + b
        error = y_pred - y
        k -= (2 / m) * learning_rate * np.dot(error, x)
        b -= (2 / m) * learning_rate * np.sum(error)

    return k, b

# Знайдемо оцінки параметрів за допомогою градієнтного спуску
gd_k, gd_b = gradient_descent(x, y)
print(f"Оцінка методом градієнтного спуску: k = {gd_k}, b = {gd_b}")


plt.scatter(x, y, label='Згенеровані дані')
plt.plot(x, k_s * x + b_s, color='red', label='Справжня пряма')
plt.plot(x, estimated_k * x + estimated_b, color='green', label='Оцінка методом найменших квадратів')
plt.plot(x, polyfit_k * x + polyfit_b, color='purple', label='Оцінка за допомогою np.polyfit')
plt.plot(x, gd_k * x + gd_b, color='orange', label='Оцінка методом градієнтного спуску')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()


def compute_cost(x, y, k, b):
    return np.mean((k * x + b - y) ** 2)

def gradient_descent_with_cost(x, y, learning_rate=0.01, n_iter=1000):
    k, b = 0, 0
    m = len(x)
    costs = []

    for _ in range(n_iter):
        y_pred = k * x + b
        error = y_pred - y
        k -= (2 / m) * learning_rate * np.dot(error, x)
        b -= (2 / m) * learning_rate * np.sum(error)
        cost = compute_cost(x, y, k, b)
        costs.append(cost)

    return k, b, costs

# Знайдемо оцінки параметрів та графік похибки
gd_k, gd_b, costs = gradient_descent_with_cost(x, y)

# Відображення графіка похибки
plt.plot(range(1, n + 1), costs, marker='o')
plt.xlabel('Кількість ітерацій')
plt.ylabel('Похибка')
plt.title('Графік похибки від кількості ітерацій')
plt.show()
"""