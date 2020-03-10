/*---------------------------------------------------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: dualFuelEngline addition to OpenFOAM v7
   \\    /   O peration     | Website:  https://github.com/StasF1/dualFuelEngine
    \\  /    A nd           | Copyright (C) 2018-2020 Stanislau Stasheuski
     \\/     M anipulation  |
-------------------------------------------------------------------------------
License
    This file is not part of OpenFOAM, but part of dualFuelEngine – OpenFOAM
    addition.

    dualFuelEngine (like OpenFOAM) is free software: you can redistribute it 
    and/or modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation, either version 3 of the License,
    or (at your option) any later version.

    dualFuelEngine (like OpenFOAM) is distributed in the hope that it will be
    useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this repository. If not, see <http://www.gnu.org/licenses/>.

File
    T.C

Description
    Set temperature BC using inlet velocity and gas dynamic functions with
    codedFixedValue BC type

\*---------------------------------------------------------------------------*/

// Get velocity field U
const fvPatchVectorField& U = patch().lookupPatchField<volVectorField, vector>("U");

double criticalSqrVelocity =
(
    2*GAMMA/(GAMMA - 1)*R*TStagn
);

operator ==
(
    TStagn*( 1 - (GAMMA - 1)/(GAMMA + 1)*magSqr(U)/criticalSqrVelocity )
);

// ************************************************************************* //
