import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Custom class for animations.
# Generalised from matplotlib docs example
# https://matplotlib.org/gallery/animation/animate_decay.html

class Animator(object):

    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], lw=2)
        self.ax.grid()
        self.xdata, self.ydata = [], []
        self.xrange_0 = (0,10)
        self.yrange_0 = (-1.1,1.1)
        self.init_axes()
        self.yscale = 'linear'
        
    def init_axes(self):
        self.ax.set_ylim(self.yrange_0)
        self.ax.set_xlim(self.xrange_0)
        del self.xdata[:]
        del self.ydata[:]
        self.line.set_data(self.xdata, self.ydata)
        return self.line,
        
    def data_gen(self,t=0):
        cnt = 0
        while cnt < 1000:
            cnt += 1
            t += 0.1
            yield t, np.sin(2*np.pi*t) * np.exp(-t/10.)

    def run(self, data):
        # update the data
        t, y = data
        self.xdata.append(t)
        self.ydata.append(y)
        self.xmin, self.xmax = self.ax.get_xlim()
        self.ymin, self.ymax = self.ax.get_ylim()

        if t >= self.xmax:
            self.ax.set_xlim(self.xmin, 1.2*self.xmax)
            self.ax.figure.canvas.draw()
        if min(self.ydata) <= self.ymin:
            self.ax.set_ylim(self.ymin/10, self.ymax)
            self.ax.figure.canvas.draw()

        self.line.set_data(self.xdata, self.ydata)
        self.ax.set_yscale(self.yscale)

        return self.line,

    def animate(self):
        ani = animation.FuncAnimation(self.fig,
            self.run, self.data_gen, blit=False, interval=10,
            repeat=False, init_func=self.init_axes)
        plt.show()
        
