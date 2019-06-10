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

Application
    testFoam

Description
    Solves the steady or transient transport equation for a passive scalar.

\*---------------------------------------------------------------------------*/

#include "fvCFD.H"
#include "simpleControl.H"

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

int main(int argc, char *argv[])
{
    #include "setRootCaseLists.H"
    #include "createTime.H"
    #include "createMesh.H"

	simpleControl simple(mesh);
	
    #include "createFields.H"

    // * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

	wordList XBCTypes
	(
	    rho.boundaryField().size(),
	    zeroGradientFvPatchScalarField::typeName
	);
	
	volScalarField X
	(
	    IOobject
	    (
	        "X",
	        runTime.timeName(),
	        mesh,
	        IOobject::NO_READ,
	        IOobject::AUTO_WRITE
	    ),
	    rho*mag(U),
	    XBCTypes
	);

	while (simple.loop(runTime))
	{

		fvScalarMatrix XEqn
        (
            fvm::ddt(X)
		  + fvc::div(phi, X)
		);
		
        XEqn.relax();
        XEqn.solve();
		
		// X.write();
		runTime.write();
	}

    Info<< "End\n" << endl;

    return 0;
}


// ************************************************************************* //
