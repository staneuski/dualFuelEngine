#!/bin/sh
# Масштабирование файлов для последующего

# ------------------------------------ Data -------------------------------- #

# Указание пути к файлам .stl для их копирования
cp -r ../../CATIA/quadPiston/*.stl ./

# -------------------------------------------------------------------------- #


# [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[ Script ]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]] #

# Inlet
export FILE="injectionXMinus.stl"
surfaceTransformPoints -scale '(0.001 0.001 0.001)' $FILE $FILE
export FILE="injectionXPlus.stl"
surfaceTransformPoints -scale '(0.001 0.001 0.001)' $FILE $FILE
export FILE="injectionYMinus.stl"
surfaceTransformPoints -scale '(0.001 0.001 0.001)' $FILE $FILE
export FILE="injectionYPlus.stl"
surfaceTransformPoints -scale '(0.001 0.001 0.001)' $FILE $FILE

# Injection
export FILE="inletXMinus.stl"
surfaceTransformPoints -scale '(0.001 0.001 0.001)' $FILE $FILE
export FILE="inletXPlus.stl"
surfaceTransformPoints -scale '(0.001 0.001 0.001)' $FILE $FILE
export FILE="inletYMinus.stl"
surfaceTransformPoints -scale '(0.001 0.001 0.001)' $FILE $FILE
export FILE="inletYPlus.stl"
surfaceTransformPoints -scale '(0.001 0.001 0.001)' $FILE $FILE

# Other
export FILE="outlet.stl"
surfaceTransformPoints -scale '(0.001 0.001 0.001)' $FILE $FILE
export FILE="valve.stl"
surfaceTransformPoints -scale '(0.001 0.001 0.001)' $FILE $FILE
export FILE="valve.stl"
surfaceTransformPoints -translate '(0 0 -0.25)' $FILE $FILE
export FILE="walls.stl"
surfaceTransformPoints -scale '(0.001 0.001 0.001)' $FILE $FILE





