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

Info<< "Reading heat capacity ratio" << endl;

dimensionedScalar GAMMA
(
	thermophysicalProperties.lookup("GAMMA")
);

Info<< "Reading thermal conductivity\n" << endl;

dimensionedScalar LAMBDA
(
	thermophysicalProperties.lookup("LAMBDA")
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

Info<< "Constructing energy field" << endl;

volScalarField e
(
	IOobject
	(
		"e",
		runTime.timeName(),
		mesh,
		IOobject::NO_READ,
		IOobject::NO_WRITE
	),
	p/(GAMMA - 1)/rho + magSqr(U)/2
);

#include "createFvOptions.H"