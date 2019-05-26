Info<< "Reading field x\n" << endl;

volScalarField x
(
    IOobject
    (
        "x",
        runTime.timeName(),
        mesh,
        IOobject::MUST_READ,
        IOobject::AUTO_WRITE
    ),
    mesh
);


Info<< "Reading field y\n" << endl;

volScalarField y
(
    IOobject
    (
        "y",
        runTime.timeName(),
        mesh,
        IOobject::MUST_READ,
        IOobject::AUTO_WRITE
    ),
    mesh
);

Info<< "Constructing field z\n" << endl;
volScalarField z
(
    IOobject
    (
        "z",
        runTime.timeName(),
        mesh,
        IOobject::NO_READ,
        IOobject::AUTO_WRITE
    ),
    mesh,
    dimensionedScalar("z", dimless, 0)
);
