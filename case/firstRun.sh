#!/bin/sh
#*---------------------------------*- sh -*----------------------------------*#
# =========                 |                                                 #
# \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           #
#  \\    /   O peration     | Version:  6                                     #
#   \\  /    A nd           | Mail:     stas.stasheuski@gmail.com             #
#    \\/     M anipulation  |                                                 #
#*---------------------------------------------------------------------------*#

# Скрипт для запуска расчёта

# Копирование файлов сетки
cp -r ../mesh/constant/polyMesh constant

# Запуск расчёта
potentialFoam
# multicompCompressFluid

foamToVTK # конвертирование решенной задачи в формат VTK

echo -ne '\007' # звуковой сигнал при выполнении задачи
