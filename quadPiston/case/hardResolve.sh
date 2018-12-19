#!/bin/sh
#-----------------------------------------------------------------------------#
# =========                 |
# \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
#  \\    /   O peration     | Website:  https://github.com/StasF1
#   \\  /    A nd           | Version:  6
#    \\/     M anipulation  |
#------------------------------------------------------------------------------
# Script
#     hardResolve
#
# Description
#     Скрипт для перезапуска расчёта
#
#-----------------------------------------------------------------------------#

# Удаление cтарых результатов расчёта
rm -r 1

# Копирование файлов начальных условий без изменений из папки Orig
# cp -r 0/Orig/*.orig 0/

# Копирование файлов сетки
cp -r ../mesh/constant/polyMesh constant

# Укрупнение сетки
refineMesh -overwrite | tee case.log

# Запуск расчёта и запись постпроцессинга
multiCompression -writep -writePhi -writedivphi | tee -a case.log

# Конвертировние и операции для просмотра решённой задачи
# foamToVTK | tee -a case.log # конвертирование решенной задачи в формат VTK

# Перемещение файлов расчёта в папку 1 для возможности открытия в solved.foam
mkdir -p 1
mv 0/U 1
mv 0/p 1
mv 0/phi 1
mv 0/T 1
mv 0/div\(phi\) 1


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
echo -ne '\007' # звуковой сигнал при выполнении задачи




