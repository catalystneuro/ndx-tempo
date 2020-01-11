import os
from pynwb import load_namespaces, get_class
from pynwb import register_class, docval
from hdmf.utils import call_docval_func
from pynwb.file import MultiContainerInterface
from hdmf.common.table import DynamicTable, ElementIdentifiers

name = 'ndx-tempo'
here = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
ns_path = os.path.join(here, 'spec', name + '.namespace.yaml')

load_namespaces(ns_path)

Measurement = get_class('Measurement', name)
LaserLine = get_class('LaserLine', name)
PhotoDetector = get_class('PhotoDetector', name)


@register_class('LockInAmplifier', name)
class LockInAmplifier(DynamicTable):
    __columns__ = (
        {'name': 'channel_name',
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
            {'name': 'demod_bandwidth', 'type': 'Measurement',
             'doc': 'demodulation bandwidth of this device', 'default': None},
            {'name': 'demodulation_filter_order', 'type': 'float',
             'doc': 'demodulation_filter_order of this device', 'default': -1.0},
            {'name': 'reference', 'type': str,
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
Surgery = get_class('Surgery', name)
Subject = get_class('SubjectComplete', name)
