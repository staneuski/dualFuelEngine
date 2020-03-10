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
    U.C

Description
    Calculation inlet velocity with Newton iteration method by
    codedFixedValue BC type throught mass gas flow and using gas dynamic
    functions.

\*---------------------------------------------------------------------------*/

#include <math.h> /* sqrt */

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

// Get patches & fields
// ~~~~~~~~~~~~~~~~~~~~
//- Patches
const fvPatch& boundaryPatch = patch();
const vectorField& Cf = boundaryPatch.Cf(); // face centroid field
vectorField& field = *this;

//- Fields
double p = /* convert fvPatchScalarField p to double by averaging the field */
gAverage(
    patch().lookupPatchField<volScalarField, scalar>("p")
);


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

// Without p convertion set type of eqvConstant as:
// const Foam::tmp<Foam::Field<double>>&
double eqvConstant =
(
    m*p/sqrt(TStagn)
   *pow(
        (GAMMA + 1)/2*(1 - (GAMMA - 1)/(GAMMA + 1)),
        1/(GAMMA - 1)
    )
);

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

// Finding the lambda with gas dynamic functions by Newton method
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
double lambda0 = 1;

double lambda1 =/* initial residual */
(
    lambda0
  - (
        G - eqvConstant*pow(lambda0, GAMMA/(GAMMA - 1)) /* f(lambda) */
    )
   /(
      - eqvConstant*GAMMA/(GAMMA - 1)*pow(lambda0, 1/(GAMMA - 1)) /* f'(lambda) */
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
            G - eqvConstant*pow(lambda1, GAMMA/(GAMMA - 1)) /* f(lambda) */
        )
       /(
          - eqvConstant*GAMMA/(GAMMA - 1)*pow(lambda1, 1/(GAMMA - 1)) /* f'(lambda) */
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
    field[faceI] = vector
    (
        lambda1*criticalVelocity*directionU.x(),
        lambda1*criticalVelocity*directionU.y(),
        lambda1*criticalVelocity*directionU.z()
    );
}

// ************************************************************************* //
