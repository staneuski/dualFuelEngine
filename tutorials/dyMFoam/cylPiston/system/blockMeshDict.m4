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
define(sqr, $1**2)

define(hex2D, hex ($1t $2t $3t $4t $1b $2b $3b $4b))
define(quad2D, ($1b $2b $2t $1t))
define(topQuad, ($1t $2t $4t $3t))
define(botQuad, ($1b $2b $4b $3b))

define(vert,  ($1 $2 $3))
define(evert, ($1 $2 $3))

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
// User-defined parameters

convertToMeters 0.01;

define(D, 70)             // Cylinder bore
define(S, 300)            // Cylinder Z size (> piston stroke)
define(chamfer, 15)       // Cylinder chamfer
define(pistonInit, 92.55) // Initial piston position

define(vlvS, 0)           // Initial valve stroke
define(vlvD, calc(D/2))   // Valve head diameter
define(vlvHd, 3)          // Valve head thickness
define(vlvStD, 8)         // Valve stem diameter
define(outletH, 50)       // Outer pipe height

define(inlW, 15)          // Inlet port width
define(inlH, 25)          // Inlet port height
define(inlL, 10)          // Inlet port length from the cylinder wall

define(injW, 2.5)         // Injector width
define(injH, 2.5)         // Injector height
define(injL, 10)          // Injector length from the cylinder wall
define(injZ, 180)         // Distance from the injector to the bottom of inlet port

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
/*FIXME arc middle point is incorrect for (inl|inj)W < 10*/
define(inlRL, calc(R + inlL))              // Inlet patch coordinate
define(inlRmW, calc(sqrt(sqr(R) - sqr(inlW)))) // Inlet port outlet patch X point
define(inlRcos, calc(sqrt(sqr(R) - sqr(inlW/2)))) // Inlet port outlet patch X middle point
define(inlRsin, calc(inlL/2))              // Inlet port outlet patch Y middle point

/* Injectors */
define(injRL, calc(R + injL))              // Injector patch coordinate
define(injRmW, calc(sqrt(sqr(R) - sqr(injW)))) // Injector outlet patch X point
define(injRcos, calc(sqrt(sqr(R) - sqr(injW/2)))) // Injector outlet patch X middle point
define(injRsin, calc(injL/2))              // Injector outlet patch Y middle point
define(injZH, calc(injZ + injH))           // Injector top coordinate

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
    /*36*/ vert(inlRmW, inlW, 0)    vlabel(inlXm0b)
    /*37*/ vert(inlRL,  inlW, 0)    vlabel(inlXm1b)
    /*38*/ vert(inlRL,  0,    0)    vlabel(inlXm2b)
    /*39*/ vert(R,      0,    0)    vlabel(inlXm3b)
    /*40*/ vert(inlRmW, inlW, inlH) vlabel(inlXm0t)
    /*41*/ vert(inlRL,  inlW, inlH) vlabel(inlXm1t)
    /*42*/ vert(inlRL,  0,    inlH) vlabel(inlXm2t)
    /*43*/ vert(R,      0,    inlH) vlabel(inlXm3t)
    // xPlus inlet port
    /*44*/ vert(-inlRmW, -inlW, 0)    vlabel(inlXp0b)
    /*45*/ vert(-inlRL,  -inlW, 0)    vlabel(inlXp1b)
    /*46*/ vert(-inlRL,   0,    0)    vlabel(inlXp2b)
    /*47*/ vert(-R,       0,    0)    vlabel(inlXp3b)
    /*48*/ vert(-inlRmW, -inlW, inlH) vlabel(inlXp0t)
    /*49*/ vert(-inlRL,  -inlW, inlH) vlabel(inlXp1t)
    /*50*/ vert(-inlRL,   0,    inlH) vlabel(inlXp2t)
    /*51*/ vert(-R,       0,    inlH) vlabel(inlXp3t)

    // yMinus inlet port
    /*52*/ vert(-inlW, inlRmW, 0)    vlabel(inlYm0b)
    /*53*/ vert(-inlW, inlRL,  0)    vlabel(inlYm1b)
    /*54*/ vert(0,     inlRL,  0)    vlabel(inlYm2b)
    /*55*/ vert(0,     R,      0)    vlabel(inlYm3b)
    /*56*/ vert(-inlW, inlRmW, inlH) vlabel(inlYm0t)
    /*57*/ vert(-inlW, inlRL,  inlH) vlabel(inlYm1t)
    /*58*/ vert(0,     inlRL,  inlH) vlabel(inlYm2t)
    /*59*/ vert(0,     R,      inlH) vlabel(inlYm3t)
    // yPlus inlet port
    /*60*/ vert(inlW, -inlRmW, 0)    vlabel(inlYp0b)
    /*61*/ vert(inlW, -inlRL,  0)    vlabel(inlYp1b)
    /*62*/ vert(0,    -inlRL,  0)    vlabel(inlYp2b)
    /*63*/ vert(0,    -R,      0)    vlabel(inlYp3b)
    /*64*/ vert(inlW, -inlRmW, inlH) vlabel(inlYp0t)
    /*65*/ vert(inlW, -inlRL,  inlH) vlabel(inlYp1t)
    /*66*/ vert(0,    -inlRL,  inlH) vlabel(inlYp2t)
    /*67*/ vert(0,    -R,      inlH) vlabel(inlYp3t)

