# [CATIA](doc/CATIA)
**3D модели для всех проектов**

Файлы сохранены в папках с аналогичным названием подпроектов, как в формате _.CATPart_, так и в _.stl_ (неотмасшабированные).

# [multiCompression](solvers/multiCompression)
**Ядро решателя**

[multiCompression.C](solvers/multiCompression/multiCompression.C)
[createFields.H](solvers/multiCompression/createFields.H)

# [quadPiston](tutorials/quadPiston)
**Предварительная сетка для проверки работоспособности моделей**

## [case](tutorials/quadPiston/case)
Настройщики/словари для запуска решения проекта на собственном ядре и соответствующие скрипты.

**Граничные условия**: 

- [Скорости](tutorials/quadPiston/case/0/U.orig)
- [Давления](tutorials/quadPiston/case/0/p.orig)
- [Температуры](tutorials/quadPiston/case/0/U.orig)

## [casePotential](tutorials/quadPiston/casePotential)
Настройщики/словари и скрипты для запуска решения проекта на ядре potentialFoam для сравнения решения на собственном ядре и соответствующие скрипты.

## [caseScalar](tutorials/quadPiston/caseScalar)
Настройщики/словари и скрипты для запуска решения проекта на ядре scalarPatentialFoam для сравнения решения на собственном ядре.

## [geometry](tutorials/quadPiston/geometry)
Файлы _.stl_ и скрипт для их масштабирования из *м* в *мм* (проблема возникает при построении модели в CATIA).

## [mesh](tutorials/quadPiston/mesh)
Настройщики/словари генерации сетки и скрипты запускающие эту генерацию
