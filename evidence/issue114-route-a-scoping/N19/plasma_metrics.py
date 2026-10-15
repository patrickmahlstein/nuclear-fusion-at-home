"""Native mirror of ConStellaration 0.2.6 vacuum well and flux compression (s=0.49)."""
import sys, numpy as np
from simsopt.mhd import Vmec, vmec_fieldlines

def metrics(wout):
    vs = Vmec(wout)
    w = vs.wout
    dv = 4*np.pi**2*np.abs(w.gmnc[0, 1:])
    a0 = 1.5*dv[0]-0.5*dv[1]; a1 = 1.5*dv[-1]-0.5*dv[-2]
    well = (a0-a1)/a0
    nfp, sym = w.nfp, not w.lasym
    lim = 2*np.pi/nfp/(1+int(sym))
    alpha = np.linspace(-lim, lim, 101, endpoint=False)
    theta = np.linspace(-np.pi, np.pi, 64, endpoint=False)
    s = np.array([0.49])
    d = vmec_fieldlines(vs, s, alpha, theta1d=theta)
    wts = np.abs(d.sqrt_g_vmec)/np.abs(d.sqrt_g_vmec).mean(axis=(1, 2))[:, None, None]
    grr = w.Aminor_p**2/(4*s[:, None, None])*d.grad_s_dot_grad_s
    kd = d.B_cross_kappa_dot_grad_alpha*np.sign(w.phipf[-1])
    fc = float(np.mean(np.heaviside(kd, 0)*grr*wts, axis=(1, 2))[0])
    return dict(vacuum_well=float(well), flux_compression=fc, aspect=float(w.aspect),
                iota_edge_per_fp=float(abs(w.iotaf[-1]))/nfp, ns=int(w.ns))

if __name__ == "__main__":
    for f in sys.argv[1:]:
        print(f, metrics(f))
