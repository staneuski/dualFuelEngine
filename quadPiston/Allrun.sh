#!/bin/bash

# ------------------------------------ Data -------------------------------- #

# Указать путь к файлам .stl в скрипте scaleSTL.sh для их последующего 
# масштабирования в geometry/


# -------------------------------------------------------------------------- #



# [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[ Script ]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]] #

startProjectTime=`date +%s` # Включение секундомера для вывода времени расчёта


## Масштабирование файлов .stl
printf 'Scaling .stl files...'
cd geometry
sh scaleSTL.sh > scaleSTL.log 
printf '\nScaling *.stl files has being DONE.'
printf '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n'


## Построение сетки
printf 'Meshing...'
cd ../mesh
sh firstMesh.sh > mesh.log 
printf '\nThe mesh has being DONE.'
printf '\n~~~~~~~~~~~~~~~~~~~~~~~~\n\n'


## Решение проекта
printf 'Solving the case...'
cd ../case
# sh firstRun.sh > case.log
sh hardResolve.sh > case.log
printf '\nThe case has being SOLVED.'
printf '\n~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n'

## Решение проекта для сравнения результатов
printf 'Solving the compared case...'
cd ../caseToCompare
# sh firstRun.sh > case.log
sh hardResolve.sh > case.log
printf '\nThe compared case has being SOLVED.'
printf '\n~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n'


## Вывод времени расчёта проекта в терминал и сигнал о завершении расчёта
cd ../
endProjectTime=`date +%s`
solveProjectTime=$((endProjectTime-startProjectTime))
printf '#######################\n'
printf 'Solve time: %dh:%dm:%ds\n' $(($solveProjectTime/3600)) $(($solveProjectTime%3600/60)) $(($solveProjectTime%60))
echo -ne '\007' # звуковой сигнал

