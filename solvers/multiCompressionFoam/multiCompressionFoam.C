/*---------------------------------------------------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: Addition to OpenFOAM v6
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
    v0.4-alpha

Comments
    Phenomenological multicomponent compressible solver (multiCompressionFoam
    stands for multicomponent compressible flow).

\*---------------------------------------------------------------------------*/

#include "fvCFD.H"
#include "dynamicFvMesh.H" // DyM
#include "fluidThermo.H"
#include "pimpleControl.H"
#include "CorrectPhi.H" // DyM
#include "fvOptions.H"

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

int main(int argc, char *argv[])
{
    #include "setRootCaseLists.H"
    #include "createTime.H"
    #include "createDynamicFvMesh.H" // DyM
    #include "createDyMControls.H" // pimpleControl pimple(mesh);
    #include "createFields.H"
    #include "createFieldRefs.H"
    #include "createRhoUfIfPresent.H" // rhoUf = rho*U

    // * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

    Info<< "\nStarting time loop\n" << endl;

    while (pimple.run(runTime))
    {
        #include "readDyMControls.H"

        // Store divrhoU from the previous mesh so that it can be mapped
        // and used in correctPhi to ensure the corrected phi has the
        // same divergence
        autoPtr<volScalarField> divrhoU;
        if (correctPhi)
        {
            divrhoU = new volScalarField
            (
                "divrhoU",
                fvc::div(fvc::absolute(phi, rho, U))
            );
        }

        #include "compressibleCourantNo.H"
        #include "setDeltaT.H"

        runTime++;

        Info<< "Time = " << runTime.timeName() << nl << endl;

        mesh.update(); // DyM, do any mesh changes

        if (mesh.changing())
        {
            if (correctPhi)
            {
                // Calculate absolute flux
                // from the mapped surface velocity
                phi = mesh.Sf() & rhoUf();

                #include "correctPhi.H"

                // Make the fluxes relative to the mesh-motion
                fvc::makeRelative(phi, rho, U);
            }

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
                fvm::ddt(rho, U)
              + fvc::div(phi, U)
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

            fvScalarMatrix eEqn
            (
                fvm::ddt(rho, e)
              + fvm::div(phi, e)
             ==
              - fvc::div(p*U)
              + fvc::div(thermo.kappa()*fvc::grad(T))
              + (
                     U & (
                            mu*fvc::laplacian(U)
                          + fvc::grad(mu/3*fvc::div(U))
                         )
                )
              //+ mu*D TODO
            );

            eEqn.relax();
            eEqn.solve();

            // Upgrade values using field e
            thermo.correct();

            p = rho/psi;

            phi = fvc::flux(rho*U);

            fvScalarMatrix alphaAirEqn
            (
                fvm::ddt(rho, alphaAir)
              + fvm::div(phi, alphaAir)
              - fvc::laplacian(DAir, rho*alphaAir)
            );

            alphaAirEqn.solve();

            fvScalarMatrix alphaGasEqn
            (
                fvm::ddt(rho, alphaGas)
              + fvm::div(phi, alphaGas)
              - fvc::laplacian(DGas, rho*alphaGas)
            );

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
