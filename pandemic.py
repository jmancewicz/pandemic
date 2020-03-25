#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

PercentSick = 0.5
PercentHospitalized = 0.2
iMinHospitalStay = 12
MaxHospital = 20.0

L = 10000.0 * PercentSick
Tau = 28.0
K = 1.0 / Tau

threshold = 10

offset = 365

days = np.arange(-offset,offset,1)

e = np.exp(-K*days)
ope = 1.0 + e

TotalSick = L / ope
SickPerDay = L * K * e / ope**2

PeopleInHospital = np.zeros(offset*2)

i = 0
for iDay in days:
    PeopleIn = SickPerDay[i] * PercentHospitalized
    PeopleOut = 0
    
    if (i > iMinHospitalStay):
        PeopleOut = SickPerDay[i-iMinHospitalStay] * PercentHospitalized

    PeopleInHospital[i] = PeopleInHospital[i-1] + PeopleIn - PeopleOut
    i=i+1

l = TotalSick < threshold 

Day1 = np.max(days[l])

ShelterDays = -2*Day1

x1 = [Day1 + offset,Day1 + offset]
x2 = [-Day1 + offset, -Day1 + offset]

title = 'Days to Shelter = '+str(ShelterDays)+' (Threshold = '+str(threshold*1000)+' people)'

fig = plt.figure(figsize=(6,10))

shift = offset+Day1

ax = fig.add_subplot(311)
ax.plot(days+offset-shift,TotalSick)
y = [0,L]
#ax.plot(x1-shift,y,'b--')
#ax.plot(x2-shift,y,'b--')
ax.set(xlabel='time (days)',
       ylabel='Number of Sick (1,000 people)',
       title=title, xlim=[0,ShelterDays])
ax.grid()

ax2 = fig.add_subplot(312)
ax2.plot(days+offset-shift,SickPerDay)
y = [0,np.max(SickPerDay)]
#ax2.plot(x1-shift,y,'b--')
#ax2.plot(x2-shift,y,'b--')
ax2.set(xlabel='time (days)', ylabel='Sick Per Day (1,000 people)',xlim=[0,ShelterDays])
ax2.grid()

ax3 = fig.add_subplot(313)
ax3.plot(days+offset-shift,PeopleInHospital, label = 'People')
ax3.plot(days+offset-shift,PeopleInHospital*0.0 + MaxHospital, 'b--', label = 'Hosp. Cap.')
ax3.plot(days+offset-shift,PeopleInHospital*0.0 + 2*MaxHospital, 'r--', label = '2x Hosp. Cap.')
y = [0,np.max(PeopleInHospital)]
#ax3.plot(x1-shift,y,'b--')
#ax3.plot(x2-shift,y,'b--')
ax3.set(xlabel='time (days)', ylabel='People In Hosp. (1,000 people)',xlim=[0,ShelterDays])
ax3.legend()
ax3.grid()

fig.savefig("test.png")
