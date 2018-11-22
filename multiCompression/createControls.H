const dictionary& potentialFlow
(
    mesh.solutionDict().subDict("multiCompression")
);

const int nNonOrthCorr
(
    multiCompression.lookupOrDefault<int>("nNonOrthogonalCorrectors", 0)
);
