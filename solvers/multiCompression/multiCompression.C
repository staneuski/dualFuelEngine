/*---------------------------------------------------------------------------*\
  =========					|
  \\	  /	 F ield			| OpenFOAM: Addition to OpenFOAM v6
   \\	 /	 O peration		| Website:	https://github.com/StasF1/dualFuelEngine
	\\	/	 A nd			| Copyright (C) 2019 Stanislau Stasheuski
	 \\/	 M anipulation	|
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
	multiCompression

Description
	v0.3-alpha

Comments

	fvc - явный метод,	 возвращает поле
	fvm - неявный метод, возвращает контрольно-объёмную матрицу

\*---------------------------------------------------------------------------*/

#include "fvCFD.H"
#include "simpleControl.H"
#include "fvOptions.H"

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

int main(int argc, char *argv[])
{
	#include "setRootCaseLists.H"
	#include "createTime.H"
	#include "createMesh.H"

	simpleControl simple(mesh);

	#include "createFields.H"

	// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

	Info<< "\nStarting time loop\n" << endl;

	while (simple.loop(runTime))
	{
		Info<< "Time = " << runTime.timeName() << nl << endl;

		#include "CourantNo.H"

        volScalarField pPrev(p);

		while (simple.correctNonOrthogonal())
		{

            #include "rhoEqn.H"

            // Because there isn't any equation for p, so under-relaxation is
            // done like that (per se this line is the same as pEqv.relax()):
            p =
            (
                p + 0.5*(p - pPrev)
            );

			fvVectorMatrix UEqn
			(
				fvm::ddt(rho, U)
			  + fvc::div(phi, U)
			 ==
			  - fvc::grad(p)
			  + fvc::grad
				(
					(MU/3)*fvc::div(U)
				)
			  + MU*fvc::laplacian(U)
			);

			UEqn.relax();
			UEqn.solve();
			
			fvScalarMatrix eEqn
			(
				fvm::ddt(rho, e)
			  + fvm::div(phi, e)
			 ==
			  - fvc::div(p*U)
			  + fvc::div(LAMBDA*fvc::grad(T))
              + (
                     U & (
                            MU*fvc::laplacian(U)
                          + fvc::grad(MU/3*fvc::div(U))
                         )
                )
              // + MU*D TODO
			);

			eEqn.relax();
			eEqn.solve();
			
			phi = fvc::flux(rho*U);

            T =
            (
                (e - magSqr(U)/2)
               /Cv
            );

			pPrev = p;
			p = rho*R*T;
			
			fvScalarMatrix alphaAirEqn
			(
				fvm::ddt(rho, alphaAir)
			  + fvm::div(phi, alphaAir)
			  - fvc::laplacian(DAir, rho*alphaAir)
			);

            // alphaAirEqn.relax(); //FIXME What are these lines (126 & 129) mean?
			fvOptions.constrain(alphaAirEqn);
			alphaAirEqn.solve();
            // fvOptions.correct(alphaAir);

			fvScalarMatrix alphaGasEqn
			(
				fvm::ddt(rho, alphaGas)
			  + fvm::div(phi, alphaGas)
			  - fvc::laplacian(DAir, rho*alphaGas)
			);

			fvOptions.constrain(alphaGasEqn);
			alphaGasEqn.solve();
		}
		
		alphaExh = dimensionedScalar("1", dimless, 1) - alphaGas - alphaAir;
		
		runTime.write();

		Info<< "ExecutionTime = " << runTime.elapsedCpuTime() << " s"
			<< "  ClockTime = " << runTime.elapsedClockTime() << " s"
			<< nl << endl;
	}

	Info<< "End\n" << endl;

}

// ************************************************************************* //
