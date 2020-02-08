CorrectPhi
(
    U,
    phi,
    p,
    rho,
    p/rho, // psi
    dimensionedScalar("rAUf", dimTime, 1),
    divrhoU(),
    pimple,
    true
);