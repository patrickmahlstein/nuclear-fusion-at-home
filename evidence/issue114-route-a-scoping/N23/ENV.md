# constellaration 0.2.6 env without system installs (macOS x86_64, 15 Oct 2026)
curl -sL https://micro.mamba.pm/api/micromamba/osx-64/latest | tar -xj bin/micromamba
MAMBA_ROOT_PREFIX=$PWD/root ./bin/micromamba create -y -p $PWD/cst -c conda-forge python=3.12 booz_xform netcdf4 ninja cmake setuptools wheel pybind11 setuptools-scm
uv pip install --python cst/bin/python constellaration==0.2.6   # keeps conda booz_xform 0.1.0 (0.0.9 sdist fails to build here)
Resolved: constellaration 0.2.6, vmecpp 0.4.11, simsopt 1.8.1, numpy 2.2.6, booz_xform 0.1.0.
Control: scripts/constellaration_metrics.py at fae0938 reproduces #76 for both targets to all recorded digits
(L∇B 6.14039/6.13881, QI 2.3756e-5/2.1949e-5, FC 1.39591/1.39774, W -0.0157702/-0.0158143); 180 s.
