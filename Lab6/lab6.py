import numpy as np
import matplotlib.pyplot as plt
from numba import njit

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
x = np.linspace(0, 500, n)
y = k_s*x + b_s + np.random.normal(0, 10, x.shape[0])

def least_squares(x, y):
    k, b, sum_up, sum_down = 0, 0, 0, 0
    
    for i in range(x.shape[0]):
        sum_up += (x[i]-x.mean())*(y[i]-y.mean())
        sum_down += (x[i]-x.mean())**2
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

@njit(nogil=True)
def not_in_treshhold(element, treshhold):
    # print(element, treshhold)
    if (abs(element) < treshhold):
        return True
    return False

@njit(nogil=True)
def gradient_descent(x, y, learning_rate_k=0.00000001, learning_rate_b=0.001, treshhold=1e-4, n_iter=150000, epsilon_needed=False, cost_needed=False):
    b = 0
    k = 0
    i = 0
    stop = False
    
    
    while i != n_iter and not stop:
        y0 = b + k*x
        # if i == 0:
        #     epsilon = [b + k*x]
        dLdb = -2 * np.mean(y-y0)
        dLdk = -2 * np.mean(x*(y-y0))
        # print(dLdb, dLdk)
        b = b - learning_rate_b * dLdb
        k = k - learning_rate_k * dLdk
        
        # if epsilon_needed:
        #     epsilon += [np.mean((y0 - y) ** 2)]
        
        stop = not_in_treshhold(dLdk, treshhold)
        if not stop:
            stop = not_in_treshhold(dLdb, treshhold)
        
        i += 1
    # print(i)
    if cost_needed:
        return [k, b, i]
    # elif epsilon_needed:
    #     return [k, b, epsilon]
    else:
        return [k, b]

# Знайдемо оцінки параметрів за допомогою градієнтного спуску
gd_k, gd_b = gradient_descent(x, y, epsilon_needed=False) # , epsilon
print(f"Оцінка методом градієнтного спуску: k = {gd_k}, b = {gd_b}")


@njit(nogil=True)
def search(k_s, b_s, polyfit_k, polyfit_b):
    lrn_rates_to_try = [1e-15, 1e-12, 1e-9, 1e-6, 1e-3, 1e-2]
    n_iters_to_try = [1e6, 1e4, 1e2]
    min_cost = np.inf
    
    for lrn_rate_k in lrn_rates_to_try:
        for lrn_rate_b in lrn_rates_to_try: 
            for n_iter in n_iters_to_try:
                [k1, b1, cost] = gradient_descent(x, y, learning_rate_k=lrn_rate_k, learning_rate_b=lrn_rate_b, n_iter=n_iter, cost_needed=True)
                # print(k1, b1, cost)
                if min_cost >= cost and polyfit_k - 1e-3 < k1 < polyfit_k + 1e-3 and polyfit_b - 1 < b1 < polyfit_b + 1: 
                    min_cost = cost
                    the_best_way = [lrn_rate_k, lrn_rate_b, n_iter, cost]
                    print(k1, b1)
                    print(lrn_rate_k, lrn_rate_b, n_iter, cost, '\n')
    return the_best_way

# the_best_way = search(k_s, b_s, polyfit_k, polyfit_b)                

f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)

ax1.scatter(x, y, label='Згенеровані дані')
ax1.plot(x, k_s * x + b_s, color='red', label='Справжня пряма')
ax1.plot(x, ks * x + bs, color='green', label='Оцінка методом найменших квадратів')
ax1.plot(x, polyfit_k * x + polyfit_b, color='purple', label='Оцінка за допомогою np.polyfit')
ax1.plot(x, gd_k * x + gd_b, color='orange', label='Оцінка методом градієнтного спуску')
# ax2.plot(range(1, n + 1), epsilon, marker='o')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()


# def compute_cost(x, y, k, b):
#     return np.mean((k * x + b - y) ** 2)

# def gradient_descent_with_cost(x, y, learning_rate=0.01, n_iter=1000):
#     k, b = 0, 0
#     m = len(x)
#     costs = []

#     for _ in range(n_iter):
#         y_pred = k * x + b
#         error = y_pred - y
#         k -= (2 / m) * learning_rate * np.dot(error, x)
#         b -= (2 / m) * learning_rate * np.sum(error)
#         cost = compute_cost(x, y, k, b)
#         costs.append(cost)

#     return k, b, costs

# # Знайдемо оцінки параметрів та графік похибки
# gd_k, gd_b, costs = gradient_descent_with_cost(x, y)

# # Відображення графіка похибки
# plt.plot(range(1, n + 1), costs, marker='o')
# plt.xlabel('Кількість ітерацій')
# plt.ylabel('Похибка')
# plt.title('Графік похибки від кількості ітерацій')
# plt.show()
