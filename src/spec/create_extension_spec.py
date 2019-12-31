from pynwb.spec import NWBDatasetSpec, NWBNamespaceBuilder, NWBGroupSpec, NWBAttributeSpec
from export_spec import export_spec

name = 'ndx-TEMPO'
ns_path = name + ".namespace.yaml"
ext_source = name + ".extensions.yaml"


def main():
    ns_builder = NWBNamespaceBuilder(
        doc='nwb extention for voltage imaging technique called TEMPO',
        name='ndx-tempo',
        version='0.1.0',
        author=list(map(str.strip, 'Saksham Sharda'.split(','))),
        contact=list(map(str.strip, 'sxs1790@case.edu'.split(',')))
    )

    ns_builder.include_type('VectorData', namespace='core')
    ns_builder.include_type('DynamicTable', namespace='core')
    ns_builder.include_type('Subject', namespace='core')
    ns_builder.include_type('Device', namespace='core')

    vector_data_custom = NWBDatasetSpec('A custom VectorData type',
                                        attributes=[NWBAttributeSpec(
                                            'Unit', 'specification of unit', 'text')],
                                        neurodata_type_def='CustomVectorData',
                                        neurodata_type_inc='VectorData',
                                        quantity='*')

    # Typedef for laserline
    laserline_device = NWBGroupSpec(neurodata_type_def='LaserLine',
                                    neurodata_type_inc='NWBDataInterface',
                                    doc='Desc of laserline device, part for a TEMPO device',
                                    quantity='?')

    laserline_device.add_dataset(
        name='Reference',
        neurodata_type_inc='CustomVectorData',
        doc='Reference metadata of the laserline module',
        dims=('NoOfDevices',),
        shape=(None),
        dtype='text',
        quantity='?'
    )

    laserline_device.add_dataset(
        name='AnalogModulationFrequency',
        neurodata_type_inc='CustomVectorData',
        doc='AnalogModulationFrequency metadata of the laserline module',
        dims=('NoOfDevices',),
        shape=(None),
        dtype='float',
        quantity='?'
    )

    laserline_device.add_dataset(
        name='Power',
        neurodata_type_inc='CustomVectorData',
        doc='Power metadata of the laserline module',
        dims=('NoOfDevices',),
        shape=(None),
        dtype='float',
        quantity='?'
    )

  # Typedef for PhotoDetector
    phototector_device = NWBGroupSpec(neurodata_type_def='PhotoDetector',
                                      neurodata_type_inc='NWBDataInterface',
                                      doc='Desc of phototector device, part for a TEMPO device',
                                      quantity='?')

    phototector_device.add_dataset(
        name='Reference',
        neurodata_type_inc='CustomVectorData',
        doc='Reference metadata of the phototector module',
        dims=('NoOfDevices',),
        shape=(None),
        dtype='text',
        quantity='?'
    )

    phototector_device.add_dataset(
        name='Gain',
        neurodata_type_inc='CustomVectorData',
        doc='Gain metadata of the phototector module',
        dims=('NoOfDevices',),
        shape=(None),
        dtype='float',
        quantity='?'
    )

    phototector_device.add_dataset(
        name='BandWidth',
        neurodata_type_inc='CustomVectorData',
        doc='BandWidth metadata of the phototector module',
        dims=('NoOfDevices',),
        shape=(None),
        dtype='float',
        quantity='?'
    )

    # Typedef for LockInAmplifier
    lockinamp_device = NWBGroupSpec(neurodata_type_def='LockInAmplifier',
                                    neurodata_type_inc='NWBDataInterface',
                                    doc='Desc of lockinamplifier device, part for a TEMPO device',
                                    quantity='?')

    lockinamp_device.add_dataset(
        name='Reference',
        neurodata_type_inc='CustomVectorData',
        doc='Reference metadata of the lockinamp module',
        shape=(1, 1),
        dtype='text',
    )

    lockinamp_device.add_dataset(
        name='DemodBandwidth',
        neurodata_type_inc='CustomVectorData',
        doc='DemodBandwidth metadata of the lockinamp module',
        shape=(1, 1),
        dtype='float',
    )

    lockinamp_device.add_dataset(
        name='DemodFilterOrder',
        neurodata_type_inc='CustomVectorData',
        doc='DemodFilterOrder metadata of the lockinamp module',
        shape=(1, 1),
        dtype='float',
    )

    lockinamp_device.add_dataset(
        name='Name',
        neurodata_type_inc='CustomVectorData',
        doc='Name of the channel of lockinamp',
        dims=('ChannelNo',),
        shape=(None),
        dtype='text',
        quantity='?'
    )

    lockinamp_device.add_dataset(
        name='Offset',
        neurodata_type_inc='CustomVectorData',
        doc='Offset for channel of lockinamp',
        dims=('ChannelNo',),
        shape=(None),
        dtype='float',
        quantity='?'
    )

    lockinamp_device.add_dataset(
        name='Gain',
        neurodata_type_inc='CustomVectorData',
        doc='Gain for channel of lockinamp',
        dims=('ChannelNo',),
        shape=(None),
        dtype='float',
        quantity='?'
    )

    tempo_device = NWBGroupSpec(neurodata_type_def='TEMPO',
                                neurodata_type_inc='NWBDataInterface',
                                doc='Datatype for a TEMPO device',
                                quantity='*',
                                attributes=[NWBAttributeSpec(
                                    name='NoOfModules',
                                    doc='the number of electronic modules with this acquisition system',
                                    dtype='float',
                                    required=True)],
                                groups=[laserline_device,
                                        phototector_device,
                                        lockinamp_device]
                                )

    new_data_types = [tempo_device]
    export_spec(ns_builder, new_data_types)


if __name__ == "__main__":
    main()