/* Injectors */
    // xMinus injector
    /*67*/ vert(injRmW, injW, injZ)  vlabel(injXm0b)
    /*68*/ vert(injRL,  injW, injZ)  vlabel(injXm1b)
    /*69*/ vert(injRL,  0,    injZ)  vlabel(injXm2b)
    /*70*/ vert(R,      0,    injZ)  vlabel(injXm3b)
    /*70*/ vert(injRmW, injW, injZH) vlabel(injXm0t)
    /*71*/ vert(injRL,  injW, injZH) vlabel(injXm1t)
    /*72*/ vert(injRL,  0,    injZH) vlabel(injXm2t)
    /*73*/ vert(R,      0,    injZH) vlabel(injXm3t)
    
    // xPlus injector
    /*74*/ vert(-injRmW, -injW, injZ)  vlabel(injXp0b)
    /*75*/ vert(-injRL,  -injW, injZ)  vlabel(injXp1b)
    /*76*/ vert(-injRL,   0,    injZ)  vlabel(injXp2b)
    /*77*/ vert(-R,       0,    injZ)  vlabel(injXp3b)
    /*78*/ vert(-injRmW, -injW, injZH) vlabel(injXp0t)
    /*79*/ vert(-injRL,  -injW, injZH) vlabel(injXp1t)
    /*80*/ vert(-injRL,   0,    injZH) vlabel(injXp2t)
    /*81*/ vert(-R,       0,    injZH) vlabel(injXp3t)
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
    // xPlus inlet port
    hex2D(inlXp0, inlXp1, inlXp2, inlXp3)
    inletXp /*block 13*/
    (Nr Nr Nr)
    simpleGrading (1 1 1)

    // yMinus inlet port
    hex2D(inlYm0, inlYm1, inlYm2, inlYm3)
    inletYm /*block 14*/
    (Nr Nr Nr)
    simpleGrading (1 1 1)

    // yPlus inlet port
    hex2D(inlYp0, inlYp1, inlYp2, inlYp3)
    inletYp /*block 14*/
    (Nr Nr Nr)
    simpleGrading (1 1 1)

/* Injectors */
    // xMinus injector
    hex2D(injXm0, injXm1, injXm2, injXm3)
    injectorXm /*block 15*/
    (2 1 1)
    simpleGrading (1 1 1)
    // xPlus injector
    hex2D(injXp0, injXp1, injXp2, injXp3)
    injectorXp /*block 16*/
    (2 1 1)
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

    // Cylinder\Piston inner (comment to make inner block prismatic)
    arc cylIn0b cylIn1b evert( vlvRcos, -vlvRcos, pistonInit)
    arc cylIn1b cylIn2b evert(-vlvRcos, -vlvRcos, pistonInit)
    arc cylIn2b cylIn3b evert(-vlvRcos,  vlvRcos, pistonInit)
    arc cylIn3b cylIn0b evert( vlvRcos,  vlvRcos, pistonInit)
    arc cylIn0t cylIn1t evert( vlvRcos, -vlvRcos, chS)
    arc cylIn1t cylIn2t evert(-vlvRcos, -vlvRcos, chS)
    arc cylIn2t cylIn3t evert(-vlvRcos,  vlvRcos, chS)
    arc cylIn3t cylIn0t evert( vlvRcos,  vlvRcos, chS)

/* Valve */
    // Valve head (comment to make inner block prismatic)
    arc vlvHd0b vlvHd1b evert( vlvRcos, -vlvRcos, vlvHdBot)
    arc vlvHd1b vlvHd2b evert(-vlvRcos, -vlvRcos, vlvHdBot)
    arc vlvHd2b vlvHd3b evert(-vlvRcos,  vlvRcos, vlvHdBot)
    arc vlvHd3b vlvHd0b evert( vlvRcos,  vlvRcos, vlvHdBot)
    arc vlvHd0t vlvHd1t evert( vlvRcos, -vlvRcos, vlvHdTop)
    arc vlvHd1t vlvHd2t evert(-vlvRcos, -vlvRcos, vlvHdTop)
    arc vlvHd2t vlvHd3t evert(-vlvRcos,  vlvRcos, vlvHdTop)
    arc vlvHd3t vlvHd0t evert( vlvRcos,  vlvRcos, vlvHdTop)

    // Valve stem (comment to make inner block prismatic)
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
    // xMinus inlet port outlet patch
    arc inlXm0b inlXm3b evert(inlRcos, inlRsin, 0)
    arc inlXm0t inlXm3t evert(inlRcos, inlRsin, inlH)
    // xPlus inlet port outlet patch
    arc inlXp0b inlXp3b evert(-inlRcos, -inlRsin, 0)
    arc inlXp0t inlXp3t evert(-inlRcos, -inlRsin, inlH)

    // yMinus inlet port outlet patch
    arc inlYm0b inlYm3b evert(-inlRsin, inlRcos, 0)
    arc inlYm0t inlYm3t evert(-inlRsin, inlRcos, inlH)
    // yPlus inlet port outlet patch
    arc inlYp0b inlYp3b evert(inlRsin, -inlRcos, 0)
    arc inlYp0t inlYp3t evert(inlRsin, -inlRcos, inlH)

