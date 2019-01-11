# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# =========                 |
# \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
#  \\    /   O peration     | Website:  https://github.com/StasF1
#   \\  /    A nd           | Copyright (C) 2017 OpenFOAM Foundation
#    \\/     M anipulation  |
#------------------------------------------------------------------------------
# Script
#     differenceFilter
#
# Description
#     Python scipt to execute it from in the ParaView using the
#     ProgrammableFilter to compare miltiCompresion result with other solvers 
#     results
# 
#------------------------------------------------------------------------------

# Difference between Phi
# Cell data
phiCell_0 = inputs[0].CellData['Phi']
phiCell_1 = inputs[1].CellData['Phi']
output.CellData.append(phiCell_1 - phiCell_0, '∆Phi')
# Point data
phiPoint_0 = inputs[0].PointData['Phi']
phiPoint_1 = inputs[1].PointData['Phi']
output.PointData.append(phiPoint_1 - phiPoint_0, '∆Phi')

# Difference between p
# Cell data
pCell_0 = inputs[0].CellData['p']
pCell_1 = inputs[1].CellData['p']
output.CellData.append(pCell_1 - pCell_0, '∆p')
# Point data
pPoint_0 = inputs[0].PointData['p']
pPoint_1 = inputs[1].PointData['p']
output.PointData.append(pPoint_1 - pPoint_0, '∆p')

# Difference between U
# Cell data
UCell_0 = inputs[0].CellData['U']
UCell_1 = inputs[1].CellData['U']
output.CellData.append(UCell_1 - UCell_0, '∆U')
# Point data
UPoint_0 = inputs[0].PointData['U']
UPoint_1 = inputs[1].PointData['U']
output.PointData.append(UPoint_1 - UPoint_0, '∆U')

# Difference between T
# Cell data
TCell_0 = inputs[0].CellData['T']
TCell_2 = inputs[2].CellData['T']
output.CellData.append(TCell_2 - TCell_0, '∆T')
# Point data
TPoint_0 = inputs[0].PointData['T']
TPoint_2 = inputs[2].PointData['T']
output.PointData.append(TPoint_2 - TPoint_0, '∆T')

