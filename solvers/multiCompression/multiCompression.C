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
    multiCompression

Description
    v0.2-alpha

Comments

    fvc - явный метод,   возвращает поле
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
    
    #include "CourantNo.H"
    
    Info<< "\nStarting time loop\n" << endl;
    
    while (simple.loop(runTime))
    {
        Info<< "Time = " << runTime.timeName() << nl << endl;
                
        while (simple.correctNonOrthogonal())
        {
			surfaceScalarField phiDiff(phi/DIFFDENSITY);
			
            fvScalarMatrix TEqn
            (
                fvm::ddt(T)
              + fvm::div(phiDiff, T)
              - fvm::laplacian(DT, T)
             ==
                fvOptions(T)
            );

            TEqn.relax(); // FIXME What are these lines mean ?
            fvOptions.constrain(TEqn);
            TEqn.solve();
            fvOptions.correct(T);
            
            fvScalarMatrix rhoEqn
            (
                fvm::ddt(rho)
              + fvc::div(phiDiff, rho)
            );

            // rhoEqn.relax();
            // fvOptions.constrain(rhoEqn);
            rhoEqn.solve();
                        
            fvVectorMatrix UEqn
            (
                fvm::ddt(rho, U)
              + fvc::div(phi, U)
             ==
              - fvc::grad(p)
              + fvc::grad
                (
                    MU/3*fvc::div(U)
                )
              + fvc::laplacian(U)
            );

            // UEqn.relax();
            // fvOptions.constrain(UEqn);
            UEqn.solve();

            // Calculate energy field
            volScalarField e(p/(GAMMA - 1)/rho + magSqr(U)/2);

            fvScalarMatrix pEqn
            (
                fvm::ddt(rho, e)
             ==
              - fvc::div(p*U)
              + fvc::div(LAMBDA*fvc::grad(T))
              + ( U & (MU*fvc::laplacian(U) + fvc::grad(MU/3*fvc::div(U))) )
            // rho*epsilon FIXME What is epsilon?
            // TODO Add mu*D
            );

            // pEqn.relax();
            // fvOptions.constrain(pEqn);
            pEqn.solve();
            
        }
        
        runTime.write();

        Info<< "ExecutionTime = " << runTime.elapsedCpuTime() << " s"
            << "  ClockTime = " << runTime.elapsedClockTime() << " s"
            << nl << endl;
    }

    Info<< "End\n" << endl;

}

// ************************************************************************* //