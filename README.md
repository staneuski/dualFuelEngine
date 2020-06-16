# About dualFuelEngine
OpenFOAM solver based on phenomenological compression model for dual-fuel ship engines. Check [**releases**](https://github.com/StasF1/dualFuelEngine/releases) to view repository history and more detailed description.

# Requirements
- OpenFOAM-dev ([`20200426`](https://github.com/OpenFOAM/OpenFOAM-dev/releases/tag/20200426) at least) or OpenFOAM v8

# Usage
## Installation
1. Set path to install and save it as OpenFOAM variable (optional, if OpenFOAM installed by default requires `sudo`)
    ```sh
    FOAM_ADD=$WM_PROJECT_USER_DIR/additions # ~/OpenFOAM/$USER-$WM_PROJECT_VERSION/additions/ by default
    mkdir -p $FOAM_ADD
    sudo sed -i "s+# Convenience+# Convenience\nexport FOAM_ADD=$FOAM_ADD+g" $WM_PROJECT_DIR/etc/config.sh/settings
    ```

1. To compile with OpenFOAM v8 or higher
    ```sh
    git clone https://github.com/StasF1/dualFuelEngine.git $FOAM_ADD/dualFuelEngine
    $FOAM_ADD/dualFuelEngine/solvers/./Allwmake
    ```

1. Add makeBackup script as a link to the OpenFOAM-?/bin
    ```sh
    sudo ln -s $FOAM_ADD/dualFuelEngine/etc/scripts/foamBackup $FOAM_APP/../bin/foamBackup
    ```

## Run
- Run all cases
    ```sh
    wmake $FOAM_ADD/dualFuelEngine/tutorials/./Allclean && $FOAM_ADD/dualFuelEngine/tutorials/./Allrun
    ```
- ParaView _.foam_ result file is created after running the _Allrun_ script which is also a script that can **rerun the current case**
    ```sh
    ./*foam
    ```

# Structure
```gitignore
dualFuelEngine-0.5.x-alpha
├── etc
│   ├── DRK2Py
│   │   ├── include
│   │   └── MAN_BnW-DieselRK.drkres # download MAN_BnW.drkres.zip from the v0.5-alpha
│   └── scripts
├── solvers
│   └── multiCompressionFoam
│       └── Make
└── tutorials
    ├── multiCompressionFoam
    │   ├── cylCyclic2D
    │   │   ├── cylCyclic2D_multiCompressionFoam
    │   │   └── cylCyclic2D_rhoPimpleFoam
    │   ├── cylPiston
    │   │   ├── cylPiston_multiCompressionFoam
    │   │   └── cylPiston_rhoPimpleFoam
    │   ├── pipeCompression
    │   │   ├── pipeCompression_multiCompressionFoam
    │   │   ├── pipeCompression_rhoCentralFoam
    │   │   └── pipeCompression_rhoPimpleFoam
    │   ├── quadPiston
    │   ├── RiemannTube
    │   ├── shockTube
    │   │   ├── shockTube_multiCompressionFoam
    │   │   ├── shockTube_rhoCentralFoam
    │   │   └── shockTube_rhoPimpleFoam
    │   └── tubePurging
    │       ├── tubePurging_multiCompressionFoam
    │       ├── tubePurging_rhoCentralFoam
    │       └── tubePurging_rhoPimpleFoam
    └── resources
        ├── blockMesh
        ├── createBaffles
        ├── engineProperties
        ├── geometry
        └── topoSet
```
