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

Info<< "Reading density field rho" << nl << endl;

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

Info<< "Reading temperure field T" << nl << endl;

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

Info<< "Read isobaric heat capacity" << endl;

dimensionedScalar Cv
(
	thermophysicalProperties.lookup("Cv")
);

Info<< "Calculate isochoric heat capacity" << endl;

dimensionedScalar Cp
(
	R + Cv
);

Info<< "Calculate heat capacity ratio" << endl;

dimensionedScalar GAMMA
(
	Cp/Cv
);

Info<< "Constructing field phi\n" << endl;

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

wordList eBCTypes
(
    U.boundaryField().size(),
    fixedValueFvPatchScalarField::typeName
);

forAll(U.boundaryField(), patchi)
{
    if (U.boundaryField()[patchi].fixesValue())
    {
        eBCTypes[patchi] = zeroGradientFvPatchScalarField::typeName;
    }
}

Info<< "Constructing energy field e\n" << endl;

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