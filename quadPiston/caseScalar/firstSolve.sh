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
#     Скрипт для запуска расчёта
#
#-----------------------------------------------------------------------------#

# Копирование файлов сетки и постоянных
mkdir -p constant
cp -r ../case/constant/transportProperties constant
cp -r ../mesh/constant/polyMesh constant/polyMesh

# Копирование граничных условий из проекта с модифицированным ядром
mkdir -p 0
cp -r ../case/0/T.orig 0
cp -r ../case/1/U 0

# Копирование файлов system из проекта с модифицированным ядром
cp -r ../case/system/controlDict system
cp -r ../case/system/fvSolution system
cp -r ../case/system/fvSchemes system
sed -i "s/multiCompression/scalarTransportFoam/g" system/controlDict

# Запуск расчёта
scalarTransportFoam | tee case.log


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
echo -ne '\007' # звуковой сигнал при выполнении задачи






