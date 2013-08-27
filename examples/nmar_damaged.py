"""
Damage the Timeseries NMAR
-------------------------------------------------------------------------

This example shows how to artificially damage a time series by uniform
distributed removal of data (NMAR = 'Not Missing At Random').  The percentage of
missing data is given to the preprocessing operator.
"""

from windml.datasets.nrel import NREL
from windml.visualization.plot_timeseries import plot_timeseries
from windml.preprocessing.preprocessing import destroy

# Author: Nils A. Treiber <nils.andre.treiber@uni-oldenburg.de>
# Author: Jendrik Poloczek <jendrik.poloczek@madewithtea.com>
# License: BSD 3 clause

ds = NREL()
turbine = ds.get_turbine(NREL.park_id['tehachapi'], 2004)
measurements = turbine.get_measurements()[:1000]
damaged = destroy(measurements, method='nmar',\
                  percentage=.80, min_length=10, max_length=50)
turbine.measurements = damaged
plot_timeseries(turbine, 0, 1000)

