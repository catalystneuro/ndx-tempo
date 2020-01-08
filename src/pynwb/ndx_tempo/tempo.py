import os

import pandas as pd
from pynwb import load_namespaces, get_class
from pynwb.misc import AnnotationSeries
from pynwb import register_class, docval, get_class
from hdmf.common.table import VectorIndex, VectorData, DynamicTable, ElementIdentifiers
from hdmf.utils import call_docval_func
from pynwb import NWBFile, NWBHDF5IO
from datetime import datetime
from dateutil.tz import tzlocal
from pynwb.device import Device
from pynwb.file import MultiContainerInterface, NWBContainer

name = 'ndx-tempo'

here = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
ns_path = os.path.join(here, 'spec', name + '.namespace.yaml')

load_namespaces(ns_path)

# Tempo = get_class('TEMPO', name)

nwbfile = NWBFile('my first synthetic recording', 'EXAMPLE_ID', datetime.now(tzlocal()),
                  experimenter='Dr. Bilbo Baggins',
                  lab='Bag End Laboratory',
                  institution='University of Middle Earth at the Shire',
                  experiment_description=('I went on an adventure with thirteen '
                                          'dwarves to reclaim vast treasures.'),
                  session_id='LONELYMTN')


@register_class('LockInAmplifier', name)
class LockInAmplifier(DynamicTable):
    __columns__ = (
        {'name': 'name',
         'description': 'name of the channel of lock_in_amp'},
        {'name': 'offset',
         'description': 'offset for channel of lock_in_amp'},
        {'name': 'gain',
         'description': 'gain for channel of lock_in_amp'}
    )

    @docval({'name': 'name', 'type': str, 'doc': 'Name of this Compartments object',
             'default': 'compartments'},
            {'name': 'description', 'type': str, 'doc': 'a description of what is in this table',
             'default': None},
            {'name': 'demodulation_bandwidth', 'type': 'Measurement',
             'doc': 'demodulation bandwidth of this device', 'default': None},
            {'name': 'demodulation_filter_order', 'type': 'float',
             'doc': 'demodulation_filter_order of this device', 'default': -1.0},
            {'name': 'reference', 'type': 'text',
             'doc': 'reference of this device', 'default': None},
            {'name': 'id', 'type': ('array_data', ElementIdentifiers),
             'doc': 'the identifiers for the units stored in this interface', 'default': None},
            {'name': 'columns', 'type': (tuple, list),
             'doc': 'the columns in this table', 'default': None},
            {'name': 'colnames', 'type': 'array_data', 'doc': 'the names of the columns in this table',
             'default': None},
            )
    def __init__(self, **kwargs):
        if kwargs.get('description', None) is None:
            kwargs['description'] = "meta-data for the LockInAmplifier for TEMPO device"
        call_docval_func(super().__init__, kwargs)


Measurement = get_class('Measurement', name)
LaserLine = get_class('LaserLine', name)
# LaserLineDevices = get_class('LaserLineDevices', name)
PhotoDetector = get_class('PhotoDetector', name)
# PhotoDetectorDevices = get_class('PhotoDetectorDevices', name)
# LockInAmplifier = get_class('LockInAmplifier', name)


@register_class('LaserLineDevices', name)
class LaserLineDevices(MultiContainerInterface):

    __clsconf__ = {
        'attr': 'laserline devices',
        'type': LaserLine,
        'add': 'add_laserline',
        'get': 'get_laserline',
        'create': 'create_laserline',
    }


@register_class('PhotoDetectorDevices', name)
class PhotoDetectorDevices(MultiContainerInterface):

    __clsconf__ = {
        'attr': 'photodetector devices',
        'type': PhotoDetector,
        'add': 'add_photodetector',
        'get': 'get_photodetector',
        'create': 'create_photodector',
    }


@register_class('LockInAmplifierDevices', name)
class LockInAmplifierDevices(MultiContainerInterface):

    __clsconf__ = {
        'attr': 'lockinamp_device devices',
        'type': LockInAmplifier,
        'add': 'add_lockinamp',
        'get': 'get_lockinamp',
        'create': 'create_lockinamp',
    }


TEMPO = get_class('TEMPO', name)

laserline_device = LaserLine(name='mylaserline1', reference='test_ref_laserline',
                             analog_modulation_frequency=Measurement(
                                 name='None', description='None', unit='Hz', data=[100]),
                             power=Measurement(name='None', description='None', unit='uW', data=[100]))

laserline_devices_ = LaserLineDevices()
laserline_devices_.add_laserline(laserline_device)

photodetector_device = PhotoDetector(name='myphotodetector1', reference='test_ref_photodetector',
                                     gain=Measurement(name='None', description='None',
                                                      unit='Hz', data=[1]),
                                     bandwidth=Measurement(name='None', description='None', unit='uW', data=[50]))

photodetector_devices_ = PhotoDetectorDevices()
photodetector_devices_.add_photodetector(photodetector_device)

lockinamp_device = LockInAmplifier(name='mylockinamp')
lockinamp_devices_ = LockInAmplifierDevices()
lockinamp_devices_.add_lockinamp(lockinamp_device)

nwbfile.add_device(TEMPO(name='tempo_test',
                         laserline_devices=laserline_devices_,
                         photodetector_devices=photodetector_devices_,
                         lockinamp_devices=lockinamp_devices_)
                   )
nwbfile.add_analysis(laserline_device)
nwbfile.add_analysis(photodetector_device)
pmod = nwbfile.create_processing_module('module_name', 'desc')
pmod.add_container(laserline_device)
pmod.add_container(photodetector_device)
pmod.add_container(lockinamp_device)

with NWBHDF5IO('testingnwbout.nwb', 'w') as io:
    io.write(nwbfile)
