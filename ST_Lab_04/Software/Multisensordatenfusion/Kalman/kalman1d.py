"""
Implementierung eines Kalman-Filters in 1D nach Thrun, udacity cs373
"""

import numpy as np

mu = 0.  # Anfangsposition unbekannt, zu Null angenommen
var = 10000.  # Anfangsposition unsicher, daher sehr hohe Varianz als Start

measurements = np.array([5., 6., 7., 9., 10.])  # Messungen der Position z.B. durch GPS
var_measure = 4.  # Varianz des Positionssensors

motion = np.array([1., 1., 2., 1., 1.])  # hier zur Vereinfachung explizit angegeben
var_motion = 2.

# Measurement update
def update(mu1, var1, mu2, var2):
    mu = (var1 * mu2 + var2 * mu1) / (var1 + var2)
    var = 1 / (1/var1 + 1/var2)
    return [mu, var]

# Motion prediction
def predict(mu1, var1, mu2, var2):
    mu = mu1 + mu2
    var = var1 + var2
    return [mu, var]
    
# Kalman-Filter 1D
for i in range(len(measurements)):
    
    [mu, var] = update(mu, var, measurements[i], var_measure)
    print("update  %d: %7.4f - %7.4f" %(i, mu, var))
    [mu, var] = predict(mu, var, motion[i], var_motion)
    print("predict %d: %7.4f - %7.4f" %(i, mu, var))
    
    
