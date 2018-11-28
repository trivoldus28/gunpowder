import logging
# import multiprocessing
# import numpy as np
# from gunpowder.array import Array
# from gunpowder.batch import Batch
# from gunpowder.coordinate import Coordinate
# from gunpowder.points import Points
# from gunpowder.producer_pool import ProducerPool
# from gunpowder.roi import Roi
# from .batch_filter import BatchFilter

from .scan import Scan
from gunpowder.batch import Batch

# import sys
# sys.path.insert(0, "/groups/funke/home/nguyent3/programming/daisy/")
import daisy

logger = logging.getLogger(__name__)

class DaisyScan(Scan):
    '''
    '''

    def __init__(self, reference, roi_mapping, num_workers=1, cache_size=50):

        super().__init__(reference, num_workers, cache_size)
        self.roi_mapping = roi_mapping


    def setup(self):

        super().setup()
        self.daisy_sched = daisy.RemoteActor()


    def provide(self, request):

        scan_spec = self.spec
        daisy_batch = Batch()

        while True:

            block = self.daisy_sched.acquire_block()

            if block == daisy.RemoteActor.END_OF_BLOCK:
                logger.info("END_OF_BLOCK received from Daisy")
                break;

            logger.info("Got block from daisy: {}".format(block))

            # note: this step is necessary and user must provide the mapping
            # because Daisy does not know which data stream is read or write
            for key, reference_spec in self.reference.items():
                if key not in self.roi_mapping:
                    logger.error("roi_mapping does not map stream {} to either 'read_roi' or 'write_roi'".format(key))
                    assert(0)

                if self.roi_mapping[key] == "read_roi":
                    scan_spec[key].roi = block.read_roi
                    
                elif self.roi_mapping[key] == "write_roi":
                    scan_spec[key].roi = block.write_roi

            # TODO: not sure how to handle this better and not discarding results from previous loop
            daisy_batch = super().provide(request=[], dummy_request=scan_spec)

            self.daisy_sched.release_block(block, ret=0)

        return daisy_batch
