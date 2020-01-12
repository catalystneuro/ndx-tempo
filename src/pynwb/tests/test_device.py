from numpy.testing import assert_array_equal
import numpy as np
from dateutil.tz import tzlocal
from datetime import datetime
from pynwb import NWBFile, NWBHDF5IO
from inspect import getsourcefile
from hdmf.common.table import VectorData
import os.path as path
import sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda: 0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])
from ndx_tempo import *
sys.path.pop(0)


def test_device():
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
                                       demod_bandwidth=Measurement(
                                           name='None', description='None', unit='Hz', data=[150]),
                                       columns=[
                                           VectorData(name='channel_name', description='None',
                                                      data=['name1', 'name2']),
                                           Measurement(name='offset', description='None',
                                                       unit='mV', data=[140, 260]),
                                           VectorData(name='gain', description='None', data=[250, 250])]
                                       )
    lockinamp_devices_ = LockInAmplifierDevices()
    lockinamp_devices_.add_lockinamp(lockinamp_device)

    nwbfile.add_device(TEMPO(name='tempo_test',
                             laserline_devices=laserline_devices_,
                             photodetector_devices=photodetector_devices_,
                             lockinamp_devices=lockinamp_devices_)
                       )

    # testing laserline_device
    assert_array_equal(np.array(nwbfile.devices['tempo_test'].
                                laserline_devices.children[0].analog_modulation_frequency.data), np.array([100]))
    # testing photodetector_device
    assert_array_equal(np.array(nwbfile.devices['tempo_test'].
                                photodetector_devices.children[0].bandwidth.data), np.array([50]))
    # testing lockinamp_device
    assert_array_equal(np.array(nwbfile.devices['tempo_test'].
                                lockinamp_devices.children[0].columns[1].data), np.array([140, 260]))

    with NWBHDF5IO('test_ndx-tempo.nwb', 'w') as io:
        io.write(nwbfile)
        del nwbfile
    with NWBHDF5IO('test_ndx-tempo.nwb', 'r', load_namespaces=True) as io:
        nwb = io.read()
        # testing laserline_device
        assert_array_equal(np.array(nwb.devices['tempo_test'].
                                    laserline_devices.children[0].analog_modulation_frequency.data), np.array([100]))
        # testing photodetector_device
        assert_array_equal(np.array(nwb.devices['tempo_test'].
                                    photodetector_devices.children[0].bandwidth.data), np.array([50]))
        # testing lockinamp_device
        assert_array_equal(np.array(nwb.devices['tempo_test'].
                                    lockinamp_device.children[0].columns[1].data), np.array([140, 260]))


def test_surgery():
    nwbfile = NWBFile('session description', 'session id', datetime.now(tzlocal()),
                      experimenter='experimenter name',
                      lab='lab name',
                      institution='institution name',
                      experiment_description=('experiment description'),
                      session_id='sessionid')
    surgery_tempo = Surgery(surgery_date='0000-0-0',
                            implantation_device='my_implantationdevice',
                            ophys_implant_name='myophysimplantname',
                            virus_injection_id='virusID',
                            virus_injection_opsin_l_r='R',
                            virus_injection_coordinates='[1.0, 2.0, 3.0]',
                            ophys_injection_date='000-00-00',
                            ophys_injection_flr_protein_data=DynamicTable(
                                                             name='name',
                                                             description='ophys_data',
                                                             columns=[VectorData(
                                                                        name='protein_name',
                                                                        description='protein_name_column',
                                                                        data=['protein1', 'protein2']),
                                                                      Measurement(
                                                                         name='protein_concentration',
                                                                         description='protein_conc_column',
                                                                         data=[2e12, 5e12],
                                                                         unit='ml')]
                                                                            )
                            )
    mouse_data_tempo = SubjectComplete(name='mouse_metadata',
                                       surgery_data=surgery_tempo,
                                       sacrificial_date='0000-00-00',
                                       strain='myanimalstrain')

    nwbfile.subject = mouse_data_tempo
    # testing nwbfile addition:
    assert_array_equal(
        nwbfile.subject.surgery_data.ophys_injection_flr_protein_data.columns[1].data, [2e12, 5e12])
    assert_array_equal(
        nwbfile.subject.surgery_data.virus_injection_coordinates, [1.0, 2.0, 3.0])
    with NWBHDF5IO('test_device_surgery.nwb', 'w') as io:
        io.write(nwbfile)
        del nwbfile
    with NWBHDF5IO('test_device_surgery.nwb', 'r', load_namespaces=True) as io:
        nwb = io.read()
        assert_array_equal(
            nwb.subject.surgery_data.ophys_injection_flr_protein_data.columns[1].data, [2e12, 5e12])
        assert_array_equal(
            nwb.subject.surgery_data.virus_injection_coordinates, [1.0, 2.0, 3.0])
