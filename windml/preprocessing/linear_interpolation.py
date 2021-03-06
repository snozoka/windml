"""
Copyright (c) 2013,
Fabian Gieseke, Justin P. Heinermann, Oliver Kramer, Jendrik Poloczek,
Nils A. Treiber
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    Redistributions of source code must retain the above copyright notice, this
    list of conditions and the following disclaimer.

    Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.

    Neither the name of the Computational Intelligence Group of the University
    of Oldenburg nor the names of its contributors may be used to endorse or
    promote products derived from this software without specific prior written
    permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from windml.preprocessing.missing_data_finder import MissingDataFinder
from numpy import zeros, int32, float32, nan

class LinearInterpolation(object):
    def interpolate(self, timeseries, **args):
        timestep = args['timestep']

        new_amount = int(timeseries.shape[0])
        misses = MissingDataFinder().find(timeseries, timestep)

        starts = {}
        for start, end, amount in misses:
            new_amount += int(amount)
            starts[start] = [int(end), int(amount)]

        # allocate new numpy array
        filled = zeros((new_amount,), dtype=[('date', int32),\
                ('corrected_score', float32),\
                ('speed', float32)])

        keys = starts.keys()
        current_index = 0

        for i in range(len(timeseries)):
            if i in keys:
            # missing data starting
                cs = 'corrected_score'
                d = 'date'
                sp = 'speed'

                # add start measurement
                filled[current_index] = timeseries[i]
                current_index += 1

                end, n = starts[i]
                n = int(n)
                # interpolate
                dy = (timeseries[end][cs] - timeseries[i][cs])
                dy2 = (timeseries[end][sp] - timeseries[i][sp])
                dx = (timeseries[end][d] - timeseries[i][d])
                gradient = dy / dx
                gradient2 = dy2 / dx

                for j in range(1, n + 1):
                    y = gradient * timestep * j + timeseries[i][cs]
                    y2 = gradient2 * timestep * j + timeseries[i][sp]
                    new_timestep = timeseries[i][d] + j * timestep
                    filled[current_index] = (new_timestep, y, y2)

                    current_index += 1
            else:
                filled[current_index] = timeseries[i]
                current_index += 1

        return filled
