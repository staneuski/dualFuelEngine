# About dualFuelEngine
OpenFOAM solver based on phenomenological compression model for dual-fuel ship engines.

# Requirements
- OpenFOAM v6 (preferred)
- OpenFOAM v5 (check [issue #6](https://github.com/StasF1/dualFuelEngine/issues/6)) 

# [Releases](https://github.com/StasF1/dualFuelEngine/releases)
|Version|Description|Documentation|Source code|
|------:|:----------|:------------|:----------|
[v0.1-alpha](https://github.com/StasF1/dualFuelEngine/tree/v0.1-alpha)|Incompressible flow. Concentration fields.|[doc-0.1-alpha](https://github.com/StasF1/dualFuelEngine/releases/download/v0.1-alpha/dualFuelEngine-0.1-alpha.pdf)|[v0.1-alpha.tar.gz](https://github.com/StasF1/dualFuelEngine/archive/v0.1-alpha.tar.gz)<br> [v0.1-alpha.zip](https://github.com/StasF1/dualFuelEngine/archive/v0.1-alpha.zip)|

# Structure
```gitignore
dualFuelEngine-0.2-alpha
├── doc
│   └── CATIA
│       └── quadPiston
├── solvers
│   ├── multiCompression
│   └── testFoam
└── tutorials
    ├── multiCompression
    │   ├── quadPiston
    │   └── RiemannTube
    ├── potentialFoam
    │   ├── prism
    │   └── quadPiston
    ├── scalarTransportFoam
    │   ├── prism
    │   └── quadPiston
    └── testFoam
        └── quadPiston
```