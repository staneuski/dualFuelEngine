#!/bin/sh
#*---------------------------------*- sh -*----------------------------------*#
# =========                 |                                                 #
# \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           #
#  \\    /   O peration     | Version:  6                                     #
#   \\  /    A nd           | Mail:     stas.stasheuski@gmail.com             #
#    \\/     M anipulation  |                                                 #
#*---------------------------------------------------------------------------*# 

# Скрипт для генерации сетки

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Копирование .stl файлов в mesh/ для генерации на их основе сетки
cp ../geometry/*.stl constant/triSurface

# Построение сетки
surfaceFeatureExtract
blockMesh
snappyHexMesh -overwrite

# Анализ сетки
printf 'Checking the mesh...\n\n'
checkMesh

echo -ne '\007' # звуковой сигнал при выполнении задачи






