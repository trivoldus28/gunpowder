from gunpowder.ext import h5py
from .hdf5like_source_base import Hdf5LikeSource

class Hdf5Source(Hdf5LikeSource):
    '''An HDF5 data source.

    Provides arrays from HDF5 datasets. If the attribute ``resolution`` is set
    in a HDF5 dataset, it will be used as the array's ``voxel_size``. If the
    attribute ``offset`` is set in a dataset, it will be used as the offset of
    the :class:`Roi` for this array. It is assumed that the offset is given in
    world units.

    Args:

        filename (``string``):

            The HDF5 file.

        datasets (``dict``, :class:`ArrayKey` -> ``string``):

            Dictionary of array keys to dataset names that this source offers.

        array_specs (``dict``, :class:`ArrayKey` -> :class:`ArraySpec`, optional):

            An optional dictionary of array keys to array specs to overwrite
            the array specs automatically determined from the data file. This
            is useful to set a missing ``voxel_size``, for example. Only fields
            that are not ``None`` in the given :class:`ArraySpec` will be used.
    '''
    def _open_file(self, filename):
        return h5py.File(filename, 'r')
