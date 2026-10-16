#!/bin/bash
# N33: neutral centred-circular seed, same fit recipe, 5 plasmas. Repository root; $PY native python; $N32 converter dir.
set -u
OUT=results/n33; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1
run() { # tag input wout
  local t=$1 in=$2 w=$3 sha; sha=$(shasum -a 256 $in | cut -d' ' -f1)
  python3 $OUT/circular.py $in 0.4 $OUT/seed-$t.json
  $PY scripts/make_target_spec.py --target-id n33-$t.v0 --input $in --input-sha256 $sha --wout $w --vmecpp 0.8.0 \
     --seed-candidate $OUT/seed-$t.json --output $OUT/spec-$t > $OUT/spec-$t.log 2>&1 || { echo "$t spec failed"; return; }
  $PY scripts/fit_coils.py --target-spec $OUT/spec-$t/spec.json --wout $w --snapshot $OUT/spec-$t/seed.json \
     --output $PWD/$OUT/fit-$t --seconds 1800 --check-seconds 900 > $OUT/fit-$t.log 2>&1; echo "$t fit exit $?"
}
run sel401 evidence/plasma-balanced-v1/selected-input-401.json results/n18/selected401/wout.nc
run 60653 results/n32/row60653-input.json results/n32/wout-60653/wout.nc
for row in 2931 46244 23761; do
  in=$OUT/row$row-input.json; $PY $N32/make_input.py $N32/row$row.json $in
  sha=$(shasum -a 256 $in | cut -d' ' -f1)
  $PY scripts/make_wout.py --input $in --input-sha256 $sha --output $OUT/wout-$row > $OUT/wout-$row.log 2>&1 || { echo "$row wout failed"; continue; }
  run $row $in $OUT/wout-$row/wout.nc
done
