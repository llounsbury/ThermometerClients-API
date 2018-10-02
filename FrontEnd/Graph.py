import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plot
import matplotlib.animation
import matplotlib.axis
from requests import get

APIURL = 'http://0.0.0.0:5000/'
figure = plot.figure()
axis = figure.add_subplot(1, 1, 1)

temperature_history = []
time_ran = []
runtime = 0


def animate(x):
    global runtime
    try:
        current_temp = float((get(APIURL + 'temp')).text)
    except:
        current_temp = 0
        print("Cannot reach API")
    if current_temp < 10:
        current_temp = 10
    if current_temp > 50:
        current_temp = 50
    print(temperature_history)
    temperature_history.insert(0,current_temp)
    time_ran.append(runtime)
    runtime += 1
    time_ran_plot = time_ran
    temperature_history_plot = temperature_history
    axis.clear()
    axis.plot(time_ran_plot, temperature_history_plot)
    axis.set_xlim(300,0)
    axis.set_ylim(10,50)
    plot.xlabel('seconds ago')
    plot.ylabel('degrees C')

x = matplotlib.animation.FuncAnimation(figure, animate, interval=1000)
plot.show()