"""N19 mirror plus edge mirror ratio (ConStellaration 0.2.6 formula, Nyquist grid at LCFS)."""
import os, sys, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "n19"))
from plasma_metrics import metrics as base_metrics
import netCDF4

def edge_mirror(wout, nt=64, nz=64):
    with netCDF4.Dataset(wout) as d:
        b = d["bmnc"][-1, :]; m = d["xm_nyq"][:]; n = d["xn_nyq"][:]
    th, ph = np.meshgrid(np.linspace(0, 2*np.pi, nt), np.linspace(0, 2*np.pi, nz), indexing="ij")
    B = np.einsum("k,kij->ij", b, np.cos(m[:, None, None]*th - n[:, None, None]*ph))
    return float((B.max()-B.min())/(B.max()+B.min()))

def metrics(wout):
    r = base_metrics(wout); r["edge_mirror"] = edge_mirror(wout); return r

if __name__ == "__main__":
    for f in sys.argv[1:]: print(f, metrics(f))
