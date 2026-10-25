from datetime import datetime,timedelta,timezone
import json
from pathlib import Path
import tempfile
import unittest

from score_recorded import claim_check


class ClaimControls(unittest.TestCase):
    def test_current_owned_empty_claim_only(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'notes').mkdir();(root/'automation').mkdir()
            now=datetime.now(timezone.utc);digest='a'*64
            (root/'notes/claude.md').write_text('no current native task in test')
            note=root/'notes/codex.md'
            note.write_text(f'C18-RECORDED-V2 CLAIM manifest={digest} start={(now-timedelta(seconds=1)).isoformat()} end={(now+timedelta(hours=1)).isoformat()}\n')
            snap=root/'automation/process-check.json'
            data=dict(checked_at=now.isoformat(),native_compute_pids=[],controller_lock_held=True,other_codex_exec_worker=False)
            snap.write_text(json.dumps(data));manifest=dict(coordination=str(root),execution_authority='User25October2026continue; existing112lane')
            self.assertIn('claim_end',claim_check(manifest,digest))
            for change in [dict(native_compute_pids=[1]),dict(controller_lock_held=False),dict(other_codex_exec_worker=True),dict(checked_at=(now-timedelta(minutes=6)).isoformat())]:
                snap.write_text(json.dumps(dict(data,**change)))
                with self.assertRaises(ValueError):claim_check(manifest,digest)
            snap.write_text(json.dumps(data));note.write_text('old or missing claim')
            with self.assertRaises(ValueError):claim_check(manifest,digest)


if __name__=='__main__':unittest.main()
