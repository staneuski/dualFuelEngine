#!/bin/bash
#------------------------------------------------------------------------------
# =========                 |
# \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
#  \\    /   O peration     | Website:  https://github.com/StasF1
#   \\  /    A nd           | Copyright (C) 2017 OpenFOAM Foundation
#    \\/     M anipulation  |
#------------------------------------------------------------------------------
# Script
#     Allrun
#
# Description
#     Generates mesh and run all cases using the multiCompression solver
#
#------------------------------------------------------------------------------

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #

startProjectTime=`date +%s` # Включение секундомера для вывода времени расчёта

# Масштабирование файлов .stl
cd geometry
printf 'Running surfaceTransformPoints (scaling .stl files) on %s\n' "${PWD}"
sh scaleSTL.sh > scaleSTL.log

# Построение сетки
cd ../mesh
printf 'Running snappyHexMesh on %s\n' "${PWD}"
sh remesh.sh > mesh.log

# Решение проекта на собственном ядре
cd ../case
printf 'Running multiCompression on %s\n' "${PWD}"
# sh firstRun.sh > case.log
sh hardResolve.sh > case.log

# Решение проекта для сравнения результатов c potentialFoam'ом
cd ../casePotential
printf 'Running potentialFoam on %s\n' "${PWD}"
# sh firstRun.sh > case.log
sh hardResolve.sh > case.log

# Решение проекта для сравнения результатов со scalarTransportFoam'ом
cd ../caseScalar
printf 'Running scalarTransportFoam on %s\n' "${PWD}"
# sh firstRun.sh > case.log
sh hardResolve.sh > case.log

# Отображение времени расчёта проекта
cd ../
endProjectTime=`date +%s`
solveProjectTime=$((endProjectTime-startProjectTime))
printf '\nCalculation time: %dh:%dm:%ds\n'\
	 $(($solveProjectTime/3600)) $(($solveProjectTime%3600/60)) $(($solveProjectTime%60))

echo -ne '\007' # звуковой сигнал

# ***************************************************************************** #

