#!/bin/bash
# N45: same intake/seed/fit recipe as N33; serial. Repository root (worktree at upstream main). $PY native python; $N45 log dir.
set -u
OUT=results/n45; mkdir -p $OUT; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1
run() { # tag input wout
  local t=$1 in=$2 w=$3 sha; sha=$(shasum -a 256 $in | cut -d' ' -f1)
  $PY $N45/circular.py $in 0.4 $OUT/seed-$t.json
  $PY scripts/make_target_spec.py --target-id n45-$t.v0 --input $in --input-sha256 $sha --wout $w --vmecpp 0.8.0 \
     --seed-candidate $OUT/seed-$t.json --output $OUT/spec-$t > $OUT/spec-$t.log 2>&1 || { echo "$t spec failed"; return; }
  echo "$t fit start $(date -u +%FT%TZ)"
  $PY scripts/fit_coils.py --target-spec $OUT/spec-$t/spec.json --wout $w --snapshot $OUT/spec-$t/seed.json \
     --output $PWD/$OUT/fit-$t --seconds 1800 --check-seconds 900 > $OUT/fit-$t.log 2>&1; echo "$t fit exit $? $(date -u +%FT%TZ)"
}
intake() { # tag input-json(raw dataset row or registered input) ; prints wout path
  local t=$1 in=$2 sha; sha=$(shasum -a 256 $in | cut -d' ' -f1)
  $PY scripts/make_wout.py --input $in --input-sha256 $sha --output $OUT/wout-$t > $OUT/wout-$t.log 2>&1 || { echo "$t wout failed"; return 1; }
}
# control first
intake sel401 evidence/plasma-balanced-v1/selected-input-401.json && run sel401 evidence/plasma-balanced-v1/selected-input-401.json $OUT/wout-sel401/wout.nc
for f in $OUT/rows/row*.json; do
  row=$(basename $f .json | sed 's/row//'); in=$OUT/row$row-input.json
  $PY $N45/make_input.py $f $in
  intake $row $in && run $row $in $OUT/wout-$row/wout.nc
done
echo "pipeline done $(date -u +%FT%TZ)"
