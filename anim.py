'''
 Custom class for animations.
 Generalised from matplotlib docs example
 https://matplotlib.org/gallery/animation/animate_decay.html
'''
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class Animator(object):
    '''
       A python class which holds an animator. The animator
       is capable of updating a matplotlib plot in realtime
       as a python program is running.
       Generalised from matplotlib docs example
       https://matplotlib.org/gallery/animation/animate_decay.html
    '''
    # pylint: disable=too-many-instance-attributes

    def __init__(self, plot_best=None, swarm=None):
        self.plot_best = plot_best
        self.swarm = swarm
        if plot_best:
            self.fig, self.axes = plt.subplots(1,2)
            self.fig.set_size_inches(12,6)
            self.axis = self.axes[0]
            self.axis2 = self.axes[1]
            plot_best(swarm.best[0], self.axis2)
        else:
            self.fig, self.axis = plt.subplots()
        self.line, = self.axis.plot([], [], lw=2)
        self.axis.grid()
        self.xdata, self.ydata = [], []
        self.xrange_0 = (0, 10)
        self.yrange_0 = (-1.1, 1.1)
        self.init_axes()
        self.yscale = 'linear'
        self.xmin, self.xmax = self.axis.get_xlim()
        self.ymin, self.ymax = self.axis.get_ylim()

    def init_axes(self):
        '''Initiates the plot axes'''

        self.axis.set_ylim(self.yrange_0)
        self.axis.set_xlim(self.xrange_0)
        del self.xdata[:]
        del self.ydata[:]
        self.line.set_data(self.xdata, self.ydata)
        return self.line,

    def run(self, data):
        '''updates the plot data'''
        t, y = data
        self.xdata.append(t)
        self.ydata.append(y)
        self.xmin, self.xmax = self.axis.get_xlim()
        self.ymin, self.ymax = self.axis.get_ylim()

        if t >= self.xmax:
            self.axis.set_xlim(self.xmin, 1.2*self.xmax)
            self.axis.figure.canvas.draw()
        if min(self.ydata) <= self.ymin:
            self.axis.set_ylim(self.ymin/10, self.ymax)
            self.axis.figure.canvas.draw()

        self.line.set_data(self.xdata, self.ydata)
        self.axis.set_yscale(self.yscale)
        if self.plot_best:
            self.axis2.clear()
            self.plot_best(self.swarm.best[0], self.axis2)

        return self.line,

    def animate(self, data_gen):
        '''Plots and shows the animation'''
        ani = animation.FuncAnimation(self.fig, self.run,
                                      data_gen, blit=False,
                                      interval=10, repeat=False,
                                      init_func=self.init_axes)
        plt.show(ani)

def test():
    '''
       Test function. Run anim.test() to ensure anim.py
       is able to produce an animation.
    '''
    test_anim = Animator()
    test_anim.animate(test_data_gen)

def test_data_gen(t=0):
    '''generates data for a test function'''
    cnt = 0
    while cnt < 1000:
        cnt += 1
        t += 0.1
        yield t, np.sin(2*np.pi*t) * np.exp(-t/10.)
