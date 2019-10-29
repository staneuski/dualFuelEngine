/*--------------------------------*- C++ -*----------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: Addition to OpenFOAM v6
   \\    /   O peration     | Website:  https://github.com/StasF1/dualFuelEngine
    \\  /    A nd           | Version:  0.3-alpha
     \\/     M anipulation  |
\*---------------------------------------------------------------------------*/

#include "../constant/transportProperties.H"

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

// Get density & temperature fields
const fvPatchScalarField& p = patch().lookupPatchField<volScalarField, scalar>("p");
const fvPatchField& T = patch().lookupPatchField<volScalarField, scalar>("T");

operator ==
(
    p/R/T
);

// ************************************************************************* //
