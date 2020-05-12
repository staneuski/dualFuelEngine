# About dualFuelEngine
OpenFOAM solver based on phenomenological compression model for dual-fuel ship engines. Check [**releases**](https://github.com/StasF1/dualFuelEngine/releases) to view repository history and more detailed description.

# Requirements
- OpenFOAM-dev ([`20200508`](https://github.com/OpenFOAM/OpenFOAM-dev/releases/tag/20200508) at least) or OpenFOAM v8

# Usage
## Installation
1. Set path to install and save it as OpenFOAM variable (optional, if OpenFOAM installed by default requires `sudo`)
    ```sh
    FOAM_ADD=$WM_PROJECT_USER_DIR/additions # ~/OpenFOAM/$USER-$WM_PROJECT_VERSION/additions/ by default
    mkdir -p $FOAM_ADD
    sudo sed -i "s+# Convenience+# Convenience\nexport FOAM_ADD=$FOAM_ADD+g" $WM_PROJECT_DIR/etc/config.sh/settings
    ```

1. To compile with OpenFOAM-dev or higher
    ```sh
    git clone https://github.com/StasF1/dualFuelEngine.git $FOAM_ADD/dualFuelEngine
    $FOAM_ADD/dualFuelEngine/solvers/./Allwmake
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
dualFuelEngine-0.4.x-alpha
├── etc
│   ├── DRK2Py
│   └── scripts
├── solvers
│   ├── multiCompressionFoam
│   └── utilities
└── tutorials
    ├── multiCompressionFoam
    │   ├── RiemannTube
    │   ├── tube
    │   ├── closedPipe
    │   ├── quadPiston
    │   └── cylPiston
    └── resources
        ├── blockMesh
        ├── createBaffles
        ├── geometry
        │   ├── MAN_BnW
        │   └── quadPiston
        └── topoSet
```
