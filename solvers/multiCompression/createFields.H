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

U = dimensionedVector("0", U.dimensions(), Zero); // ????

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
    fvc::flux(U)
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

Info<< "Constructing specific energy field e" << nl << endl;

wordList eBCTypes
(
	rho.boundaryField().size(),
	zeroGradientFvPatchScalarField::typeName
);

forAll(rho.boundaryField(), patchi)
{
    if (rho.boundaryField()[patchi].fixesValue())
    {
        eBCTypes[patchi] = fixedValueFvPatchScalarField::typeName;
    }
}

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
	p/(k - 1)*rho + sqr(phi)/2,
    eBCTypes
);

Info<< "Constructing mass field M" << nl << endl;

wordList IntegralBCTypes
(
	rho.boundaryField().size(),
	zeroGradientFvPatchScalarField::typeName
);

forAll(rho.boundaryField(), patchi)
{
    if (rho.boundaryField()[patchi].fixesValue())
    {
        IntegralBCTypes[patchi] = fixedValueFvPatchScalarField::typeName;
    }
}

volScalarField M
(
	IOobject
	(
	    "M",
	    runTime.timeName(),
	    mesh,
	    IOobject::NO_READ,
	    IOobject::AUTO_WRITE
	),
	rho*phi*deltaT*F, // deltaT*F - ?
    IntegralBCTypes
);

Info<< "Constructing momentum field K" << nl << endl;

volScalarField K
(
	IOobject
	(
	    "K",
	    runTime.timeName(),
	    mesh,
	    IOobject::NO_READ,
	    IOobject::AUTO_WRITE
	),
	M*phi,
    IntegralBCTypes
);

Info<< "Constructing energy field E" << nl << endl;

volScalarField E
(
	IOobject
	(
	    "E",
	    runTime.timeName(),
	    mesh,
	    IOobject::NO_READ,
	    IOobject::AUTO_WRITE
	),
	M*e,
    IntegralBCTypes
);

#include "createFvOptions.H"
