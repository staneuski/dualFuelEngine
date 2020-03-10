# About dualFuelEngine
OpenFOAM solver based on phenomenological compression model for dual-fuel ship engines. Check [**releases**](https://github.com/StasF1/dualFuelEngine/releases) to view repository history and more detailed description.

# Requirements
- **OpenFOAM v7 (preferred)**
- OpenFOAM v6 (has some bugs with an ACMI interface)
- OpenFOAM v5 (check the [issue #6](https://github.com/StasF1/dualFuelEngine/issues/6)) 

# Usage
## Installation
1. Set path to install and save it as OpenFOAM variable (optional, if OpenFOAM installed by default requires `sudo`)
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

## Run
- Run all cases
    ```sh
    wmake $FOAM_ADDITIONS/dualFuelEngine/tutorials/./Allclean && $FOAM_ADDITIONS/dualFuelEngine/tutorials/./Allrun
    ```
- ParaView _.foam_ result file is created after running the _Allrun_ script which is also a script which can **rerun the current case**
    ```sh
    ./*foam
    ```

# Structure
```gitignore
dualFuelEngine-0.4-alpha
├── etc
│   └── DRK2Py
├── solvers
│   ├── dyMFoam
│   ├── multiCompressionFoam
│   └── utilities
└── tutorials
    ├── dyMFoam
    │   ├── tube
    │   ├── quadPiston
    │   ├── cylSym2D
    │   └── cylPiston
    └── multiCompressionFoam
        ├── RiemannTube
        ├── tube
        ├── closedPipe
        ├── quadPiston
        └── cylPiston
```
