/*---------------------------------------------------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: Addition to OpenFOAM v6
   \\    /   O peration     | Website:  https://github.com/StasF1/dualFuelEngine
    \\  /    A nd           | Copyright (C) 2019 Stanislau Stasheuski
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
    U.C

Description
    Calculation inlet velocity with Newton iteration method by
    codedFixedValue BC type throught mass gas flow and using gas dynamic
    functions.

\*---------------------------------------------------------------------------*/

#include <math.h> /* sqrt */

#include "../../constant/transportProperties.H" /* get variables */

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

// Get patches & fields
// ~~~~~~~~~~~~~~~~~~~~
//- Patches
const fvPatch& boundaryPatch = patch();
const vectorField& Cf = boundaryPatch.Cf();
vectorField& field = *this;

//- Fields
// const fvPatchScalarField& p = patch().lookupPatchField<volScalarField, scalar>("p");
#define p 101325*3.632 /* [Pa] static pressure */


// Variables reinitialisation
// ~~~~~~~~~~~~~~~~~~~~~~~~~~
double m =
sqrt(
    pow(2*GAMMA/(GAMMA + 1), (GAMMA + 1)/(GAMMA - 1))
   *GAMMA/R
);

double criticalVelocity =
sqrt(
    2*GAMMA/(GAMMA + 1)*R*TStagn
);

double constant =
(
    m*p/sqrt(TStagn) /*FIXME can't initialise p (which type is fvPatchScalarField) to double*/
   *pow(
        (GAMMA + 1)/2*(1 - (GAMMA - 1)/(GAMMA + 1)),
        1/(GAMMA - 1)
    )
);

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

// Finding the lambda with gas dynamic functions by Newton method
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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


// Initilise found velocity to patch
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
forAll(Cf, faceI)
{
    field[faceI] = vector(0, lambda1*criticalVelocity, 0);
}

// ************************************************************************* //
