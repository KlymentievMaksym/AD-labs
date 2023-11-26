# Постановка задачі:
# Створіть програму, яка дозволить користувачам малювати графік функції гармоніки (функція виду y(t) = A ∗ sin(ω ∗ t + φ)) з накладеним шумом та надавати можливість змінювати параметри гармоніки та шуму за допомогою інтерактивного інтерфейсу, що включає в себе слайдери, кнопки та чекбокси. Зашумлену гармоніку відфільтруйте за допомогою фільтру на вибір, порівняйте результат.

# # 1. Створіть програму, яка використовує бібліотеки Matplotlib для створення графічного інтерфейсу.
# # 2. Реалізуйте функцію harmonic_with_noise, яка приймає наступні параметри:
# # amplitude - амплітуда гармоніки.
# # frequency - частота гармоніки.
# # phase – фазовий зсув гаромніки
# # noise_mean - амплітуда шуму.
# # noise_covariance – дисперсія шуму
# # show_noise - флаг, який вказує, чи слід показувати шум на графіку.
# # 3. У програмі має бути створено головне вікно з такими елементами інтерфейсу:
# # Поле для графіку функції (plot)
# # Слайдери (sliders), які відповідають за амплітуду, частоту гармоніки, а також слайдери для параметрів шуму
# # Чекбокс для перемикання відображення шуму на гармоніці
# # Кнопка «Reset», яка відновлює початкові параметри
# # 4. Програма повинна мати початкові значення кожного параметру, а також передавати параметри для відображення оновленого графіку.

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons, Button, Slider

# The parametrized function to be plotted
def f(t, amplitude, frequency, phase): # harmonic
    return amplitude * np.sin(2 * np.pi * frequency * t + phase)

def f1(t, amplitude, frequency, phase): # harmonic_with_noise
    return amplitude * np.sin(4 * np.pi * frequency * t + phase)

t = np.linspace(0, 1, 1000)

# Define initial parameters
init_amplitude = 5
init_frequency = 3
init_phase = 0
init_noise_mean = 0
init_noise_covariance = 0

# Create the figure and the line that we will manipulate
fig, ax = plt.subplots()
line, = ax.plot(t, f(t, init_amplitude, init_frequency, init_phase), lw=2)
line2, = ax.plot(t, f1(t, init_amplitude, init_frequency, init_phase), visible=False, lw=2)
ax.set_xlabel('Time [s]')

# adjust the main plot to make room for the sliders
fig.subplots_adjust(left=0.25, bottom=0.25)

# Make a horizontal slider to control the frequency.
axfreq = fig.add_axes([0.25, 0.1, 0.65, 0.03])
freq_slider = Slider(
    ax=axfreq,
    label='Frequency [Hz]',
    valmin=0.1,
    valmax=30,
    valinit=init_frequency,
)

# Make a horizontal slider to control the phase.
axphas = fig.add_axes([0.25, 0.05, 0.65, 0.03])
phas_slider = Slider(
    ax=axphas,
    label='Phase',
    valmin=0,
    valmax=2*np.pi,
    valinit=init_phase,
)

# Make a vertically oriented slider to control the amplitude
axamp = fig.add_axes([0.1, 0.25, 0.0225, 0.63])
amp_slider = Slider(
    ax=axamp,
    label="Amplitude",
    valmin=0,
    valmax=10,
    valinit=init_amplitude,
    orientation="vertical"
)

rax = fig.add_axes([0.40, 0.89, 0.35, 0.12])
check = CheckButtons(rax, ('Harmonic', 'Harmonic via noise'), (True, False))

# The function to be called anytime a slider's value changes
def update(val):
    line.set_ydata(f(t, amp_slider.val, freq_slider.val, phas_slider.val))
    line2.set_ydata(f1(t, amp_slider.val, freq_slider.val, phas_slider.val))
    fig.canvas.draw_idle()


def func(label):
    if label == 'Harmonic':
        line.set_visible(not line.get_visible())
    elif label == 'Harmonic via noise':
        line2.set_visible(not line2.get_visible())
    plt.draw()

# register the update function with each slider
check.on_clicked(func)
freq_slider.on_changed(update)
amp_slider.on_changed(update)
phas_slider.on_changed(update)

# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
resetax = fig.add_axes([0.8, 0.005, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor='0.975')


def reset(event):
    freq_slider.reset()
    amp_slider.reset()
    phas_slider.reset()
button.on_clicked(reset)

plt.show()


# Завдання 1

# 5. Через чекбокс користувач може вмикати або вимикати відображення шуму на графіку. Якщо прапорець прибрано – відображати «чисту гармоніку», якщо ні – зашумлену.
# 6. Після оновлення параметрів програма повинна одразу оновлювати графік функції гармоніки з накладеним шумом згідно з виставленими параметрами.
# Зауваження: якщо ви змінили параметри гармоніки, але не змінювали параметри шуму, то шум має залишитись таким як і був, а не генеруватись наново. Якщо ви змінили параметри шуму, змінюватись має лише шум – параметри гармоніки мають залишатись незмінними.
# 7. Після натискання кнопки «Reset», мають відновитись початкові параметри
# 8. Залиште коментарі та інструкції для користувача, які пояснюють, як користуватися програмою.
# 9. Завантажте файл зі скриптом до вашого репозиторію на GitHub
# 10. Надайте короткий звіт про ваш досвід та вивчені навички.
# Завдання 2
# 1. Отриману гармоніку з накладеним на неї шумом відфільтруйте за допомогою фільтру на ваш вибір (наприклад scipy.signal.iirfilter, повний список за посиланням: https://docs.scipy.org/doc/scipy/reference/signal.html). Відфільтрована гармоніка має бути максимально близька до «чистої»
# 2. Відобразіть відфільтровану «чисту» гармоніку поряд з початковою
# 3. Додайте відповідні інтерактивні елементи (чекбокс показу, параметри фільтру тощо) та оновіть існуючі: відфільтрована гармоніка має оновлюватись разом з початковою.
# Завдання 3
# 1. Реалізуйте завдання 1 за допомогою сучасних графічних бібліотек на ваш вибір: Plotly, Bokeh, Altair тощо. Додайте декілька вікон для візуалізації замість одного, спадне меню (drop-down menu) та інші інтерактивні елементи на власний розсуд.
# 2. Реалізуйте ваш власний фільтр, використовуючи виключно Python (а також numpy, але виключно для операцій з масивами numpy.ndarray). Застосуйте фільтр
# Корисні посилання
# https://matplotlib.org/stable/gallery/widgets/index.html
# https://docs.scipy.org/doc/scipy/reference/signal.html
# https://plotly.com/python/#controls
# https://docs.bokeh.org/en/latest/docs/user_guide/interaction/widgets.html
# https://altair-viz.github.io/user_guide/interactions.html
