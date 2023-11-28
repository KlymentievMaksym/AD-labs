# Постановка задачі:
# Створіть програму, яка дозволить користувачам малювати графік функції гармоніки (функція виду y(t) = A ∗ sin(ω ∗ t + φ)) з накладеним шумом та надавати можливість змінювати параметри гармоніки та шуму за допомогою інтерактивного інтерфейсу, що включає в себе слайдери, кнопки та чекбокси. Зашумлену гармоніку відфільтруйте за допомогою фільтру на вибір, порівняйте результат.

# Завдання 1
# 1. Створіть програму, яка використовує бібліотеки Matplotlib для створення графічного інтерфейсу.
# 2. Реалізуйте функцію harmonic_with_noise, яка приймає наступні параметри:
# # amplitude - амплітуда гармоніки.
# # frequency - частота гармоніки.
# # phase – фазовий зсув гаромніки
# # noise_mean - амплітуда шуму.
# # noise_covariance – дисперсія шуму
# # show_noise - флаг, який вказує, чи слід показувати шум на графіку.
# 3. У програмі має бути створено головне вікно з такими елементами інтерфейсу:
# # Поле для графіку функції (plot)
# # Слайдери (sliders), які відповідають за амплітуду, частоту гармоніки, а також слайдери для параметрів шуму
# # Чекбокс для перемикання відображення шуму на гармоніці
# # Кнопка «Reset», яка відновлює початкові параметри
# 4. Програма повинна мати початкові значення кожного параметру, а також передавати параметри для відображення оновленого графіку.
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

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons, Button, Slider
from scipy import signal

# The parametrized function to be plotted
def f(t, amplitude, frequency, phase): # harmonic
    return amplitude * np.sin(2 * np.pi * frequency * t + phase)

def f1(t, amplitude, frequency, phase, noise_mean, noise_covariance): # harmonic_with_noise
    noise = np.random.uniform(noise_mean, noise_covariance, len(t))
    return amplitude * np.sin(2 * np.pi * frequency * t + phase) + noise

t = np.linspace(0, 1, 1000)

# Define initial parameters
init_amplitude = 5
init_frequency = 3
init_phase = 0
init_noise_mean = 0
init_noise_covariance = 0
init_filter = 0.03

# Create the figure and the line that we will manipulate
fig, (ax0, ax1) = plt.subplots(1, 2)

line, = ax0.plot(t, f(t, init_amplitude, init_frequency, init_phase), lw=2)

line2, = ax0.plot(t, f1(t, init_amplitude, init_frequency, init_phase, init_noise_mean, init_noise_covariance), visible=False, lw=2)

# b, a = signal.iirfilter(3, 0.5, btype='low')
b, a = signal.butter(4, init_filter, btype='low')#, analog=False)

filtered_harmonic = signal.lfilter(b, a, f1(t, init_amplitude, init_frequency, init_phase, init_noise_mean, init_noise_covariance))
line3, = ax1.plot(t, filtered_harmonic, visible=False, lw=2)

ax0.set_xlabel('Time [s]')
ax0.set_title('Harmonic')
ax1.set_title('Filtered Harmonic')

# adjust the main plot to make room for the sliders
fig.subplots_adjust(left=0.25, bottom=0.35, top=0.75)

# Make a horizontal oriented slider to control the amplitude
axamp = fig.add_axes([0.25, 0.2, 0.65, 0.03])
amp_slider = Slider(
    ax=axamp,
    label="Amplitude",
    valmin=0,
    valmax=10,
    valinit=init_amplitude,
    #orientation="vertical"
    color='red'
)

# Make a horizontal slider to control the frequency.
axfreq = fig.add_axes([0.25, 0.15, 0.65, 0.03])
freq_slider = Slider(
    ax=axfreq,
    label='Frequency [Hz]',
    valmin=0.1,
    valmax=30,
    valinit=init_frequency,
    color='grey'
)

# Make a horizontal slider to control the phase.
axphas = fig.add_axes([0.25, 0.1, 0.65, 0.03])
phas_slider = Slider(
    ax=axphas,
    label='Phase',
    valmin=0,
    valmax=2*np.pi,
    valinit=init_phase,
    color='purple'
)

# Make a vertically oriented slider to control the Noise mean
nmamp = fig.add_axes([0.15, 0.35, 0.0225, 0.53])
noismean_slider = Slider(
    ax=nmamp,
    label="Mean",
    valmin=-5,
    valmax=5,
    valinit=init_noise_mean,
    orientation="vertical",
    color='#3F51B5'
)

# Make a vertically oriented slider to control the Noise covariance
ncamp = fig.add_axes([0.08, 0.35, 0.0225, 0.53])
noiscovar_slider = Slider(
    ax=ncamp,
    label="Covar",
    valmin=-5,
    valmax=5,
    valinit=init_noise_mean,
    orientation="vertical",
    color='#FF5722'
)

fltamp = fig.add_axes([0.95, 0.35, 0.0225, 0.53])
flt_slider = Slider(
    ax=fltamp,
    label="Filter",
    valmin=0.001,
    valmax=0.1,
    valinit=init_filter,
    orientation="vertical"
)

rax = fig.add_axes([0.40, 0.82, 0.35, 0.12])
check = CheckButtons(rax, ('Harmonic via noise', 'Harmonic filtered'), (False, False))

# The function to be called anytime a slider's value changes
def update(val):
    
    b, a = signal.butter(4, flt_slider.val, btype='low')# , analog=False)
    
    line.set_ydata(f(t, amp_slider.val, freq_slider.val, phas_slider.val))
    
    line2.set_ydata(f1(t, amp_slider.val, freq_slider.val, phas_slider.val, noismean_slider.val, noiscovar_slider.val))
    
    filtered_harmonic = signal.lfilter(b, a, f1(t, amp_slider.val, freq_slider.val, phas_slider.val, noismean_slider.val, noiscovar_slider.val))
    line3.set_ydata(filtered_harmonic)
    
    fig.canvas.draw_idle()


def func(label):
    if label == 'Harmonic via noise':
        line.set_visible(not line.get_visible())
        line2.set_visible(not line2.get_visible())
    elif label == 'Harmonic filtered':
        line3.set_visible(not line3.get_visible())
    plt.draw()

# register the update function with each slider
check.on_clicked(func)
freq_slider.on_changed(update)
amp_slider.on_changed(update)
phas_slider.on_changed(update)
noismean_slider.on_changed(update)
noiscovar_slider.on_changed(update)
flt_slider.on_changed(update)

# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
resetax = fig.add_axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor='0.975')


def reset(event):
    freq_slider.reset()
    amp_slider.reset()
    phas_slider.reset()
    noismean_slider.reset()
    noiscovar_slider.reset()
    flt_slider.reset()
button.on_clicked(reset)

plt.show()

# print(line2.get_ydata().size)


# Завдання 3
# 1. Реалізуйте завдання 1 за допомогою сучасних графічних бібліотек на ваш вибір: Plotly, Bokeh, Altair тощо. Додайте декілька вікон для візуалізації замість одного, спадне меню (drop-down menu) та інші інтерактивні елементи на власний розсуд.
# 2. Реалізуйте ваш власний фільтр, використовуючи виключно Python (а також numpy, але виключно для операцій з масивами numpy.ndarray). Застосуйте фільтр

# Корисні посилання
# https://matplotlib.org/stable/gallery/widgets/index.html
# https://docs.scipy.org/doc/scipy/reference/signal.html
# https://plotly.com/python/#controls
# https://docs.bokeh.org/en/latest/docs/user_guide/interaction/widgets.html
# https://altair-viz.github.io/user_guide/interactions.html
