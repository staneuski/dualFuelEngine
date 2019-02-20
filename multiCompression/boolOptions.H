argList::addOption
(
    "pName",
    "pName",
    "Name of the pressure field"
);

argList::addBoolOption
(
    "initialiseUBCs",
    "Initialise U boundary conditions"
);

argList::addBoolOption
(
    "writePhi",
    "Write the velocity potential field"
);

argList::addBoolOption
(
    "writep",
    "Calculate and write the pressure field"
);

argList::addBoolOption
(
    "withFunctionObjects",
    "execute functionObjects"
);

argList::addBoolOption
(
    "writedivphi",
    "Calculating divergence of phi"
);

argList::addBoolOption
(
    "stat",
    "Calculating transport equation stationary"
);
