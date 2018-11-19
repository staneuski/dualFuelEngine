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
if [! -d "$constant" ]; then
	mkdir constant
fi
cp -r ../mesh/constant/polyMesh constant

# Копирование граничных условий из проекта с модифицированным ядром
cp -r ../case/0/T.orig 0
cp -r ../case/1/U 0
cp -r ../case/1/transportProperties constant

# Запуск расчёта
scalarTransportFoam


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
echo -ne '\007' # звуковой сигнал при выполнении задачи






