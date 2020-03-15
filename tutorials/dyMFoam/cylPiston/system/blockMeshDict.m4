/*--------------------------------*- C++ -*----------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: dualFuelEngline addition to OpenFOAM v7
   \\    /   O peration     | Website:  https://github.com/StasF1/dualFuelEngine
    \\  /    A nd           | Version:  0.4-alpha
     \\/     M anipulation  |
\*---------------------------------------------------------------------------*/
FoamFile
{
    version     2;
    format      ascii;
    // `format'      ascii;
    class       dictionary;
    object      blockMeshDict;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
// General m4 macros

changecom(//)changequote([,]) dnl>
// define(calc, [esyscmd(perl -e 'use Math::Trig; print ($1)')]) dnl>
define(calc, [esyscmd(perl -e 'print ($1)')]) dnl>
define(VCOUNT, 0)
define(vlabel, [[// ]Vertex $1 = VCOUNT define($1, VCOUNT)define([VCOUNT], incr(VCOUNT))])

define(pi, 3.14159265)
define(sind, sin((pi/180)*$1))
define(cosd, cos((pi/180)*$1))

define(hex2D, hex ($1t $2t $3t $4t $1b $2b $3b $4b))
define(quad2D, ($1b $2b $2t $1t))
define(topQuad, ($1t $2t $4t $3t))
define(botQuad, ($1b $2b $4b $3b))

define(vert,  ($1 $2 $3))
define(evert, ($1 $2 $3))

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
// User-defined parameters

convertToMeters 0.01;

/*TODO Initial piston position (not only at BDC)*/
define(D, 70)             // Cylinder bore
define(S, 300)            // Cylinder Z size (> piston stroke)
define(chamfer, 15)       // Cylinder chamfer
define(pistonInit, 92.55) // Initial piston position

define(vlvS, 0)           // Initial valve stroke
define(vlvD, calc(D/2))   // Valve head diameter
define(vlvHd, 3)          // Valve head thickness
define(vlvStD, 8)         // Valve stem diameter
define(outletH, 50)       // Outer pipe height

/*TODO Create more options for inlet ports location & size*/
define(inlW, calc(D/2))   // Inlet port width
define(inlH, 25)          // Inlet port height
define(inlL, 10)          // Inlet port length from the cylinder wall

define(Nr, 5)             // Number of cells in the radius dimension
define(Nz, 20)            // Number of cells in the length dimension

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
// Derived parameters

/* Cylinder */
define(R, calc(D/2))                       // Cylinder radius
define(Rcos, calc(R*cosd(45)))             // Cylinder radius middle point

define(chS, calc(chamfer + S))

/* Valve */
define(vlvR, calc(vlvD/2))                 // Valve radius
define(vlvRcos, calc(vlvR*cosd(45)))       // Valve radius middle point

define(vlvStR, calc(vlvStD/2))             // Valve stem radius
define(vlvStRcos, calc(vlvStR*cosd(45)))   // Valve stem radius middle point

define(vlvFltR, calc(vlvR - vlvStR))       // Valve fillet radius
define(vlvFltRcos, calc(vlvFltR*cosd(45))) // Valve fillet radius middle point

define(vlvHdBot, calc(chS - vlvS))         // Valve head bottom Z coordinate
define(vlvHdTop, calc(vlvHdBot + vlvHd))   // Valve head top Z coordinate
define(vlvStBot, calc(vlvHdBot + vlvFltR)) // Valve stem bottom Z coordinate
define(vlvStTop, calc(S + outletH))        // Valve stem top & outer pipe top Z coordinate

/* Inlet ports */
define(inlCoord, calc(R + inlL))           // Inlet patch coordinate
define(inlRcos, calc(R*cosd(45)))          // Inlet port outlet patch X middle point
define(inlRsin, calc(R*sind(45)))          // Inlet port outlet patch Y middle point

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
// Parametric description

vertices
(
/* Cylinder */
    // Cylinder\Piston inner
    /*00*/ vert(vlvR,  0,    pistonInit) vlabel(cylIn0b)
    /*01*/ vert(0,    -vlvR, pistonInit) vlabel(cylIn1b)
    /*02*/ vert(-vlvR, 0,    pistonInit) vlabel(cylIn2b)
    /*03*/ vert(0,     vlvR, pistonInit) vlabel(cylIn3b)
    /*04*/ vert(vlvR,  0,    chS)        vlabel(cylIn0t)
    /*05*/ vert(0,    -vlvR, chS)        vlabel(cylIn1t)
    /*06*/ vert(-vlvR, 0,    chS)        vlabel(cylIn2t)
    /*07*/ vert(0,     vlvR, chS)        vlabel(cylIn3t)

    // Cylinder\Piston outer
    /*08*/ vert(R,  0, pistonInit) vlabel(cylOut0b)
    /*09*/ vert(0, -R, pistonInit) vlabel(cylOut1b)
    /*10*/ vert(-R, 0, pistonInit) vlabel(cylOut2b)
    /*11*/ vert(0,  R, pistonInit) vlabel(cylOut3b)
    /*12*/ vert(R,  0, S) vlabel(cylOut0t)
    /*13*/ vert(0, -R, S) vlabel(cylOut1t)
    /*14*/ vert(-R, 0, S) vlabel(cylOut2t)
    /*15*/ vert(0,  R, S) vlabel(cylOut3t)

/* Valve */
    // Valve head
    /*16*/ vert(vlvR,  0,    vlvHdBot) vlabel(vlvHd0b)
    /*17*/ vert(0,    -vlvR, vlvHdBot) vlabel(vlvHd1b)
    /*18*/ vert(-vlvR, 0,    vlvHdBot) vlabel(vlvHd2b)
    /*19*/ vert(0,     vlvR, vlvHdBot) vlabel(vlvHd3b)
    /*20*/ vert(vlvR,  0,    vlvHdTop) vlabel(vlvHd0t)
    /*21*/ vert(0,    -vlvR, vlvHdTop) vlabel(vlvHd1t)
    /*22*/ vert(-vlvR, 0,    vlvHdTop) vlabel(vlvHd2t)
    /*23*/ vert(0,     vlvR, vlvHdTop) vlabel(vlvHd3t)

    // Valve stem
    /*24*/ vert(vlvStR,   0,      vlvStBot) vlabel(vlvSt0b)
    /*25*/ vert(0,       -vlvStR, vlvStBot) vlabel(vlvSt1b)
    /*26*/ vert(-vlvStR,  0,      vlvStBot) vlabel(vlvSt2b)
    /*27*/ vert(0,        vlvStR, vlvStBot) vlabel(vlvSt3b)
    /*28*/ vert(vlvStR,   0,      vlvStTop) vlabel(vlvSt0t)
    /*29*/ vert(0,       -vlvStR, vlvStTop) vlabel(vlvSt1t)
    /*30*/ vert(-vlvStR,  0,      vlvStTop) vlabel(vlvSt2t)
    /*31*/ vert(0,        vlvStR, vlvStTop) vlabel(vlvSt3t)

/* Outer pipe */
    /*32*/ vert(vlvR,   0,    vlvStTop) vlabel(pipe0t)
    /*33*/ vert(0,     -vlvR, vlvStTop) vlabel(pipe1t)
    /*34*/ vert(-vlvR,  0,    vlvStTop) vlabel(pipe2t)
    /*35*/ vert(0,      vlvR, vlvStTop) vlabel(pipe3t)

/* Inlet ports */
    // xMinus inlet port
    /*36*/ vert(0,        inlW, 0)    vlabel(inlXm0b)
    /*37*/ vert(inlCoord, inlW, 0)    vlabel(inlXm1b)
    /*38*/ vert(inlCoord, 0,    0)    vlabel(inlXm2b)
    /*39*/ vert(R,        0,    0)    vlabel(inlXm3b)
    /*40*/ vert(0,        inlW, inlH) vlabel(inlXm0t)
    /*41*/ vert(inlCoord, inlW, inlH) vlabel(inlXm1t)
    /*42*/ vert(inlCoord, 0,    inlH) vlabel(inlXm2t)
    /*43*/ vert(R,        0,    inlH) vlabel(inlXm3t)

    /*TODO Create other three inlet ports blocks*/

/* Injectors */
    /*TODO Create injectors blocks*/
);


blocks
(
/* Cylinder */
    // Inner cylinder block
    hex (vlvHd0b vlvHd1b vlvHd2b vlvHd3b cylIn0b cylIn1b cylIn2b cylIn3b)
    cylinder /*block 0*/
    (Nr Nr Nz)
    simpleGrading (1 1 1)

    // 1st quarter outer cylinder block
    hex2D(cylIn0, cylOut0, cylOut1, cylIn1)
    cylinder /*block 1*/
    (Nr Nr Nz)
    simpleGrading (1 1 1)

    // 2nd quarter outer cylinder block
    hex2D(cylIn1, cylOut1, cylOut2, cylIn2)
    cylinder /*block 2*/
    (Nr Nr Nz)
    simpleGrading (1 1 1)

    // 3rd quarter outer cylinder block
    hex2D(cylIn2, cylOut2, cylOut3, cylIn3)
    cylinder /*block 3*/
    (Nr Nr Nz)
    simpleGrading (1 1 1)

    // 4th quarter outer cylinder block
    hex2D(cylIn3, cylOut3, cylOut0, cylIn0)
    cylinder /*block 4*/
    (Nr Nr Nz)
    simpleGrading (1 1 1)

/* Outlet pipe */
    // 1st quarter outlet pipe block
    hex (vlvSt0t pipe0t pipe1t vlvSt1t vlvSt0b vlvHd0t vlvHd1t vlvSt1b)
    pipe /*block 8*/
    (Nr Nr Nr)
    simpleGrading (1 1 1)

    // 2nd quarter outlet pipe block
    hex (vlvSt1t pipe1t pipe2t vlvSt2t vlvSt1b vlvHd1t vlvHd2t vlvSt2b)
    pipe /*block 9*/
    (Nr Nr Nr)
    simpleGrading (1 1 1)

    // 3rd quarter outlet pipe block
    hex (vlvSt2t pipe2t pipe3t vlvSt3t vlvSt2b vlvHd2t vlvHd3t vlvSt3b)
    pipe /*block 10*/
    (Nr Nr Nr)
    simpleGrading (1 1 1)

    // 4th quarter outlet pipe block
    hex (vlvSt3t pipe3t pipe0t vlvSt0t vlvSt3b vlvHd3t vlvHd0t vlvSt0b)
    pipe /*block 11*/
    (Nr Nr Nr)
    simpleGrading (1 1 1)

/* Inlet ports */
    // xMinus inlet port
    hex2D(inlXm0, inlXm1, inlXm2, inlXm3)
    inletXm /*block 12*/
    (Nr Nr Nr)
    simpleGrading (1 1 1)
);


edges
(
/* Cylinder */
    // Cylinder\Piston outer
    arc cylOut0b cylOut1b evert( Rcos, -Rcos, pistonInit)
    arc cylOut1b cylOut2b evert(-Rcos, -Rcos, pistonInit)
    arc cylOut2b cylOut3b evert(-Rcos,  Rcos, pistonInit)
    arc cylOut3b cylOut0b evert( Rcos,  Rcos, pistonInit)
    arc cylOut0t cylOut1t evert( Rcos, -Rcos, S)
    arc cylOut1t cylOut2t evert(-Rcos, -Rcos, S)
    arc cylOut2t cylOut3t evert(-Rcos,  Rcos, S)
    arc cylOut3t cylOut0t evert( Rcos,  Rcos, S)

    // Cylinder\Piston inner (comment to make inner block prismatic закоментировать)
    arc cylIn0b cylIn1b evert( vlvRcos, -vlvRcos, pistonInit)
    arc cylIn1b cylIn2b evert(-vlvRcos, -vlvRcos, pistonInit)
    arc cylIn2b cylIn3b evert(-vlvRcos,  vlvRcos, pistonInit)
    arc cylIn3b cylIn0b evert( vlvRcos,  vlvRcos, pistonInit)
    arc cylIn0t cylIn1t evert( vlvRcos, -vlvRcos, chS)
    arc cylIn1t cylIn2t evert(-vlvRcos, -vlvRcos, chS)
    arc cylIn2t cylIn3t evert(-vlvRcos,  vlvRcos, chS)
    arc cylIn3t cylIn0t evert( vlvRcos,  vlvRcos, chS)

/* Valve */
    // Valve head (comment to make inner block prismatic закоментировать)
    arc vlvHd0b vlvHd1b evert( vlvRcos, -vlvRcos, vlvHdBot)
    arc vlvHd1b vlvHd2b evert(-vlvRcos, -vlvRcos, vlvHdBot)
    arc vlvHd2b vlvHd3b evert(-vlvRcos,  vlvRcos, vlvHdBot)
    arc vlvHd3b vlvHd0b evert( vlvRcos,  vlvRcos, vlvHdBot)
    arc vlvHd0t vlvHd1t evert( vlvRcos, -vlvRcos, vlvHdTop)
    arc vlvHd1t vlvHd2t evert(-vlvRcos, -vlvRcos, vlvHdTop)
    arc vlvHd2t vlvHd3t evert(-vlvRcos,  vlvRcos, vlvHdTop)
    arc vlvHd3t vlvHd0t evert( vlvRcos,  vlvRcos, vlvHdTop)

    // Valve stem (comment to make inner block prismatic закоментировать)
    arc vlvSt0b vlvSt1b evert( vlvStRcos, -vlvStRcos, vlvStBot)
    arc vlvSt1b vlvSt2b evert(-vlvStRcos, -vlvStRcos, vlvStBot)
    arc vlvSt2b vlvSt3b evert(-vlvStRcos,  vlvStRcos, vlvStBot)
    arc vlvSt3b vlvSt0b evert( vlvStRcos,  vlvStRcos, vlvStBot)
    arc vlvSt0t vlvSt1t evert( vlvStRcos, -vlvStRcos, vlvStTop)
    arc vlvSt1t vlvSt2t evert(-vlvStRcos, -vlvStRcos, vlvStTop)
    arc vlvSt2t vlvSt3t evert(-vlvStRcos,  vlvStRcos, vlvStTop)
    arc vlvSt3t vlvSt0t evert( vlvStRcos,  vlvStRcos, vlvStTop)

    // Valve fillet
    arc vlvHd0t vlvSt0b evert( calc(vlvR - vlvFltRcos), 0, calc(vlvHdBot + vlvFltRcos))
    arc vlvHd1t vlvSt1b evert( 0,-calc(vlvR - vlvFltRcos), calc(vlvHdBot + vlvFltRcos))
    arc vlvHd2t vlvSt2b evert(-calc(vlvR - vlvFltRcos), 0, calc(vlvHdBot + vlvFltRcos))
    arc vlvHd3t vlvSt3b evert( 0, calc(vlvR - vlvFltRcos), calc(vlvHdBot + vlvFltRcos))

/* Outer pipe */
    arc pipe0t pipe1t evert( vlvRcos, -vlvRcos, vlvStTop)
    arc pipe1t pipe2t evert(-vlvRcos, -vlvRcos, vlvStTop)
    arc pipe2t pipe3t evert(-vlvRcos,  vlvRcos, vlvStTop)
    arc pipe3t pipe0t evert( vlvRcos,  vlvRcos, vlvStTop)

/* Inlet ports */
    arc inlXm0b inlXm3b evert(inlRcos, inlRsin, 0)
    arc inlXm0t inlXm3t evert(inlRcos, inlRsin, inlH)
);


boundary
(
/* Pathes */
    inletXm
    {
        type patch;
        faces
        (
            quad2D(inlXm1, inlXm2)
        );
    }
    outlet
    {
        type patch;
        faces
        (
            topQuad(pipe0, pipe1, vlvSt0, vlvSt1) // 1st quarter
            topQuad(pipe1, pipe2, vlvSt1, vlvSt2) // 2nd quarter
            topQuad(pipe2, pipe3, vlvSt2, vlvSt3) // 3rd quarter
            topQuad(pipe3, pipe0, vlvSt3, vlvSt0) // 4th quarter
        );
    }
/* Couples */
    innerCouple1
    {
        type patch;
        faces
        (
            quad2D(cylIn0, cylIn1) // 1st quarter
            quad2D(cylIn1, cylIn2) // 2nd quarter
            quad2D(cylIn2, cylIn3) // 3rd quarter
            quad2D(cylIn3, cylIn0) // 4th quarter
        );
    }
    innerCouple2
    {
        type patch;
        faces
        (
            // Valve patches
            (cylIn0b cylIn1b vlvHd1b vlvHd0b) // 1st quarter
            (vlvHd0t vlvHd1t pipe1t pipe0t)
            (cylIn1b cylIn2b vlvHd2b vlvHd1b) // 2nd quarter
            (vlvHd1t vlvHd2t pipe2t pipe1t)
            (cylIn2b cylIn3b vlvHd3b vlvHd2b) // 3rd quarter
            (vlvHd2t vlvHd3t pipe3t pipe2t)
            (cylIn3b cylIn0b vlvHd0b vlvHd3b) // 4th quarter
            (vlvHd3t vlvHd0t pipe0t pipe3t)
        );
    }
    outerCouple1
    {
        type patch;
        faces
        (
            quad2D(inlXm3, inlXm0) // xMinus inlet port
        );
    }
    outerCouple2
    {
        type patch;
        faces
        (
            quad2D(cylOut0, cylOut1) // 1st quarter
            quad2D(cylOut1, cylOut2) // 2nd quarter
            quad2D(cylOut2, cylOut3) // 3rd quarter
            quad2D(cylOut3, cylOut0) // 4th quarter
        );
    }
/* Walls */
    walls
    {
        type wall;
        faces
        (
            // Cyinder top walls
            topQuad(cylIn0, cylOut0, cylOut1, cylIn1) // 1st quarter
            topQuad(cylIn1, cylOut1, cylOut2, cylIn2) // 2nd quarter
            topQuad(cylIn2, cylOut2, cylOut3, cylIn3) // 3rd quarter
            topQuad(cylIn3, cylOut3, cylOut0, cylIn0) // 4th quarter

            // xMinus inlet port walls
            botQuad(inlXm0, inlXm1, inlXm2, inlXm3)
            topQuad(inlXm0, inlXm1, inlXm2, inlXm3)
            quad2D(inlXm0, inlXm1)
            quad2D(inlXm2, inlXm3)
        );
    }
    piston
    {
        type wall;
        faces
        (
            botQuad(cylIn0, cylIn1, cylIn2, cylIn3) // piston inner
            botQuad(cylIn0, cylOut0, cylOut1, cylIn1) // 1st quarter
            botQuad(cylIn1, cylOut1, cylOut2, cylIn2) // 2nd quarter
            botQuad(cylIn2, cylOut2, cylOut3, cylIn3) // 3rd quarter
            botQuad(cylIn3, cylOut3, cylOut0, cylIn0) // 4th quarter
        );
    }
    valve
    {
        type wall;
        faces
        (
            botQuad(vlvHd0, vlvHd1, vlvHd2, vlvHd3) // valve head bottom

            (vlvHd0t vlvSt0b vlvHd1t vlvSt1b) // 1st quarter of valve
            quad2D(vlvSt0, vlvSt1)
            (vlvHd1t vlvSt1b vlvHd2t vlvSt2b) // 2nd quarter of valve
            quad2D(vlvSt1, vlvSt2)
            (vlvHd2t vlvSt2b vlvHd3t vlvSt3b) // 3rd quarter of valve
            quad2D(vlvSt2, vlvSt3)
            (vlvHd3t vlvSt3b vlvHd0t vlvSt0b) // 4th quarter of valve
            quad2D(vlvSt3, vlvSt0)
        );
    }
);

// ************************************************************************* //
