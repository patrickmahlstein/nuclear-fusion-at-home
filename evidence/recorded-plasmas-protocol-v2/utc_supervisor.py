"""Bound elapsed host time conservatively; do not infer why clocks diverge."""
from datetime import datetime, timezone
import os
from pathlib import Path
import shutil
import signal
import subprocess
import time


def deadline(start_monotonic, start_utc, budget, reservation_end, *, mono=None, utc=None):
    mono = time.monotonic() if mono is None else mono
    utc = time.time() if utc is None else utc
    elapsed = max(0.0, mono-start_monotonic, utc-start_utc)
    if utc >= reservation_end:
        return 'resource window expired'
    return 'elapsed-time limit' if elapsed >= budget else None


def supervise(command, output, env, stop_path, *, limits, reservation_end):
    start_m, start_w = time.monotonic(), time.time()
    reason = None
    with (output/'native.stdout').open('xb') as stdout, (output/'native.stderr').open('xb') as stderr:
        child = subprocess.Popen(command, cwd=output, env=env, stdout=stdout, stderr=stderr,
                                 start_new_session=True)
        try:
            while child.poll() is None:
                reason = deadline(start_m,start_w,limits['wall_seconds'],reservation_end)
                size = sum(p.stat().st_size for p in output.rglob('*') if p.is_file())
                if stop_path.exists(): reason = 'STOP present'
                elif size >= limits['output_bytes']: reason = 'output size limit'
                elif shutil.disk_usage(output).free < limits['runtime_disk_reserve_bytes']:
                    reason = 'runtime disk reserve'
                if reason: break
                time.sleep(.2)
        finally:
            if child.poll() is None:
                os.killpg(child.pid,signal.SIGTERM)
                try: child.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    os.killpg(child.pid,signal.SIGKILL);child.wait(timeout=5)
    # Reject late completion even when a process exited between monitor polls.
    reason = reason or deadline(start_m,start_w,limits['wall_seconds'],reservation_end)
    return dict(exit_code=child.returncode,stop_reason=reason,
                monotonic_seconds=time.monotonic()-start_m,utc_elapsed_seconds=time.time()-start_w,
                finished_at=datetime.now(timezone.utc).isoformat(),
                output_bytes=sum(p.stat().st_size for p in output.rglob('*') if p.is_file()))
