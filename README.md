# Stucture
```
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
# solvers/
## [multiCompression/](solvers/multiCompression)
**Ядро решателя**

[multiCompression.C](solvers/multiCompression/multiCompression.C)

[createFields.H](solvers/multiCompression/createFields.H)

## [testFoam/](solvers/testFoam)
**Ядро решателя для проведения тестировки**

[testFoam.C](solvers/multiCompression/testFoam.C)

[createFields.H](solvers/multiCompression/createFields.H)

# tutorials/
## [multiCompression/quadPiston/](tutorials/multiCompression/quadPiston)
**Предварительная сетка для проверки работоспособности моделей**

# doc/
## [CATIA/](doc/CATIA)
**3D модели для всех проектов**

Файлы сохранены в папках с аналогичным названием подпроектов, как в формате _.CATPart_, так и в _.stl_ (неотмасшабированные).

---
# [Releases](https://github.com/StasF1/dualFuelEngine/releases)
- [v0.1-alpha:](https://github.com/StasF1/dualFuelEngine/tree/v0.1-alpha) Incompressible flow. Concentration fields.
