#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np


class Data:
    threshold = 10
    max_hospital = 20.0
    offset = 365
    percent_sick = 0.5
    percent_hospitalized = 0.2
    min_hospital_stay = 12

    def __init__(self):
        self.shelter_days = None
        self.days = np.arange(-Data.offset, Data.offset, 1)
        self.day1 = None
        self.total_sick = None
        self.people_in_hospital = np.zeros(self.days.size)
        self.sick_per_day = None

    def compute(self):

        sick = 10000.0 * Data.percent_sick
        tau = 28.0

        e = np.exp(-self.days / tau)
        ope = 1.0 + e

        self.total_sick = sick / ope
        self.sick_per_day = sick / tau * e / ope ** 2

        for i in range(len(self.days)):
            people_in = self.sick_per_day[i] * Data.percent_hospitalized
            people_out = 0

            if i > Data.min_hospital_stay:
                people_out = self.sick_per_day[i - Data.min_hospital_stay] * \
                             Data.percent_hospitalized

            self.people_in_hospital[i] = self.people_in_hospital[i - 1] + people_in - people_out

        less_than = self.total_sick < Data.threshold

        self.day1 = np.max(self.days[less_than])

        self.shelter_days = -2 * self.day1

    def plot(self):
        title = 'Days to Shelter = ' + str(self.shelter_days) + ' (Threshold = ' + str(
            Data.threshold * 1000) + ' people)'

        fig = plt.figure(figsize=(6, 10))

        shift = Data.offset + self.day1

        ax = fig.add_subplot(311)
        ax.plot(self.days + Data.offset - shift,
                self.total_sick)
        ax.set(xlabel='time (days)',
               ylabel='Number of Sick (1,000 people)',
               title=title,
               xlim=[0, self.shelter_days])
        ax.grid()

        ax2 = fig.add_subplot(312)
        ax2.plot(self.days + Data.offset - shift,
                 self.sick_per_day)
        ax2.set(xlabel='time (days)',
                ylabel='Sick Per Day (1,000 people)',
                xlim=[0, self.shelter_days])
        ax2.grid()

        ax3 = fig.add_subplot(313)
        ax3.plot(self.days + Data.offset - shift,
                 self.people_in_hospital,
                 label='People')
        ax3.plot(self.days + Data.offset - shift,
                 np.zeros(len(self.days)) + Data.max_hospital,
                 'b--',
                 label='Hosp. Cap.')
        ax3.plot(self.days + Data.offset - shift,
                 np.zeros(len(self.days)) + 2 * Data.max_hospital,
                 'r--',
                 label='2x Hosp. Cap.')
        ax3.set(xlabel='time (days)',
                ylabel='People In Hosp. (1,000 people)',
                xlim=[0, self.shelter_days])
        ax3.legend()
        ax3.grid()

        fig.savefig("test.png")
        plt.show()


if __name__ == '__main__':
    data = Data()
    data.compute()
    data.plot()
