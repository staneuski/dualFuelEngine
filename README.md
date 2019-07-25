# About dualFuelEngine
OpenFOAM solver based on phenomenological compression model for dual-fuel ship engines.

# Requirements
- OpenFOAM v6 or higher (preferred)
- OpenFOAM v5 (check [issue #6](https://github.com/StasF1/dualFuelEngine/issues/6)) 

# [Releases](https://github.com/StasF1/dualFuelEngine/releases)
|Version|Description|Doc|Source code 📥|
|------:|:----------|:-:|:-------------|
[v0.2-alpha](https://github.com/StasF1/dualFuelEngine/tree/v0.1-alpha)|Compressible flow. Solve Navier–Stokes equation and energy equation.|-|[.tar.gz](https://github.com/StasF1/dualFuelEngine/archive/v0.2-alpha.tar.gz), [.zip](https://github.com/StasF1/dualFuelEngine/archive/v0.2-alpha.zip)|
[v0.1-alpha](https://github.com/StasF1/dualFuelEngine/tree/v0.1-alpha)|Incompressible flow. Concentration fields.|[.pdf](https://github.com/StasF1/dualFuelEngine/releases/download/v0.1-alpha/dualFuelEngine-0.1-alpha.pdf)|[.tar.gz](https://github.com/StasF1/dualFuelEngine/archive/v0.1-alpha.tar.gz), [.zip](https://github.com/StasF1/dualFuelEngine/archive/v0.1-alpha.zip)|

# Usage
## Installation
1. Set path to install and save it as OpenFOAM variable (optional, if OpenFOAM installed by default requires sudo)
	```bash
	FOAM_ADDITIONS="\$HOME/\$WM_PROJECT" # path to install (~/OpenFOAM by default)
	sudo sed -i "s+# Convenience+# Convenience\nexport FOAM_ADDITIONS=$FOAM_ADDITIONS+g" $WM_PROJECT_DIR/etc/config.sh/settings
	```

3. To compile with OpenFOAM v6 or higher
	```bash
	git clone https://github.com/StasF1/dualFuelEngine.git $FOAM_ADDITIONS/dualFuelEngine
	$FOAM_ADDITIONS/dualFuelEngine/solvers/./Allwmake
	```
	
4. To compile with OpenFOAM v5.x
	```bash
	git clone https://github.com/StasF1/dualFuelEngine.git $FOAM_ADDITIONS/dualFuelEngine
	$FOAM_ADDITIONS/dualFuelEngine/etc/./v5x-compile
	$FOAM_ADDITIONS/dualFuelEngine/solvers/./Allwmake
	```

## Running
```bash
wmake $FOAM_ADDITIONS/dualFuelEngine/tutorials/./Allclean && $FOAM_ADDITIONS/dualFuelEngine/tutorials/./Allrun
```

### Re-wmake and rerun by cases
- RiemannTube case
    ```bash
    wmake $FOAM_ADDITIONS/dualFuelEngine/solvers/multiCompression && $FOAM_ADDITIONS/dualFuelEngine/tutorials/multiCompression/RiemannTube/./Allclean && $FOAM_ADDITIONS/dualFuelEngine/tutorials/multiCompression/RiemannTube/./Allrun || cat $FOAM_ADDITIONS/dualFuelEngine/tutorials/multiCompression/RiemannTube/log.multiCompression
    ```
- quadPiston case
    ```bash
    wmake $FOAM_ADDITIONS/dualFuelEngine/solvers/multiCompression && $FOAM_ADDITIONS/dualFuelEngine/tutorials/multiCompression/quadPiston/./Allclean && $FOAM_ADDITIONS/dualFuelEngine/tutorials/multiCompression/quadPiston/./Allrun || cat $FOAM_ADDITIONS/dualFuelEngine/tutorials/multiCompression/quadPiston/log.multiCompression
    ```
- cylPiston case (only meshing now)
    ```bash
    $FOAM_ADDITIONS/dualFuelEngine/tutorials/multiCompression/cylPiston/./Allclean && $FOAM_ADDITIONS/dualFuelEngine/tutorials/multiCompression/cylPiston/./Allrun || cat $FOAM_ADDITIONS/dualFuelEngine/tutorials/multiCompression/cylPiston/log.blockMesh
    ```

# Structure
```gitignore
dualFuelEngine-0.2-alpha
├── doc
├── etc
├── solvers
│   ├── multiCompression
│   └── testFoam
└── tutorials
    ├── multiCompression
    │   ├── cylPiston	
    │   ├── quadPiston
    │   └── RiemannTube
    ├── potentialFoam
    │   ├── prism
    │   └── quadPiston
    ├── scalarTransportFoam
    │   ├── prism
    │   └── quadPiston
    └── testFoam
        └── prism
```