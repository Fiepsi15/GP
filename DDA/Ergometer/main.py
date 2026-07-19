from DDA.Ergometer.subscripts import calibration
from DDA.Ergometer.subscripts import force_and_power
import numpy as np

data_dir = 'DDA/Ergometer/daten'
masses = [0, 500, 1000, 2000]
measurement_rates = 500

factor, offset = calibration.calibrate(data_dir, masses, measurement_rates)

students = [1, 2]
force_and_power.analyze_student(data_dir, factor, offset, students)