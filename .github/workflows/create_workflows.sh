#!/bin/sh
cd ${0%/*} || exit 1    # Run from this directory

solvers=("cylCyclic2D" "pipeCompression" "tubePurging")

for solver in "${solvers[@]}"; do
    sed "s/shockTube/$solver/g" shockTube.yml > $solver.yml
done