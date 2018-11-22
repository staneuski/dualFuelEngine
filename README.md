# [CATIA](CATIA)
**3D модели для всех проектов**

Файлы сохранены в папках с аналогичным названием подпроектов, как в формате _.CATPart_, так и в _.stl_ (неотмасшабированные).

# [multiCompression](multiCompression)
**Ядро решателя**

[multiCompression.C](multiCompression/multiCompression.C)
[createFields.H](multiCompression/createFields.H)

# [quadPiston](quadPiston)
**Предварительная сетка для проверки работоспособности моделей**

## [case](quadPiston/case)
Настройщики/словари для запуска решения проекта на собственном ядре и соответствующие скрипты.

**Граничные условия**: 

- [Скорости](quadPiston/case/0/U.orig)
- [Давления](quadPiston/case/0/p.orig)
- [Температуры](quadPiston/case/0/U.orig)

## [casePotential](quadPiston/casePotential)
Настройщики/словари и скрипты для запуска решения проекта на ядре potentialFoam для сравнения решения на собственном ядре и соответствующие скрипты.

## [caseScalar](quadPiston/caseScalar)
Настройщики/словари и скрипты для запуска решения проекта на ядре scalarPatentialFoam для сравнения решения на собственном ядре.

## [geometry](quadPiston/geometry)
Файлы _.stl_ и скрипт для их масштабирования из *м* в *мм* (проблема возникает при построении модели в CATIA).

## [mesh](quadPiston/mesh)
Настройщики/словари генерации сетки и скрипты запускающие эту генерацию
