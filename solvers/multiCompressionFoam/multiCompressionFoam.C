/*---------------------------------------------------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: dualFuelEngline addition to OpenFOAM v7
   \\    /   O peration     | Website:  https://github.com/StasF1/dualFuelEngine
    \\  /    A nd           | Copyright (C) 2018-2020 Stanislau Stasheuski
     \\/     M anipulation  |
-------------------------------------------------------------------------------
License
    This file is of dualFuelEngine – OpenFOAM addition.

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
    multiCompressionFoam

Description
    Density-based phenomenological multicomponent compressible flow solver
    (multiCompressionFoam stands for multicomponent compressible flow).

    v0.4.9-alpha

\*---------------------------------------------------------------------------*/

#include "fvCFD.H"
#include "dynamicFvMesh.H"
#include "fluidThermo.H"
#include "pimpleControl.H"
#include "fvOptions.H"

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

int main(int argc, char *argv[])
{
    #include "setRootCaseLists.H"
    #include "createTime.H"
    #include "createDynamicFvMesh.H"
    #include "createDyMControls.H"
    #include "createFields.H"
    #include "createFieldRefs.H"

    // * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

    Info<< "\nStarting time loop\n" << endl;

    while (pimple.run(runTime))
    {
        #include "readDyMControls.H"
        #include "compressibleCourantNo.H"
        #include "setDeltaT.H"

        runTime++;

        Info<< "Time = " << runTime.timeName() << nl << endl;

        mesh.update();

        phi = fvc::flux(rho*U);

        if (mesh.moving())
        {
            // Make flux relative to the mesh-motion
            phi = fvc::relative(phi, rho, U);

            if (checkMeshCourantNo)
            {
                #include "meshCourantNo.H"
            }
        }

        while (pimple.loop())
        {
            #include "rhoEqn.H"

            // Explicitly relax pressure for UEqn
            p.relax();

            fvVectorMatrix UEqn
            (
                fvm::ddt(rho, U) + fvc::div(phi, U)
             ==
              - fvc::grad(p)
              + fvc::grad
                (
                    (mu/3)*fvc::div(U)
                )
              + mu*fvc::laplacian(U)
            );

            UEqn.relax();
            UEqn.solve();

            fvOptions.correct(U);
            K = 0.5*magSqr(U);

            fvScalarMatrix EEqn
            (
                fvm::ddt(rho, e) + fvm::div(phi, e)
              + fvc::ddt(rho, K) + fvc::div(phi, K)
              + fvc::div
                (
                    fvc::absolute(phi/fvc::interpolate(rho), U),
                    p,
                    "div(phiv,p)"
                )
            );

            EEqn.relax();
            EEqn.solve();

            fvOptions.correct(e);

            // Upgrade temperature using internal energy field
            thermo.correct();

            p = rho/psi;
            p.correctBoundaryConditions();
        }

        // --- Solve concentrations
        solve
        (
            fvm::ddt(rho, alphaAir)
          + fvm::div(phi, alphaAir)
          - fvc::laplacian(DAir, rho*alphaAir)
        );

        solve
        (
            fvm::ddt(rho, alphaGas)
          + fvm::div(phi, alphaGas)
          - fvc::laplacian(DGas, rho*alphaGas)
        );

        alphaExh = dimensionedScalar("1", dimless, 1) - alphaGas - alphaAir;

        runTime.write();

        Info<< "ExecutionTime = " << runTime.elapsedCpuTime() << " s"
            << "  ClockTime = " << runTime.elapsedClockTime() << " s"
            << nl << endl;
    }

    Info<< "End\n" << endl;
}

// ************************************************************************* //
