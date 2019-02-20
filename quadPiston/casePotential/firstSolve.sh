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
#     Скрипт для запуска расчёта при использовании настроек из ../case
#
#-----------------------------------------------------------------------------# 

# Копирование файлов сетки
mkdir -p constant/
cp -r ../mesh/constant/polyMesh constant/polyMesh

# Копирование граничных условий из проекта с модифицированным ядром
mkdir -p 0/
cp -r ../case/0/p.orig 0
cp -r ../case/0/U.orig 0

# Копирование файлов system
cp -r ../case/system/controlDict system
sed -i "s/multiCompression/potentialFoam/g" system/controlDict
cp -r ../case/system/fvSolution system
sed -i "s/multiCompression/potentialFlow/g" system/fvSolution

# Запуск расчёта
potentialFoam -writePhi -writep | tee case.log

# Перемещение файлов расчёта в папку 1 для возможности открытия в solved.foam
mkdir -p 1/
mv 0/U 1
mv 0/p 1
mv 0/phi 1
mv 0/Phi 1


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
echo -ne '\007' # звуковой сигнал при выполнении задачи






