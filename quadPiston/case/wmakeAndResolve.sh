#!/bin/sh
#-----------------------------------------------------------------------------#
# =========                 |
# \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
#  \\    /   O peration     | Website:  https://github.com/StasF1
#   \\  /    A nd           | Version:  6
#    \\/     M anipulation  |
#------------------------------------------------------------------------------
# Script
#     wmakeAndResolve
#
# Description
#     Recompilates solver and resolves the case
#
#-----------------------------------------------------------------------------# 

# Recompilation
cd ../../multiCompression
wmake #| tee ../quadPiston/case/wmake.log

# Resolving the case 
cd -
sh resolve.sh




