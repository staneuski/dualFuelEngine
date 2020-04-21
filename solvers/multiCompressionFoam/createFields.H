Info<< "Reading thermophysical properties\n" << endl;

autoPtr<fluidThermo> pThermo
(
    fluidThermo::New(mesh)
);
fluidThermo& thermo = pThermo();

volScalarField& p = thermo.p();

// Infer the density BCs from the pressure
wordList rhoTypes
(
    p.boundaryField().size()
);

// Set the same type BCs of rho as for T and set them to zero-gradient for
// patches at which p and T is fixed
forAll(p.boundaryField(), patchi)
{
    if
    (
        (
            p.boundaryField()[patchi].fixesValue()
         && thermo.T().boundaryField()[patchi].fixesValue()
        )
     ||
        (
            p.boundaryField().types()[patchi]
         ==
            zeroGradientFvPatchScalarField::typeName
        &&
            thermo.T().boundaryField().types()[patchi]
         ==
            zeroGradientFvPatchScalarField::typeName
        )
    )
    {
        rhoTypes[patchi] = zeroGradientFvPatchScalarField::typeName;
    }
    else
    {
        rhoTypes[patchi] = thermo.T().boundaryField().types()[patchi];
    }
}

Info<< "\nConstructing density field rho" << nl << endl;
volScalarField rho
(
    IOobject
    (
        "rho",
        runTime.timeName(),
        mesh,
        IOobject::READ_IF_PRESENT,
        IOobject::AUTO_WRITE
    ),
    thermo.rho(),
    rhoTypes
);

Info<< "Reading velocity field U" << endl;
volVectorField U
(
    IOobject
    (
        "U",
        runTime.timeName(),
        mesh,
        IOobject::MUST_READ,
        IOobject::AUTO_WRITE
    ),
    mesh
);

#include "compressibleCreatePhi.H"

pressureControl pressureControl
(
    p,
    rho,
    pimple.dict(),
    thermo.incompressible()
);

Info<< "Reading concentration fields" << endl;

volScalarField alphaAir
(
    IOobject
    (
        "alphaAir",
        runTime.timeName(),
        mesh,
        IOobject::MUST_READ,
        IOobject::AUTO_WRITE
    ),
    mesh
);
volScalarField alphaGas
(
    IOobject
    (
        "alphaGas",
        runTime.timeName(),
        mesh,
        IOobject::MUST_READ,
        IOobject::AUTO_WRITE
    ),
    mesh
);

Info<< "\nConstructing exhaust concentration field\n" << endl;
volScalarField alphaExh
(
    IOobject
    (
        "alphaExh",
        runTime.timeName(),
        mesh,
        IOobject::NO_READ,
        IOobject::AUTO_WRITE
    ),
    mesh,
    dimensionedScalar("alphaExh", dimless, 0)
);

Info<< "Reading transport properties\n" << endl;
IOdictionary transportProperties
(
    IOobject
    (
        "transportProperties",
        runTime.constant(),
        mesh,
        IOobject::MUST_READ_IF_MODIFIED,
        IOobject::NO_WRITE
    )
);

Info<< "Reading DAir (equals diffusivity DT)" << endl;
dimensionedScalar DAir
(
    transportProperties.lookup("DT")
);

Info<< "Reading DGas (equals diffusivity DT)" << endl;
dimensionedScalar DGas
(
    transportProperties.lookup("DT")
);

Info<< "Creating field kinetic energy K\n" << endl;
volScalarField K("K", 0.5*magSqr(U));

#include "createFvOptions.H"