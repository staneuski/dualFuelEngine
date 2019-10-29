/*--------------------------------*- C++ -*----------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: Addition to OpenFOAM v6
   \\    /   O peration     | Website:  https://github.com/StasF1/dualFuelEngine
    \\  /    A nd           | Version:  0.3-alpha
     \\/     M anipulation  |
\*---------------------------------------------------------------------------*/

#include <math.h> /* sqrt */

#include "../constant/transportProperties.H"

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

// Get patches & fields
// ~~~~~~~~~~~~~~~~~~~~
const fvPatch& boundaryPatch = patch();
const vectorField& Cf = boundaryPatch.Cf();
vectorField& field = *this;

#define p 101325*3.632 /* [Pa] static pressure */

// Variables reinitialisation
// ~~~~~~~~~~~~~~~~~~~~~~~~~~
double m =
    sqrt(
        pow(2*GAMMA/(GAMMA + 1), (GAMMA + 1)/(GAMMA - 1))
       *GAMMA/R
    );

double criticalVelocity =
    sqrt(2*GAMMA/(GAMMA + 1)*R*TStagn);

double constant =
    (
        m*p/sqrt(TStagn)
       *pow(
            (GAMMA + 1)/2*(1 - (GAMMA - 1)/(GAMMA + 1)),
            1/(GAMMA - 1)
        )
    );

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

double lambda0 = tolerance;

double lambda1 = /* initial residual */
(
    lambda0
  - (
        G - constant*pow(lambda0, GAMMA/(GAMMA - 1)) /* f(lambda) */
    )
   /(
      - constant*GAMMA/(GAMMA - 1)*pow(lambda0, 1/(GAMMA - 1)) /* f'(lambda) */
    )
);

int counter = 1; // iteration counter

Info << "Newton:  Solving for lambda, Initial residual = " << lambda1;

while (fabs(lambda1 - lambda0) > tolerance)
{
    
    lambda0 = lambda1;
    
    lambda1 =
    (
        lambda1
      - (
            G - constant*pow(lambda1, GAMMA/(GAMMA - 1)) /* f(lambda) */
        )
       /(
          - constant*GAMMA/(GAMMA - 1)*pow(lambda1, 1/(GAMMA - 1)) /* f'(lambda) */
        )
    );
    
    counter++;
}

Info << ", Final residual = " << lambda1
     << ", No Iterations " << counter
     << endl;

forAll(Cf, faceI)
{
	field[faceI] = vector(0, lambda1*criticalVelocity, 0);
}

// ************************************************************************* //
