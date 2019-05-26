#!/bin/sh
#-----------------------------------------------------------------------------#
# =========                 |
# \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
#  \\    /   O peration     | Website:  https://github.com/StasF1
#   \\  /    A nd           | Version:  6
#    \\/     M anipulation  |
#------------------------------------------------------------------------------
# Script
#     firstSolve
#
# Description
#     Масштабирование файлов из мм в м и выставление хода клапана в 25 мм
#
#-----------------------------------------------------------------------------#

# Указание пути к файлам .stl для их копирования
cp -r ../../../doc/CATIA/quadPiston/*.stl ./

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #

# Inlet
export FILE="injectionXMinus.stl"
surfaceTransformPoints -scale '(0.001 0.001 0.001)' $FILE $FILE | tee scaleSTL.log
export FILE="injectionXPlus.stl"
surfaceTransformPoints -scale '(0.001 0.001 0.001)' $FILE $FILE | tee -a scaleSTL.log
export FILE="injectionYMinus.stl"
surfaceTransformPoints -scale '(0.001 0.001 0.001)' $FILE $FILE | tee -a scaleSTL.log
export FILE="injectionYPlus.stl"
surfaceTransformPoints -scale '(0.001 0.001 0.001)' $FILE $FILE | tee -a scaleSTL.log

# Injection
export FILE="inletXMinus.stl"
surfaceTransformPoints -scale '(0.001 0.001 0.001)' $FILE $FILE | tee -a scaleSTL.log
export FILE="inletXPlus.stl"
surfaceTransformPoints -scale '(0.001 0.001 0.001)' $FILE $FILE | tee -a scaleSTL.log
export FILE="inletYMinus.stl"
surfaceTransformPoints -scale '(0.001 0.001 0.001)' $FILE $FILE | tee -a scaleSTL.log
export FILE="inletYPlus.stl"
surfaceTransformPoints -scale '(0.001 0.001 0.001)' $FILE $FILE | tee -a scaleSTL.log

# Other
export FILE="outlet.stl"
surfaceTransformPoints -scale '(0.001 0.001 0.001)' $FILE $FILE | tee -a scaleSTL.log
export FILE="valve.stl"
surfaceTransformPoints -scale '(0.001 0.001 0.001)' $FILE $FILE | tee -a scaleSTL.log
export FILE="valve.stl"
surfaceTransformPoints -translate '(0 0 -0.25)' $FILE $FILE | tee -a scaleSTL.log
export FILE="walls.stl"
surfaceTransformPoints -scale '(0.001 0.001 0.001)' $FILE $FILE | tee -a scaleSTL.log

# *************************************************************************** #