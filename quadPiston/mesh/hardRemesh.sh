#!/bin/sh
#*---------------------------------*- sh -*----------------------------------*#
# =========                 |                                                 #
# \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           #
#  \\    /   O peration     | Version:  6                                     #
#   \\  /    A nd           | Mail:     stas.stasheuski@gmail.com             #
#    \\/     M anipulation  |                                                 #
#*---------------------------------------------------------------------------*#

# Скрипт для генерации сетки заново с копированием файлов геометрии

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Удаление всех файлов созданных при предыдущем разбиении сетки
rm -r constant/extendedFeatureEdgeMesh 
rm -r constant/polyMesh
rm -r constant/triSurface/*
rm -r ../geometry/*.stl

# Копирование .stl файлов и их масштабирование
cp ../geometry/CATIA/*.stl ../geometry/
cd ../geometry/
sh scaleSTL.sh | tee scaleSTL.log

# Регенерация сетки с нуля
cd -
sh firstMesh.sh | tee mesh.log
