#!/bin/sh
#*---------------------------------*- sh -*----------------------------------*#
# =========                 |                                                 #
# \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           #
#  \\    /   O peration     | Version:  6                                     #
#   \\  /    A nd           | Mail:     stas.stasheuski@gmail.com             #
#    \\/     M anipulation  |                                                 #
#*---------------------------------------------------------------------------*# 

# Скрипт для регенерации сетки

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Перезапись .stl файлов в mesh/constant/triSurface/
rm -r constant/extendedFeatureEdgeMesh
rm -r constant/triSurface/*
rm -r constant/polyMesh

# Регенерация сетки
sh firstMesh.sh | tee mesh.log








