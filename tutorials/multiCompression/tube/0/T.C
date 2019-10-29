/*--------------------------------*- C++ -*----------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: Addition to OpenFOAM v6
   \\    /   O peration     | Website:  https://github.com/StasF1/dualFuelEngine
    \\  /    A nd           | Version:  0.3-alpha
     \\/     M anipulation  |
\*---------------------------------------------------------------------------*/

#include "../constant/transportProperties.H"

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

// Get velocity field U
const fvPatchVectorField& U = patch().lookupPatchField<volVectorField, vector>("U");

scalar criticalSqrVelocity = 2*GAMMA/(GAMMA - 1)*R*TStagn;

operator ==
(
    TStagn*( 1 - (GAMMA - 1)/(GAMMA + 1)*magSqr(U)/criticalSqrVelocity )
);

// ************************************************************************* //
