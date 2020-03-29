#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np


class Data:

    def __init__(self):
        self.transmission_rate = 1 / 2
        self.recovery_rate = 1 / 14
        self.number_of_days = 30
        self.population = 1000000.0
        self.hospital_capacity = 20000
        self.hospital_ration = self.hospital_capacity / self.population

    def ds_dt(self, s, i):
        return - self.transmission_rate * s * i

    def di_dt(self, s, i):
        return self.transmission_rate * s * i - self.recovery_rate * i

    def dr_dt(self, s, i):
        return self.recovery_rate * i

    def compute(self):
        infected_start = 0.01
        susceptible_start = 1.0 - infected_start
        recovered_start = 0.0

        dt = 1 / 24
        t = np.arange(0, self.number_of_days, dt)
        print(t.size)
        s = np.zeros(t.size) + susceptible_start
        i = np.zeros(t.size) + infected_start
        r = np.zeros(t.size) + recovered_start

        for index in range(1, t.size):
            s[index] = s[index - 1] + self.ds_dt(s[index - 1], i[index - 1]) * dt
            i[index] = i[index - 1] + self.di_dt(s[index - 1], i[index - 1]) * dt
            r[index] = r[index - 1] + self.dr_dt(s[index - 1], i[index - 1]) * dt

        self.plot(s, i, r, t)

    def plot(self, s, i, r, t):
        fig = plt.figure(figsize=(6, 10))

        ax3 = fig.add_subplot(313)
        ax3.plot(t, s * self.population, label='Susceptible')
        ax3.plot(t, i * self.population, 'b--', label='Infected')
        ax3.plot(t, r * self.population, 'r--', label='Recovered')
        ax3.set(xlabel='time (days)',
                ylabel='')
        ax3.legend()
        ax3.grid()

        fig.savefig("test.png")
        plt.show()


if __name__ == '__main__':
    data = Data()
    data.compute()
