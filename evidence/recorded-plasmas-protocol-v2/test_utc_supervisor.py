import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

import utc_supervisor as timer


class DeadlineControls(unittest.TestCase):
    def test_forward_wall_jump_expires_without_monotonic_progress(self):
        self.assertEqual(timer.deadline(10,100,900,3000,mono=11,utc=1101),'elapsed-time limit')

    def test_backward_wall_jump_does_not_extend_active_budget(self):
        self.assertEqual(timer.deadline(10,100,900,3000,mono=911,utc=50),'elapsed-time limit')

    def test_reservation_end_is_independent(self):
        self.assertEqual(timer.deadline(10,100,900,101,mono=10.1,utc=101),'resource window expired')
        self.assertIsNone(timer.deadline(10,100,900,2000,mono=11,utc=101))

    def test_real_harmless_child_is_stopped_and_reaped(self):
        with tempfile.TemporaryDirectory() as directory:
            output=Path(directory)
            result=timer.supervise([sys.executable,'-c','import time;time.sleep(30)'],output,
                {},output/'STOP',limits=dict(wall_seconds=.05,output_bytes=1000000,
                runtime_disk_reserve_bytes=0),reservation_end=time.time()+60)
            self.assertEqual(result['stop_reason'],'elapsed-time limit')
            self.assertNotEqual(result['exit_code'],0)

    def test_utc_jump_stops_a_child_with_monotonic_time_still_available(self):
        with tempfile.TemporaryDirectory() as directory:
            output=Path(directory)
            with patch.object(timer.time,'time',side_effect=[100,1101,1101,1101,1101]):
                result=timer.supervise([sys.executable,'-c','import time;time.sleep(30)'],output,
                    {},output/'STOP',limits=dict(wall_seconds=900,output_bytes=1000000,
                    runtime_disk_reserve_bytes=0),reservation_end=3000)
            self.assertEqual(result['stop_reason'],'elapsed-time limit')
            self.assertNotEqual(result['exit_code'],0)


if __name__=='__main__':unittest.main()
