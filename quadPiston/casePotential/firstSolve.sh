#!/bin/sh
#*---------------------------------*- sh -*----------------------------------*#
# =========                 |                                                 #
# \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           #
#  \\    /   O peration     | Version:  6                                     #
#   \\  /    A nd           | Mail:     stas.stasheuski@gmail.com             #
#    \\/     M anipulation  |                                                 #
#*---------------------------------------------------------------------------*#

# Скрипт для запуска расчёта

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Копирование файлов сетки
mkdir -p constant
cp -r ../mesh/constant/polyMesh constant/polyMesh

# Копирование граничных условий из проекта с модифицированным ядром
mkdir -p 0
cp -r ../case/0/p.orig 0
cp -r ../case/0/U.orig 0

# Запуск расчёта
potentialFoam -writePhi -writep | tee case.log

# Перемещение файлов расчёта в папку 1 для возможности открытия в solved.foam
mkdir -p 1
mv 0/U 1
mv 0/p 1
mv 0/phi 1


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
echo -ne '\007' # звуковой сигнал при выполнении задачи






