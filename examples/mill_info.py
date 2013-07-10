"""
Information of Single Windmill
-------------------------------------------------------------------------
"""

import matplotlib.pyplot as plt
import numpy as np
import windml.util.features

from windml.datasets.nrel import NREL
from windml.visualization.show_coord_topo_mill import show_coord_topo_mill

ds = NREL()
windmill = ds.get_windmill(NREL.park_id['tehachapi'], 2004)

feat, month_power, ramps_up, ramps_down, power_freq = windml.util.features.compute_highlevel_features(windmill)

month = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
figure = plt.figure(figsize=(15, 10))

# plot 1
plot1 = plt.subplot(2, 2, 1)
plt.title("Windmill Location")
show_coord_topo_mill(windmill, show = False)

# plot 2
plot2 = plt.subplot(2, 2, 2)
plt.title("Power Statistics")
plot2.bar(range(1,13), month_power, color='grey')
plot2.set_ylabel('Power', color='black')
plot2.set_xlabel('Month', color='black')
plot2.set_xticks([i+0.5 for i in range(1,13)])
plot2.set_xticklabels(month)

# plot 3
length = 2*len(windml.util.features.rampheights)+1
plot3 = plt.subplot(2, 2, 3)
plt.title("Ramp Statistics")
plot3.bar(range(1,length), ramps_up+ramps_down, color='orange')
plot3.set_ylabel('# of Ramps', color='black')
plot3.set_xticks([i+0.5 for i in range(1,length)])
plot3.set_xticklabels(['up '+str(i) for i in windml.util.features.rampheights]+['dwn '+str(i) for i in windml.util.features.rampheights])

# plot 4
plot4 = plt.subplot(2, 2, 4)
help = [i*windml.util.features.interval_width for i in range(1,30/windml.util.features.interval_width+1)]
labels = [str(i-windml.util.features.interval_width)+"-"+str(i) for i in help]
plot4.pie(power_freq, labels = labels, shadow=True)

plt.title("Stability Statistics")
plt.show()
