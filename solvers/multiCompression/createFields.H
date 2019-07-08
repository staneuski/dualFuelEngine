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

Info<< "Reading pressure field p\n" << nl << endl;

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

Info<< "Reading pressure field rho\n" << nl << endl;

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

Info<< "Reading temperure field T\n" << nl << endl;

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
	fvc::flux(rho*U) // FIXME phi with density makes dimensions not equal almost in every Eqn
);

Info<< "Reading thermophysical properties\n" << endl;

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

Info<< "Reading diffusivity DT\n" << endl;

dimensionedScalar DT
(
	thermophysicalProperties.lookup("DT")
);

Info<< "Reading dinamic viscosity\n" << endl;

dimensionedScalar MU
(
	thermophysicalProperties.lookup("MU")
);

Info<< "Reading DIFFDENSITY\n" << endl;

dimensionedScalar DIFFDENSITY
(
	thermophysicalProperties.lookup("DIFFDENSITY")
);


Info<< "Reading heat capacity ratio\n" << endl;

dimensionedScalar GAMMA
(
	thermophysicalProperties.lookup("GAMMA")
);

Info<< "Reading thermal conductivity\n" << endl;

dimensionedScalar LAMBDA
(
	thermophysicalProperties.lookup("LAMBDA")
);

#include "createFvOptions.H"