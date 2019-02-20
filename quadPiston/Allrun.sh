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

#
# # Масштабирование файлов .stl
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~
# printf 'Scaling .stl files...\n'
# cd geometry
# sh scaleSTL.sh > scaleSTL.log
# printf '\nScaling *.stl files has being DONE.\n'
# printf '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n'
#
#
# # Построение сетки
# # ~~~~~~~~~~~~~~~~
# printf 'Meshing...\n'
# cd ../mesh
# sh firstMesh.sh > mesh.log
# printf '\nThe mesh has being DONE.\n'
# printf '~~~~~~~~~~~~~~~~~~~~~~~~\n\n'
#

# Решение проекта на собственном ядре
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
printf 'Solving the case...\n'
cd ../case
# sh firstRun.sh > case.log
sh hardResolve.sh > case.log
printf '\nThe case has being SOLVED.\n'
printf '~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n'


# Решение проекта для сравнения результатов c potentialFoam'ом
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
printf 'Solving the comparing potentialFoam case...\n'
cd ../casePotential
# sh firstRun.sh > case.log
sh hardResolve.sh > case.log
printf '\nThe comparing potentialFoam case has being SOLVED.\n'
printf '~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n'


# Решение проекта для сравнения результатов со scalarTransportFoam'ом
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
printf 'Solving the comparing scalarTransportFoam case...\n'
cd ../caseScalar
# sh firstRun.sh > case.log
sh hardResolve.sh > case.log
printf '\nThe comparing scalarTransportFoam case has being SOLVED.\n'
printf '~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n'


# Отображение времени расчёта проекта
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
cd ../
endProjectTime=`date +%s`
solveProjectTime=$((endProjectTime-startProjectTime))
printf '***********************\n'
printf 'Solve time: %dh:%dm:%ds\n'\
	 $(($solveProjectTime/3600)) $(($solveProjectTime%3600/60)) $(($solveProjectTime%60))

echo -ne '\007' # звуковой сигнал

# ***************************************************************************** #

