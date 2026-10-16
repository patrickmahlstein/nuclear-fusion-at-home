#!/bin/bash
# N32: intake + fixed-recipe coil fit per plasma. Run from repository root with native python in $PY.
set -u
OUT=results/n32; mkdir -p $OUT
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1
for row in 60653 2931 46244 23761; do
  in=$OUT/row$row-input.json; $PY $N32/make_input.py $N32/row$row.json $in
  sha=$(shasum -a 256 $in | cut -d' ' -f1)
  $PY scripts/make_wout.py --input $in --input-sha256 $sha --output $OUT/wout-$row > $OUT/wout-$row.log 2>&1 || { echo "$row wout failed"; continue; }
  $PY scripts/make_target_spec.py --target-id dataset-row$row.v0 --input $in --input-sha256 $sha --wout $OUT/wout-$row/wout.nc \
     --vmecpp 0.8.0 --seed-candidate submissions/length-headroom-six-coil/candidate.json --output $OUT/spec-$row > $OUT/spec-$row.log 2>&1 || { echo "$row spec failed"; continue; }
  $PY scripts/fit_coils.py --target-spec $OUT/spec-$row/spec.json --wout $OUT/wout-$row/wout.nc --snapshot $OUT/spec-$row/seed.json \
     --output $PWD/$OUT/fit-$row --seconds 1800 --check-seconds 900 > $OUT/fit-$row.log 2>&1; echo "$row fit exit $?"
done
$PY scripts/fit_coils.py --target-spec results/n18/spec-selected/spec.json --wout results/n18/selected401/wout.nc --snapshot results/n18/spec-selected/seed.json \
   --output $PWD/$OUT/fit-sel401 --seconds 1800 --check-seconds 900 > $OUT/fit-sel401.log 2>&1; echo "sel401 fit exit $?"
