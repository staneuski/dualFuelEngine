#!/bin/sh
#*---------------------------------*- sh -*----------------------------------*#
# =========                 |                                                 #
# \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           #
#  \\    /   O peration     | Version:  5                                     #
#   \\  /    A nd           | Mail:     stas.stasheuski@gmail.com             #
#    \\/     M anipulation  |                                                 #
#*---------------------------------------------------------------------------*#

# Скрипт для перезапуска расчёта

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Удаление cтарых результатов расчёта
rm -r 1

# Копирование граничных условий (и проч.) из проекта с модифицированным ядром
cp -r ../case/0/T.orig 0
cp -r ../case/1/U 0
cp -r ../case/1/transportProperties constant

# Копирование файлов сетки
cp -r ../mesh/constant/polyMesh constant

# Укрупнение сетки
# refineMesh -overwrite | tee case.log

# Запуск расчёта и запись постпроцессинга
scalarTransportFoam | tee -a case.log


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
echo -ne '\007' # звуковой сигнал при выполнении задачи




