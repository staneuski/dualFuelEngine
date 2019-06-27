
# About dualFuelEngine
OpenFOAM solver based on phenomenological compression model for dual-fuel ship engines.

# Requirements
- [OpenFOAM v6](https://openfoam.org/download/)

# [Releases](https://github.com/StasF1/dualFuelEngine/releases)

|Version|Description|Download|
|------:|:----------|:-------|
[v0.1-alpha](https://github.com/StasF1/dualFuelEngine/tree/v0.1-alpha)|Incompressible flow. Concentration fields.|[v0.1-alpha.tar.gz](https://github.com/StasF1/dualFuelEngine/archive/v0.1-alpha.tar.gz), [v0.1-alpha.zip](https://github.com/StasF1/dualFuelEngine/archive/v0.1-alpha.zip)|

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
    │   ├── prism
    │   └── quadPiston
    ├── potentialFoam
    │   ├── prism
    │   └── quadPiston
    ├── scalarTransportFoam
    │   ├── prism
    │   └── quadPiston
    └── testFoam
        └── quadPiston
```
---
