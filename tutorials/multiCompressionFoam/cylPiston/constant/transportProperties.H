/*--------------------------------*- C++ -*----------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: dualFuelEngline addition to OpenFOAM v7
   \\    /   O peration     | Website:  https://github.com/StasF1/dualFuelEngine
    \\  /    A nd           | Version:  0.3-alpha
     \\/     M anipulation  |
-------------------------------------------------------------------------------

Description
    Mirror of the transportProperties dictionary for calculated BCs

\*---------------------------------------------------------------------------*/

#define GAMMA 1.4 /* [dimensionless] heat capacity ratio */

#define R 287.3 /* [J/kg/K] gas constant */

#define TStagn 293.15 /* [K] stagnation temperature */

#define G 168//60/0.6 /* [kg/s/m^2] mass flow rate to area relation */

#define tolerance 1e-03 /* tolerance & initial residual */

// ************************************************************************* //