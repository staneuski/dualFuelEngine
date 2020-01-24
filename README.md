# About dualFuelEngine
OpenFOAM solver based on phenomenological compression model for dual-fuel ship engines.

# Requirements
- OpenFOAM v6 or higher (preferred)
- OpenFOAM v5 (check the [issue #6](https://github.com/StasF1/dualFuelEngine/issues/6)) 

# [Releases](https://github.com/StasF1/dualFuelEngine/releases)
|Version|Description|Doc|Source code 📥|
|------:|:----------|:-:|:-------------|
[v0.3-alpha](https://github.com/StasF1/dualFuelEngine/tree/v0.3-alpha)|Improved stability. Concentration fields are back. [cylPiston](https://github.com/StasF1/dualFuelEngine/tree/v0.3-alpha/tutorials/multiCompression/cylPiston) case can be run now.|-|[.tar.gz](https://github.com/StasF1/dualFuelEngine/archive/v0.3-alpha.tar.gz), [.zip](https://github.com/StasF1/dualFuelEngine/archive/v0.3-alpha.zip)|
[v0.2-alpha](https://github.com/StasF1/dualFuelEngine/tree/v0.2-alpha)|Compressible flow. Solve Navier–Stokes equation and energy equation.|-|[.tar.gz](https://github.com/StasF1/dualFuelEngine/archive/v0.2-alpha.tar.gz), [.zip](https://github.com/StasF1/dualFuelEngine/archive/v0.2-alpha.zip)|
[v0.1-alpha](https://github.com/StasF1/dualFuelEngine/tree/v0.1-alpha)|Incompressible flow. Concentration fields.|[.pdf](https://github.com/StasF1/dualFuelEngine/releases/download/v0.1-alpha/dualFuelEngine-0.1-alpha.pdf)|[.tar.gz](https://github.com/StasF1/dualFuelEngine/archive/v0.1-alpha.tar.gz), [.zip](https://github.com/StasF1/dualFuelEngine/archive/v0.1-alpha.zip)|

# Usage
## Installation
1. Set path to install and save it as OpenFOAM variable (optional, if OpenFOAM installed by default requires sudo)
    ```sh
    mkdir -p $WM_PROJECT_USER_DIR/additions
    FOAM_ADD=$WM_PROJECT_USER_DIR/additions # path to install (~/OpenFOAM by default)
    sudo sed -i "s+# Convenience+# Convenience\nexport FOAM_ADD=$FOAM_ADD+g" $WM_PROJECT_DIR/etc/config.sh/settings
    ```

3. To compile with OpenFOAM v6 or higher
    ```sh
    git clone https://github.com/StasF1/dualFuelEngine.git $FOAM_ADD/dualFuelEngine
    $FOAM_ADD/dualFuelEngine/solvers/./Allwmake
    ```
    
4. To compile with OpenFOAM v5.x
    ```sh
    git clone https://github.com/StasF1/dualFuelEngine.git $FOAM_ADD/dualFuelEngine
    $FOAM_ADD/dualFuelEngine/etc/./v5x-compile
    $FOAM_ADD/dualFuelEngine/solvers/./Allwmake
    ```

## Running
```sh
wmake $FOAM_ADD/dualFuelEngine/tutorials/./Allclean && $FOAM_ADD/dualFuelEngine/tutorials/./Allrun
```

### Re-wmake and rerun by cases
- RiemannTube case
    ```sh
    wmake $FOAM_ADD/dualFuelEngine/solvers/multiCompression && $FOAM_ADD/dualFuelEngine/tutorials/multiCompression/RiemannTube/./Allclean && $FOAM_ADD/dualFuelEngine/tutorials/multiCompression/RiemannTube/./Allrun || cat $FOAM_ADD/dualFuelEngine/tutorials/multiCompression/RiemannTube/log.multiCompression
    ```
- quadPiston case
    ```sh
    wmake $FOAM_ADD/dualFuelEngine/solvers/multiCompression && $FOAM_ADD/dualFuelEngine/tutorials/multiCompression/quadPiston/./Allclean && $FOAM_ADD/dualFuelEngine/tutorials/multiCompression/quadPiston/./Allrun || cat $FOAM_ADD/dualFuelEngine/tutorials/multiCompression/quadPiston/log.multiCompression
    ```
- cylPiston case
    ```sh
    wmake $FOAM_ADD/dualFuelEngine/solvers/multiCompression && $FOAM_ADD/dualFuelEngine/tutorials/multiCompression/cylPiston/./Allclean && $FOAM_ADD/dualFuelEngine/tutorials/multiCompression/cylPiston/./Allrun || cat $FOAM_ADD/dualFuelEngine/tutorials/multiCompression/cylPiston/log.multiCompression
    ```

# Structure
```gitignore
dualFuelEngine-0.3-alpha
├── etc
├── solvers
│   ├── dyMFoam
│   ├── multiCompression
│   └── utilities
└── tutorials
    ├── dyMFoam
    │   ├── dynamicInkJetFvMesh
    │   │   ├── cylPiston
    │   │   ├── quadPiston
    │   │   └── tube
    │   └── dynamicMotionSolverFvMesh
    │       ├── cylPiston
    │       ├── cylPistonBlockMesh
    │       └── tube
    └── multiCompression
        ├── RiemannTube
        ├── cylPiston
        ├── quadPiston
        └── tube
```