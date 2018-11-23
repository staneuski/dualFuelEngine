/*---------------------------------------------------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     | Website:  https://openfoam.org
    \\  /    A nd           | Copyright (C) 2011-2018 OpenFOAM Foundation
     \\/     M anipulation  |
-------------------------------------------------------------------------------
License
    This file is part of OpenFOAM.

    OpenFOAM is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    OpenFOAM is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
    for more details.

    You should have received a copy of the GNU General Public License
    along with OpenFOAM.  If not, see <http://www.gnu.org/licenses/>.

Application
    multiCompression

Description
    Potential flow solver which solves for the velocity potential, to
    calculate the flux-field, from which the velocity field is obtained by
    reconstructing the flux.

    This application is particularly useful to generate starting fields for
    Navier-Stokes codes.

\*---------------------------------------------------------------------------*/

#include "fvCFD.H"
#include "pisoControl.H"
#include "simpleControl.H"
#include "fvOptions.H"

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

int main(int argc, char *argv[])
{
    argList::addOption
    (
        "pName",
        "pName",
        "Name of the pressure field"
    );

    argList::addBoolOption
    (
        "initialiseUBCs",
        "Initialise U boundary conditions"
    );

    argList::addBoolOption
    (
        "writePhi",
        "Write the velocity potential field"
    );

    argList::addBoolOption
    (
        "writep",
        "Calculate and write the pressure field"
    );

    argList::addBoolOption
    (
        "withFunctionObjects",
        "execute functionObjects"
    );

    #include "setRootCaseLists.H"
    #include "createTime.H"
    #include "createMesh.H"

	pisoControl multiCompression(mesh, "multiCompression");
	simpleControl temperatureField(mesh);
	

    #include "createFields.H"

    // * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

    Info<< nl << "Calculating potential flow" << endl;

    // Since solver contains no time loop it would never execute function objects so do it ourselves
    runTime.functionObjects().start();

    MRF.makeRelative(phi); // Работа для различных зон. MRF zone definition based on cell zone and parameters obtained from a control dictionary constructed from the given stream. The rotation of the MRF region is defined by an origin and axis of rotation and an angular speed.
    adjustPhi(phi, U, p); // For cases which do no have a pressure boundary adjust the balance of fluxes to obey continuity. Обеспечивает консервативность уравнений
	// ? - обеспечивает баланс ур-ний неразрывности при отсутствии ГУ по давлению


    // Non-orthogonal velocity potential corrector loop
    while (multiCompression.correctNonOrthogonal())
    {
		// Mass continuity for an incompressible fluid:	∇•U=0 | div(U) = 0 | du/dx+... = 0
		// Pressure equation for an incompressible, irrotational fluid assuming steady-state conditions: (∇^2)p = 0 | ∆p = 0 | d^2(p_x)/dx^2+... = 0 | laplacian(p) = 0
		// Phi - потенциал скорости (volScalarField): U = ∇•Phi | U = grad(Phi) | U = d(Phi)/dx*i+...
		// ? phi - скороcть, м/с (surfaceScalarField)
		fvScalarMatrix PhiEqn
        (
			// (∇^2)Phi = ∇(phi)
			
			// fvm - неявный метод/дискретизация, возвращает контрольно-объёмную матрицу
            fvm::laplacian(dimensionedScalar("1", dimless, 1), Phi)
         ==
			// fvc - явный метод/дискретизация, возвращает поле
			fvc::div(phi)
        );

        PhiEqn.setReference(PhiRefCell, PhiRefValue); // устанавливает настройки
	  	PhiEqn.solve(); // решает

        if (multiCompression.finalNonOrthogonalIter())
        {
            phi -= PhiEqn.flux(); // flux - поток
        }
		
        fvScalarMatrix TEqn
        (
            fvm::ddt(T)
          + fvm::div(phi, T)
          - fvm::laplacian(DT, T)
         ==
            fvOptions(T)
        );

        // TEqn.relax();
        // fvOptions.constrain(TEqn);
        TEqn.solve();
		fvOptions.correct(T);
    }

    MRF.makeAbsolute(phi);

    Info<< "Continuity error = "
        << mag(fvc::div(phi))().weightedAverage(mesh.V()).value()
        << endl;

    U = fvc::reconstruct(phi);
    U.correctBoundaryConditions();

    Info<< "Interpolated velocity error = "
        << (sqrt(sum(sqr(fvc::flux(U) - phi)))/sum(mesh.magSf())).value()
        << endl;

    // Write U
    U.write();
	
    // Optionally write Phi (if not it writes phi)
    if (args.optionFound("writePhi"))
    {
        Info<< nl << "Writing field Phi (grad(Phi) = U)" << endl;
		Phi.write();
    } else {
		Info<< nl << "Writing field phi" << endl;
		phi.write();
	}
	
	
    // Calculate the pressure field
    if (args.optionFound("writep"))
    {
        Info<< nl << "Calculating approximate pressure field" << endl;

        label pRefCell = 0;
        scalar pRefValue = 0.0;
        setRefCell
        (
            p,
            multiCompression.dict(),
            pRefCell,
            pRefValue
        );

        // Calculate the flow-direction filter tensor
        volScalarField magSqrU(magSqr(U));	// квадрат амплитуды веткторного поля |U|^2
        volSymmTensorField F(sqr(U)/(magSqrU + small*average(magSqrU))); // U^2 / (|U|^2 + 1e-06*<|U|^2>)

        // Calculate the divergence of the flow-direction filtered div(U*U)
        // Filtering with the flow-direction generates a more reasonable
        // pressure distribution in regions of high velocity gradient in the
        // direction of the flow
        volScalarField divDivUU
        (
            fvc::div
            (
                // & - понижение ранга тензора
				F & fvc::div(phi, U), // поток количества движения
                "div(div(phi,U))"
            )
        );

        // Solve a Poisson equation for the approximate pressure
        while (multiCompression.correctNonOrthogonal())
        {
            fvScalarMatrix pEqn
            (
                fvm::laplacian(p) + divDivUU
            );

            pEqn.setReference(pRefCell, pRefValue);
            pEqn.solve();
        }

        p.write();
    }
	
	// Calculating temperature field
	Info<< nl << "Calculating temperature field" << endl;
	
	// Non-orthogonal temperature corrector loop
    while (temperatureField.correctNonOrthogonal())
    {
        fvScalarMatrix TEqn
        (
            fvm::ddt(T)
          + fvm::div(phi, T)
          - fvm::laplacian(DT, T)
         ==
            fvOptions(T)
        );

        TEqn.relax();
        fvOptions.constrain(TEqn);
        TEqn.solve();
		fvOptions.correct(T);
    }
	
	// Write T
    T.write();
	
    runTime.functionObjects().end();

    Info<< "ExecutionTime = " << runTime.elapsedCpuTime() << " s"
        << "  ClockTime = " << runTime.elapsedClockTime() << " s"
        << nl << endl;

    Info<< "End\n" << endl;

	// F.write();
    return 0;
}


// ************************************************************************* //
