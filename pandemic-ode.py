#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np

"""
Plot SIR [susceptible, infected, recovered] and now dead.

Setup your choices in the constructor

The death rates below and above capacity allows you to experiment with those rates in a crude way.

The d{X}_dt set up the differential equations. Change these for your needs.
"""


class PandemicODE:

    def __init__(self):
        self.transmission_rate = 1 / 2
        self.recovery_rate = 1 / 14
        self.number_of_days = 60
        self.population = 1000000.0
        self.hospital_capacity = 200000
        self.hospital_ratio = self.hospital_capacity / self.population
        self.death_rate_below_capacity = 0.02
        self.death_rate_above_capacity = 0.1

    # Conditional on hospital capacity
    def death_rate(self, i):
        return self.death_rate_below_capacity if i < self.hospital_ratio else \
            self.death_rate_above_capacity

    def ds_dt(self, s, i):
        return - self.transmission_rate * s * i

    def di_dt(self, s, i):
        return - self.ds_dt(s, i) - self.dr_dt(s, i) - self.dd_dt(s, i)

    def dr_dt(self, s, i):
        return self.recovery_rate * i

    def dd_dt(self, s, i):
        return self.death_rate(i) * i

    def compute(self):
        infected_start = 0.01
        susceptible_start = 1.0 - infected_start
        recovered_start = 0.0
        dead_start = 0.0

        dt = 1 / 24
        t = np.arange(0, self.number_of_days, dt)
        print(t.size)
        s = np.zeros(t.size) + susceptible_start
        i = np.zeros(t.size) + infected_start
        r = np.zeros(t.size) + recovered_start
        d = np.zeros(t.size) + dead_start

        for index in range(1, t.size):
            s[index] = s[index - 1] + self.ds_dt(s[index - 1], i[index - 1]) * dt
            i[index] = i[index - 1] + self.di_dt(s[index - 1], i[index - 1]) * dt
            r[index] = r[index - 1] + self.dr_dt(s[index - 1], i[index - 1]) * dt
            d[index] = d[index - 1] + self.dd_dt(s[index - 1], i[index - 1]) * dt

        self.plot(s, i, r, t, d)

    def plot(self, s, i, r, t, d):
        fig = plt.figure(figsize=(6, 10))

        print(self.population)
        ax3 = fig.add_subplot(313)
        ax3.plot(t, s * self.population, label='Susceptible')
        ax3.plot(t, i * self.population, 'b', label='Infected')
        ax3.plot(t, r * self.population, 'r', label='Recovered')
        ax3.plot(t, d * self.population, 'black', label='Dead')
        ax3.plot([0, self.number_of_days],
                 [self.hospital_ratio * self.population] * 2, 'g--', label='Capacity')

        ax3.set(xlabel='time (days)',
                ylabel='')
        ax3.legend()
        ax3.grid()

        fig.savefig("test.png")
        plt.show()


if __name__ == '__main__':
    pandemic_ode = PandemicODE()
    pandemic_ode.compute()
