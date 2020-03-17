from numpy.testing import assert_array_equal
import numpy as np
from dateutil.tz import tzlocal
from datetime import datetime
from pynwb import NWBFile, NWBHDF5IO
from inspect import getsourcefile
from hdmf.common.table import VectorData
import os
import sys
import unittest
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ndx_tempo')))
# # current_dir = path.dirname(path.abspath(getsourcefile(lambda: 0)))
# # sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])
from ndx_tempo import *
sys.path.pop(0)


nwbfile = NWBFile('session description', 'session id', datetime.now(tzlocal()),
                  experimenter='experimenter name',
                  lab='lab name',
                  institution='institution name',
                  experiment_description=('experiment description'),
                  session_id='sessionid')
laserline_device = LaserLine(name='mylaserline1', reference='test_ref_laserline',
                             analog_modulation_frequency=Measurement(
                                 name='None', description='None', unit='Hz', data=[100]),
                             power=Measurement(name='None', description='None', unit='uW', data=[100]))

laserline_devices_ = LaserLineDevices()
laserline_devices_.add_laserline(laserline_device)
laserline_devices_.create_laserline(name='mylaserline2', reference='test_ref_laserline',
                                    analog_modulation_frequency=Measurement(
                                        name='None', description='None', unit='Hz', data=[100]),
                                    power=Measurement(name='None', description='None', unit='uW', data=[100]))

photodetector_device = PhotoDetector(name='myphotodetector1', reference='test_ref_photodetector',
                                     gain=Measurement(name='None', description='None',
                                                      unit='Hz', data=[1]),
                                     bandwidth=Measurement(name='None', description='None', unit='uW', data=[50]))

photodetector_devices_ = PhotoDetectorDevices()
photodetector_devices_.add_photodetector(photodetector_device)

lockinamp_device = LockInAmplifier(name='mylockinamp', demodulation_filter_order=10.0,
                                   reference='test_ref',
                                   # demod_bandwidth=VectorData(
                                   #     name='None', description='None', data=[150]),
                                   columns=[
                                       VectorData(name='channel_name', description='None',
                                                  data=['name1', 'name2']),
                                       VectorData(name='offset', description='None',
                                                   data=[140, 260]),
                                       VectorData(name='gain', description='None', data=[250, 250])]
                                   )
lockinamp_devices_ = LockInAmplifierDevices()
lockinamp_devices_.add_lockinamp(lockinamp_device)

nwbfile.add_device(TEMPO(name='tempo_test',
                         laserline_devices=laserline_devices_,
                         photodetector_devices=photodetector_devices_,
                         lockinamp_devices=lockinamp_devices_)
                   )

nwbfile.add_analysis(lockinamp_devices_)   # can add container, dynamic table
nwbfile.add_analysis(lockinamp_device)

mod = nwbfile.create_processing_module('device_cont', 'contains devices')
mod.add_container(lockinamp_device) # data interface, dynamic table
# mod.add_data_interface(lockinamp_device) # same as above
mod.add_data_interface(lockinamp_devices_)
# mod.add(lockinamp_device) # add anything! same as above

with NWBHDF5IO('test_ndx-tempo.nwb', 'w') as io:
    io.write(nwbfile)

with NWBHDF5IO('test_ndx-tempo.nwb', 'r') as io:
    nwbfile2 = io.read()
