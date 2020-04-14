Info<< "Reading thermophysical properties\n" << endl;

autoPtr<fluidThermo> pThermo
(
    fluidThermo::New(mesh)
);
fluidThermo& thermo = pThermo();
thermo.validate(args.executable(), "h", "e");

volScalarField& p = thermo.p(); // Ref

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

// Infer the density BCs from the pressure
wordList rhoBCTypes
(
    p.boundaryField().size(),
    zeroGradientFvPatchScalarField::typeName
);

forAll(U.boundaryField(), patchi)
{
    if (U.boundaryField().types()[patchi] == zeroGradientFvPatchScalarField::typeName)
    {
        rhoBCTypes[patchi] = fixedValueFvPatchScalarField::typeName;
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
    rhoBCTypes
);

#include "compressibleCreatePhi.H"

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

Info<< "Reading diffusivity DT" << endl;

dimensionedScalar DT
(
    transportProperties.lookup("DT")
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