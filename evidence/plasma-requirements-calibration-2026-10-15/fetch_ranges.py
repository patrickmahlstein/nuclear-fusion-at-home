"""Fetch only manifest-bound columns; no dataset or publisher code is executed."""
import concurrent.futures
import hashlib
import json
import shutil
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REVISION = '8da71572eb63ce93e77ce89bec0d7c30b7eba89e'
MAX_BYTES = 128*1024**2


def main():
    manifest = json.loads((ROOT/'ranges.json').read_text(encoding='utf-8'))
    entries = {Path(p['entry']['path']).stem: p['entry']
               for p in json.loads((ROOT/'range-plan.json').read_text(encoding='utf-8'))}
    jobs = []
    for key, digest in manifest.items():
        stem, start, end = key.removesuffix('.range').rsplit('-', 2)
        jobs.append((key, entries[stem], int(start), int(end), digest))
    if sum(end-start+1 for _, _, start, end, _ in jobs) > MAX_BYTES:
        raise ValueError('128 MiB input transfer ceiling')
    if shutil.disk_usage(ROOT).free < 3*1024**3:
        raise ValueError('3 GiB initial reserve required')
    started = time.monotonic()

    def fetch(job):
        key, entry, start, end, digest = job
        path = ROOT/key
        size = end-start+1
        if path.exists():
            data = path.read_bytes()
        else:
            if time.monotonic()-started > 900 or shutil.disk_usage(ROOT).free < 2*1024**3:
                raise ValueError('time/disk ceiling')
            url = ('https://huggingface.co/datasets/proxima-fusion/constellaration/resolve/'
                   + REVISION + '/' + entry['path'])
            request = urllib.request.Request(url, headers={'Range': f'bytes={start}-{end}'})
            with urllib.request.urlopen(request, timeout=30) as response:
                if response.status != 206 or response.headers.get('Content-Range') != (
                        f"bytes {start}-{end}/{entry['size']}"):
                    raise ValueError('range response required; no bulk fallback')
                data = response.read(size+1)
            if len(data) == size and hashlib.sha256(data).hexdigest() == digest:
                path.write_bytes(data)
        if len(data) != size or hashlib.sha256(data).hexdigest() != digest:
            raise ValueError('range integrity failure: '+key)
        return size

    # Four network requests may overlap; numerical analysis remains one-threaded.
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        sizes = list(pool.map(fetch, jobs))
    print(f'Verified {len(sizes)} ranges, {sum(sizes)} input bytes.')


if __name__ == '__main__':
    main()
