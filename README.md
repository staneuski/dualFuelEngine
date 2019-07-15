# About dualFuelEngine
OpenFOAM solver based on phenomenological compression model for dual-fuel ship engines.

# Requirements
- OpenFOAM v6 or v7 (preferred)
- OpenFOAM v5 (check [issue #6](https://github.com/StasF1/dualFuelEngine/issues/6)) 

# [Releases](https://github.com/StasF1/dualFuelEngine/releases)
|Version|Description|Documentation|Source code 📥|
|------:|:----------|:-----------:|:-------------|
[v0.2-alpha](https://github.com/StasF1/dualFuelEngine/tree/v0.1-alpha)|Compressible flow. Solve Navier–Stokes equation and energy equation.|-|[.tar.gz](https://github.com/StasF1/dualFuelEngine/archive/v0.2-alpha.tar.gz)<br> [.zip](https://github.com/StasF1/dualFuelEngine/archive/v0.2-alpha.zip)|
[v0.1-alpha](https://github.com/StasF1/dualFuelEngine/tree/v0.1-alpha)|Incompressible flow. Concentration fields.|[.pdf](https://github.com/StasF1/dualFuelEngine/releases/download/v0.1-alpha/dualFuelEngine-0.1-alpha.pdf)|[.tar.gz](https://github.com/StasF1/dualFuelEngine/archive/v0.1-alpha.tar.gz)<br> [.zip](https://github.com/StasF1/dualFuelEngine/archive/v0.1-alpha.zip)|

# Usage
### Installation
```bash
git clone https://github.com/StasF1/dualFuelEngine.git ~/OpenFOAM/dualFuelEngine
```

### Running
- RiemannTube case
    ```bash
    wmake ~/OpenFOAM/dualFuelEngine/solvers/multiCompression && ~/OpenFOAM/dualFuelEngine/tutorials/multiCompression/RiemannTube/./Allclean && ~/OpenFOAM/dualFuelEngine/tutorials/multiCompression/RiemannTube/./Allrun || cat ~/OpenFOAM/dualFuelEngine/tutorials/multiCompression/RiemannTube/log.multiCompression
    ```
- quadPiston case
    ```bash
    wmake ~/OpenFOAM/dualFuelEngine/solvers/multiCompression && ~/OpenFOAM/dualFuelEngine/tutorials/multiCompression/quadPiston/./Allclean && ~/OpenFOAM/dualFuelEngine/tutorials/multiCompression/quadPiston/./Allrun || cat ~/OpenFOAM/dualFuelEngine/tutorials/multiCompression/quadPiston/log.multiCompression
    ```

# Structure
```gitignore
dualFuelEngine-0.2-alpha
├── doc
├── solvers
│   ├── multiCompression
│   └── testFoam
└── tutorials
    ├── multiCompression
    │   ├── RiemannTube
    │   └── quadPiston
    ├── potentialFoam
    │   ├── prism
    │   └── quadPiston
    ├── scalarTransportFoam
    │   ├── prism
    │   └── quadPiston
    └── testFoam
        └── prism
```