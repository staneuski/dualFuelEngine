#!/bin/sh
# Recompilates solver and resolves the case

# Recompilation
cd ../../multicompCompressFluid
wmake #| tee ../quadPiston/case/wmake.log

# Resolving the case 
cd -
sh resolve.sh