/* Injectors */
    // // xMinus injector outlet patch
    // arc injXm0b injXm3b evert(injRcos, injRsin, injZ)
    // arc injXm0t injXm3t evert(injRcos, injRsin, injZH)
    // // xPlus injector outlet patch
    // arc injXp0b injXp3b evert(-injRcos, -injRsin, injZ)
    // arc injXp0t injXp3t evert(-injRcos, -injRsin, injZH)
);


boundary
(
/* Pathes */
    inletXm
    {
        type            patch;
        faces           (quad2D(inlXm1, inlXm2));
    }
    inletXp
    {
        type            patch;
        faces           (quad2D(inlXp1, inlXp2));
    }
    inletYm
    {
        type            patch;
        faces           (quad2D(inlYm1, inlYm2));
    }
    inletYp
    {
        type            patch;
        faces           (quad2D(inlYp1, inlYp2));
    }
    injectionXm
    {
        type            patch;
        faces           (quad2D(injXm1, injXm2));
    }
    injectionXp
    {
        type            patch;
        faces           (quad2D(injXp1, injXp2));
    }
    outlet
    {
        type            patch;
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
        type            patch;
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
        type            patch;
        faces
        (
            // Valve patches
            (cylIn0b cylIn1b vlvHd1b vlvHd0b) // 1st quarter
            (vlvHd0t vlvHd1t pipe1t  pipe0t)
            (cylIn1b cylIn2b vlvHd2b vlvHd1b) // 2nd quarter
            (vlvHd1t vlvHd2t pipe2t  pipe1t)
            (cylIn2b cylIn3b vlvHd3b vlvHd2b) // 3rd quarter
            (vlvHd2t vlvHd3t pipe3t  pipe2t)
            (cylIn3b cylIn0b vlvHd0b vlvHd3b) // 4th quarter
            (vlvHd3t vlvHd0t pipe0t  pipe3t)
        );
    }
    outerCouple1
    {
        type            patch;
        faces
        (
            quad2D(inlXm3, inlXm0) // xMinus inlet port outlet
            quad2D(inlXp3, inlXp0) // xPlus inlet port outlet
            quad2D(inlYm3, inlYm0) // yMinus inlet port outlet
            quad2D(inlYp3, inlYp0) // yMinus inlet port outlet

            quad2D(injXm3, injXm0) // xMinus injector outlet
            quad2D(injXp3, injXp0) // xPlus injector outlet
        );
    }
    outerCouple2
    {
        type            patch;
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
        type            wall;
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
            // xPlus inlet port walls
            botQuad(inlXp0, inlXp1, inlXp2, inlXp3)
            topQuad(inlXp0, inlXp1, inlXp2, inlXp3)
            quad2D(inlXp0, inlXp1)
            quad2D(inlXp2, inlXp3)

            // yMinus inlet port walls
            botQuad(inlYm0, inlYm1, inlYm2, inlYm3)
            topQuad(inlYm0, inlYm1, inlYm2, inlYm3)
            quad2D(inlYm0, inlYm1)
            quad2D(inlYm2, inlYm3)
            // yPlus inlet port walls
            botQuad(inlYp0, inlYp1, inlYp2, inlYp3)
            topQuad(inlYp0, inlYp1, inlYp2, inlYp3)
            quad2D(inlYp0, inlYp1)
            quad2D(inlYp2, inlYp3)

            // xMinus injector walls
            botQuad(injXm0, injXm1, injXm2, injXm3)
            topQuad(injXm0, injXm1, injXm2, injXm3)
            quad2D(injXm0, injXm1)
            quad2D(injXm2, injXm3)
            // xPlus injector walls
            botQuad(injXp0, injXp1, injXp2, injXp3)
            topQuad(injXp0, injXp1, injXp2, injXp3)
            quad2D(injXp0, injXp1)
            quad2D(injXp2, injXp3)
        );
    }
    piston
    {
        type            wall;
        faces
        (
            botQuad(cylIn0, cylIn1,  cylIn2,  cylIn3) // piston inner
            botQuad(cylIn0, cylOut0, cylOut1, cylIn1) // 1st quarter
            botQuad(cylIn1, cylOut1, cylOut2, cylIn2) // 2nd quarter
            botQuad(cylIn2, cylOut2, cylOut3, cylIn3) // 3rd quarter
            botQuad(cylIn3, cylOut3, cylOut0, cylIn0) // 4th quarter
        );
    }
    /*FIXME Valve stem moves the edge of the outlet patch*/
    valve
    {
        type            wall;
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
