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

Info<< "\nReading density field rho" << nl << endl;

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

Info<< "Reading temperature field T" << nl << endl;

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

Info<< "Reading thermophysical properties" << endl;

IOdictionary thermophysicalProperties
(
    IOobject
    (
        "thermophysicalProperties",
        runTime.constant(),
        mesh,
        IOobject::MUST_READ_IF_MODIFIED,
        IOobject::NO_WRITE
    )
);

Info<< "Reading diffusivity DT" << endl;

dimensionedScalar DT
(
	thermophysicalProperties.lookup("DT")
);

Info<< "Reading DAir" << endl;

dimensionedScalar DAir
(
    thermophysicalProperties.lookup("DAir")
);

Info<< "Reading DGas" << endl;

dimensionedScalar DGas
(
    thermophysicalProperties.lookup("DGas")
);

Info<< "Reading dinamic viscosity" << endl;

dimensionedScalar MU
(
	thermophysicalProperties.lookup("MU")
);

Info<< "Reading thermal conductivity" << endl;

dimensionedScalar LAMBDA
(
	thermophysicalProperties.lookup("LAMBDA")
);

Info<< "Reading gas constant" << endl;

dimensionedScalar R
(
	thermophysicalProperties.lookup("R")
);

Info<< "Reading isobaric heat capacity\n" << endl;

dimensionedScalar Cv
(
	thermophysicalProperties.lookup("Cv")
);

Info<< "Calculate isochoric heat capacity\n" << endl;

dimensionedScalar Cp
(
	R + Cv
);

Info<< "Calculate heat capacity ratio" << endl;

dimensionedScalar GAMMA
(
	Cp/Cv
);

Info<< "\nConstructing exhaust concentration field" << endl;

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

// Infer the pressure BCs from the temperature and the viscosity
wordList pBCTypes
(
    T.boundaryField().size(),
    fixedValueFvPatchScalarField::typeName
);

forAll(T.boundaryField(), patchi)
{
    if (!T.boundaryField()[patchi].fixesValue())
    {
        pBCTypes[patchi] = zeroGradientFvPatchScalarField::typeName;
    }
}

forAll(rho.boundaryField(), patchi)
{
    if (!rho.boundaryField()[patchi].fixesValue())
    {
        pBCTypes[patchi] = zeroGradientFvPatchScalarField::typeName;
    }
}

Info<< "\nConstructing pressure field p" << nl << endl;

volScalarField p
(
	IOobject
	(
		"p",
		runTime.timeName(),
		mesh,
		IOobject::NO_READ,
		IOobject::AUTO_WRITE
	),
	rho*R*T,
	pBCTypes
);

Info<< "Constructing field phi" << endl;

surfaceScalarField phi
(
	IOobject
	(
		"phi",
		runTime.timeName(),
		mesh,
		IOobject::NO_READ,
		IOobject::AUTO_WRITE
	),
	fvc::flux(rho*U)
);

// Infer the pressure BCs from the velocity and the pressure
wordList eBCTypes
(
    pBCTypes
);

forAll(U.boundaryField(), patchi)
{
    if (!U.boundaryField()[patchi].fixesValue())
    {
        eBCTypes[patchi] = zeroGradientFvPatchScalarField::typeName;
    }
}

Info<< "\nConstructing energy field e\n" << endl;

volScalarField e
(
	IOobject
	(
		"e",
		runTime.timeName(),
		mesh,
		IOobject::NO_READ,
		IOobject::AUTO_WRITE
	),
	p/(GAMMA - 1)/rho + magSqr(U)/2,
	eBCTypes
);

#include "createFvOptions.H"