Info<< "Reading velocity field U\n" << endl;

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

U = dimensionedVector("0", U.dimensions(), Zero); // ????????????????

// Pressure field p
Info<< "Reading pressure field p" << nl << endl;

volScalarField p
(
    IOobject
    (
        "p",
		runTime.timeName(),
		mesh,
		IOobject::MUST_READ,
		IOobject::AUTO_WRITE
    ),
    mesh
);

Info<< "Reading pressure field rho" << nl << endl;

volScalarField rho
(
    IOobject
    (
        "rho",
        runTime.timeName(),
        mesh,
        IOobject::MUST_READ,
        IOobject::AUTO_WRITE
    ),
    mesh
);

Info<< "Constructing velocity potential field Phi\n" << endl;

wordList PhiBCTypes
(
    p.boundaryField().size(),
    zeroGradientFvPatchScalarField::typeName
);

forAll(p.boundaryField(), patchi)
{
    if (p.boundaryField()[patchi].fixesValue())
    {
        PhiBCTypes[patchi] = fixedValueFvPatchScalarField::typeName;
    }
}

volScalarField Phi
(
    IOobject
    (
        "Phi",
        runTime.timeName(),
        mesh,
        IOobject::READ_IF_PRESENT,
		IOobject::AUTO_WRITE
    ),
    mesh,
    dimensionedScalar("Phi", dimLength*dimVelocity, 0),
    PhiBCTypes
);

label PhiRefCell = 0;
scalar PhiRefValue = 0;
setRefCell
(
    Phi,
    multiCompression.dict(),
    PhiRefCell,
    PhiRefValue
);
mesh.setFluxRequired(Phi.name());

// SCALAR TRANSPORT FIELDS

Info<< "Reading field T\n" << endl;
volScalarField T
(
    IOobject
    (
        "T",
        runTime.timeName(),
        mesh,
        IOobject::MUST_READ,
        IOobject::AUTO_WRITE
    ),
    mesh
);

Info<< "Reading inlet air concentration field alpha_air\n" << endl;
volScalarField alpha_air
(
    IOobject
    (
        "alpha_air",
        runTime.timeName(),
        mesh,
        IOobject::MUST_READ,
        IOobject::AUTO_WRITE
    ),
    mesh
);

Info<< "Reading injectction gas concentration field alpha_gas\n" << endl;
volScalarField alpha_gas
(
    IOobject
    (
        "alpha_gas",
        runTime.timeName(),
        mesh,
        IOobject::MUST_READ,
        IOobject::AUTO_WRITE
    ),
    mesh
);

Info<< "Constructing exhaust concentration field alpha_exh" << nl << endl;
volScalarField alpha_exh
(
    IOobject
    (
        "alpha_exh",
        runTime.timeName(),
        mesh,
        IOobject::NO_READ,
        IOobject::AUTO_WRITE
    ),
    mesh,
	dimensionedScalar("alpha_exh", dimless, 0)
);

Info<< "Reading transportProperties\n" << endl;

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

Info<< "Reading diffusivities DT, DAir, Dgas and DExh\n" << endl;

dimensionedScalar DT
(
    transportProperties.lookup("DT")
);

dimensionedScalar DAir
(
    transportProperties.lookup("DAir")
);
dimensionedScalar DGas
(
    transportProperties.lookup("DGas")
);

#include "createFvOptions.H"





