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


TEMPO = get_class('Miniscope', name)
# nwbfile.add_device([TEMPO(unit='test',name='temp',description='desc')])
nwbfile.add_device(TEMPO('temp_miniscope'))
# nwbfile.devices=[TEMPO(name='tempdevice')]
# nwbfile.add_device(Device('temp_device'))
with NWBHDF5IO('testingnwbout.nwb', 'w') as io:
    io.write(nwbfile)
