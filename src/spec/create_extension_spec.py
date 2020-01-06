from pynwb.spec import NWBDatasetSpec, NWBNamespaceBuilder, NWBGroupSpec, NWBAttributeSpec
from export_spec import export_spec

name = 'ndx-tempo'
ns_path = name + ".namespace.yaml"
ext_source = name + ".extensions.yaml"


def main():
    ns_builder = NWBNamespaceBuilder(
        doc='nwb extention for voltage imaging technique called TEMPO',
        name=name,
        version='0.1.0',
        author=list(map(str.strip, 'Saksham Sharda'.split(','))),
        contact=list(map(str.strip, 'sxs1790@case.edu'.split(',')))
    )

    ns_builder.include_type('VectorData', namespace='core')
    ns_builder.include_type('DynamicTable', namespace='core')
    ns_builder.include_type('Subject', namespace='core')
    ns_builder.include_type('NWBDataInterface', namespace='core')
    ns_builder.include_type('Device', namespace='core')

    measurement = NWBDatasetSpec('Flexible vectordataset with a custom unit/conversion/resolution'
                                 ' field similar to timeseries.data',
                                 attributes=[
                                     NWBAttributeSpec('unit',
                                                      'The base unit of measure used to store data. This should be in the SI unit.'
                                                      'COMMENT: This is the SI unit (when appropriate) of the stored data, such as '
                                                      'Volts. If the actual data is stored in millivolts, the field ''conversion'' '
                                                      'below describes how to convert the data to the specified SI unit.',
                                                      'text'),
                                     NWBAttributeSpec('conversion',
                                                      'Scalar to multiply each element in '
                                                      'data to convert it to the specified unit',
                                                      'float32', required=False, default_value=1.0),
                                     NWBAttributeSpec('resolution',
                                                      'Smallest meaningful difference between values in data, stored in the specified '
                                                      'by unit. COMMENT: E.g., the change in value of the least significant bit, or '
                                                      'a larger number if signal noise is known to be present. If unknown, use -1.0',
                                                      'float32', required=False, default_value=0.0)
                                 ],
                                 neurodata_type_def='Measurement',
                                 neurodata_type_inc='VectorData',
                                 )


    # Typedef for laserline
    laserline_device = NWBGroupSpec(neurodata_type_def='LaserLine',
                                    neurodata_type_inc='NWBDataInterface',
                                    doc='description of laserline device, part for a TEMPO device',
                                    quantity='*')

    laserline_device.add_dataset(
        name='reference',
        neurodata_type_inc='VectorData',
        doc='reference metadata of the laserline module',
        shape=(1,),
        dtype='text',
        quantity='?'
    )

    laserline_device.add_dataset(
        name='analog_modulation_frequency',
        neurodata_type_inc=measurement,
        doc='analog_modulation_frequency of the laserline module',
        shape=(1,),
        dtype='float32',
        quantity='?'
    )

    laserline_device.add_dataset(
        name='power',
        neurodata_type_inc=measurement,
        doc='power of the laserline module',
        shape=(1,),
        dtype='float32',
        quantity='?'
    )

    # Typedef for PhotoDetector
    phototector_device = NWBGroupSpec(neurodata_type_def='PhotoDetector',
                                      neurodata_type_inc='NWBDataInterface',
                                      doc='description of phototector device, part for a TEMPO device',
                                      quantity='*')

    phototector_device.add_dataset(
        name='reference',
        neurodata_type_inc='VectorData',
        doc='reference of the phototector module',
        shape=(1,),
        dtype='text',
        quantity='?'
    )

    phototector_device.add_dataset(
        name='gain',
        neurodata_type_inc=measurement,
        doc='gain of the phototector module',
        shape=(1,),
        dtype='int32',
        quantity='?'
    )

    phototector_device.add_dataset(
        name='bandwidth',
        neurodata_type_inc=measurement,
        doc='bandwidth metadata of the phototector module',
        shape=(1,),
        dtype='float32',
        quantity='?'
    )

    # Typedef for LockInAmplifier
    lockinamp_device = NWBGroupSpec(neurodata_type_def='LockInAmplifier',
                                    neurodata_type_inc='DynamicTable',
                                    doc='description of lock_in_amp device, part for a TEMPO device',
                                    quantity='?')

    lockinamp_device.add_dataset(
        name='reference',
        neurodata_type_inc='VectorData',
        doc='reference metadata of the lock_in_amp module',
        shape=(1,),
        dtype='text',
        quantity='?'
    )

    lockinamp_device.add_dataset(
        name='demod_bandwidth',
        neurodata_type_inc=measurement,
        doc='demodulation bandwidth metadata of the lock_in_amp module',
        shape=(1,),
        dtype='float32',
        quantity='?'
    )

    lockinamp_device.add_dataset(
        name='demodulation_filter_order',
        neurodata_type_inc='VectorData',
        doc='demodulation filter order metadata of the lock_in_amp module',
        shape=(1,),
        dtype='int8',
        quantity='?'
    )

    lockinamp_device.add_dataset(
        name='name',
        neurodata_type_inc='VectorData',
        doc='name of the channel of lock_in_amp',
        dims=('no_of_channels',),
        shape=(None,),
        dtype='text',
        quantity='?'
    )

    lockinamp_device.add_dataset(
        name='offset',
        neurodata_type_inc=measurement,
        doc='offset for channel of lock_in_amp',
        dims=('no_of_channels',),
        shape=(None,),
        dtype='float32',
        quantity='?'
    )

    lockinamp_device.add_dataset(
        name='gain',
        neurodata_type_inc='VectorData',
        doc='gain for channel of lock_in_amp',
        dims=('no_of_channels',),
        shape=(None,),
        dtype='int32',
        quantity='?'
    )

    tempo_device = NWBGroupSpec(neurodata_type_def='TEMPO',
                                neurodata_type_inc='Device',
                                doc='datatype for a TEMPO device',
                                attributes=[NWBAttributeSpec(
                                    name='no_of_modules',
                                    doc='the number of electronic modules with this acquisition system',
                                    dtype='float',
                                    required=False,
                                    default_value=3)],
                                groups=[laserline_device,
                                        phototector_device,
                                        lockinamp_device]
                                )


    new_data_types = [measurement, tempo_device]
    export_spec(ns_builder, new_data_types)


if __name__ == "__main__":
    main()
