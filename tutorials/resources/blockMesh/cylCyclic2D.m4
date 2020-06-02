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

// MAN 6S70ME-C8.2-GI-TII
define(theta, calc(360/24)) // Wedge/periodic angle [deg]

define(bore, 70)          // Cylinder bore
define(stroke, 280)       // Piston stroke
define(clearance, 5.75)   // Clearance to the chamfer at TDC
define(chamfer, 13.75)    // Cylinder chamfer
define(pistonInit, 92.55) // Initial piston position
define(pistonChamber, 10.4) // Piston chamber depth

define(vlvInit, 0)        // Initial valve stroke
define(vlvD, 34.5)        // Valve head diameter
define(vlvHd, 3)          // Valve head thickness
define(vlvStD, 8.25)      // Valve stem diameter
define(outletH, 40)       // Outer pipe height

define(inlW, 5.15)        // Inlet port width
define(inlH, 19.2)        // Inlet port height
define(inlL, inlW)        // Inlet port closest length from the cylinder wall
define(inlTiltXZ, 37.9)   // Inlet port tilting to the XZ plane [deg]
define(inlTiltXY, 0)      // Inlet port tilting to the XY plane [deg]

define(injW, 2)           // Injector width
define(injH, injW)        // Injector height
define(injL, inlL)        // Injector length from the cylinder wall
define(injz, 159.4)       // Distance from the injector to the bottom of
                          // the inlet port outlet patch


define(Nr, 2)             // Number of cells in the radius dimension
define(Nz, 50)            // Number of cells in the length dimension

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
// Derived parameters

/* Cylinder */
define(S, calc(stroke + clearance))        // Cylinder Z size
define(R, calc(bore/2))                    // Cylinder radius
define(Rsin, calc(R*sind(theta)))          // Cylinder radius middle point

define(chS, calc(chamfer + S))             // Cylinder Z size with chamfer
define(pistonChamberZ, calc(pistonInit - pistonChamber)) // Piston chamber Z coordinate


/* Valve */
define(vlvR, calc(vlvD/2))                 // Valve radius
define(vlvRsin, calc(vlvR*sind(theta)))    // Valve radius middle point

define(vlvStR, calc(vlvStD/2))             // Valve stem radius
define(vlvStRsin, calc(vlvStR*sind(theta/2))) // Valve stem radius middle point

define(vlvFltR, calc(vlvR - vlvStR))       // Valve fillet radius
define(vlvHdTop, calc(chS - vlvInit))      // Valve head top Z coordinate
define(vlvHdBot, calc(vlvHdTop - vlvHd))   // Valve head bottom Z coordinate
define(vlvStBot, calc(vlvHdTop + vlvFltR)) // Valve stem bottom Z coordinate
define(vlvStTop, calc(S + outletH))        // Valve stem & outer pipe top Z coordinate
define(vlvFltRcos, calc(vlvStR + vlvFltR*(1 - cosd(45)))) // Valve fillet
                                           // radius middle point X coordinate
define(vlvFltRSym, calc(vlvFltRcos*sind(theta/2))) // Valve fillet radius
                                           // middle point Y coordinate
define(vlvFltRZcos, calc(vlvHdTop + vlvFltR*(1 - cosd(45)))) // Valve fillet
                                           //radius middle point Z coordinate


/* Inlet port */
define(inlWHf, calc(inlW/2))               // Inlet port width half
define(inlLt, calc(inlH*sind(inlTiltXY)*cosd(inlTiltXY) + inlL))

//- Inlet patch bottom
define(inlLbx, calc((inlL - inlWHf*sind(inlTiltXZ))*cosd(inlTiltXZ) + R))
define(inlRbx, calc((inlL + inlWHf*sind(inlTiltXZ))*cosd(inlTiltXZ) + R))
define(inlLby, calc((inlL - inlWHf*sind(inlTiltXZ))*sind(inlTiltXZ) + inlWHf*cosd(inlTiltXZ)))
define(inlRby, calc((inlL + inlWHf*sind(inlTiltXZ))*sind(inlTiltXZ) - inlWHf*cosd(inlTiltXZ)))

//- Inlet patch top
define(inlLtx, calc((inlLt - inlWHf*sind(inlTiltXZ))*cosd(inlTiltXZ) + R))
define(inlRtx, calc((inlLt + inlWHf*sind(inlTiltXZ))*cosd(inlTiltXZ) + R))
define(inlLty, calc((inlLt - inlWHf*sind(inlTiltXZ))*sind(inlTiltXZ) + inlWHf*cosd(inlTiltXZ)))
define(inlRty, calc((inlLt + inlWHf*sind(inlTiltXZ))*sind(inlTiltXZ) - inlWHf*cosd(inlTiltXZ)))

define(inlz, calc(inlL*sind(inlTiltXY)))   // Inlet patch lower Z coordinate
define(inlHz, calc(inlH*sqr(cosd(inlTiltXY)) - inlz)) // Inlet patch upper 
                                           // Z coordinate


/* Injectors */
define(injWHf, calc(injW/2))               // Injector width half
define(injx, calc(R + injL))               // Injector patch coordinate
define(injRmW, calc(sqrt(sqr(R) - sqr(injW)))) // Injector outlet patch X point
define(injHz, calc(injz + injH))           // Injector top coordinate

define(Nr2, calc(Nr*2))

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
// Parametric description

vertices
(
/* Cylinder */
    // Cylinder\Piston inner
    /*00*/ vert(vlvR,  vlvRsin, pistonChamberZ) vlabel(cylIn0b)
    /*01*/ vert(vlvR, -vlvRsin, pistonChamberZ) vlabel(cylIn1b)
    /*02*/ vert(0,     0,       pistonChamberZ) vlabel(cylIn2b)
    /*03*/ vert(vlvR,  vlvRsin, chS)            vlabel(cylIn0t)
    /*04*/ vert(vlvR, -vlvRsin, chS)            vlabel(cylIn1t)

    // Cylinder\Piston outer
    /*05*/ vert(R,  Rsin, pistonInit) vlabel(cylOut0b) 
    /*06*/ vert(R, -Rsin, pistonInit) vlabel(cylOut1b)
    /*07*/ vert(R,  Rsin, S) vlabel(cylOut0t)
    /*08*/ vert(R, -Rsin, S) vlabel(cylOut1t)

/* Valve */
    // Valve head
    /*09*/ vert(vlvR,  vlvRsin, vlvHdBot) vlabel(vlvHd0b)
    /*10*/ vert(vlvR, -vlvRsin, vlvHdBot) vlabel(vlvHd1b)
    /*11*/ vert(0,     0,       vlvHdBot) vlabel(vlvHd2b)
    /*12*/ vert(vlvR,  vlvRsin, vlvHdTop) vlabel(vlvHd0t)
    /*13*/ vert(vlvR, -vlvRsin, vlvHdTop) vlabel(vlvHd1t)

    // Valve stem
    /*14*/ vert(vlvStR,  vlvStRsin, vlvStBot) vlabel(vlvSt0b)
    /*15*/ vert(vlvStR, -vlvStRsin, vlvStBot) vlabel(vlvSt1b)
    /*16*/ vert(vlvStR,  vlvStRsin, vlvStTop) vlabel(vlvSt0t)
    /*17*/ vert(vlvStR, -vlvStRsin, vlvStTop) vlabel(vlvSt1t)

/* Outer pipe */
    /*18*/ vert(vlvR,  vlvRsin, vlvStTop) vlabel(pipe0t)
    /*19*/ vert(vlvR, -vlvRsin, vlvStTop) vlabel(pipe1t)

/* Inlet port */
    /*20*/ vert(R,       inlWHf,  0)     vlabel(inlXm0b)
    /*21*/ vert(inlLbx,  inlLby, -inlz)  vlabel(inlXm1b)
    /*22*/ vert(inlRbx,  inlRby, -inlz)  vlabel(inlXm2b)
    /*23*/ vert(R,      -inlWHf,  0)     vlabel(inlXm3b)
    /*24*/ vert(R,       inlWHf,  inlH)  vlabel(inlXm0t)
    /*25*/ vert(inlLtx,  inlLty,  inlHz) vlabel(inlXm1t)
    /*26*/ vert(inlRtx,  inlRty,  inlHz) vlabel(inlXm2t)
    /*27*/ vert(R,      -inlWHf,  inlH)  vlabel(inlXm3t)

/* Injectors */
    /*28*/ vert(R,     injWHf, injz)  vlabel(injXm0b)
    /*29*/ vert(injx,  injWHf, injz)  vlabel(injXm1b)
    /*30*/ vert(injx, -injWHf, injz)  vlabel(injXm2b)
    /*31*/ vert(R,    -injWHf, injz)  vlabel(injXm3b)
    /*32*/ vert(R,     injWHf, injHz) vlabel(injXm0t)
    /*33*/ vert(injx,  injWHf, injHz) vlabel(injXm1t)
    /*34*/ vert(injx, -injWHf, injHz) vlabel(injXm2t)
    /*35*/ vert(R,    -injWHf, injHz) vlabel(injXm3t)
);


blocks
(
/* Cylinder */
    // Inner cylinder
    hex (vlvHd0b vlvHd1b vlvHd2b vlvHd2b cylIn0b cylIn1b cylIn2b cylIn2b)
    cylinder /*block 0*/
    (1 Nr Nz)
    simpleGrading (1 1.2 1.2)

    // Outer cylinder
    hex2D(cylIn0, cylOut0, cylOut1, cylIn1)
    cylinder /*block 1*/
    (Nr Nr Nz)
    simpleGrading (1 1 1)

/* Outlet pipe */
    // outlet pipe block
    hex (vlvSt0t pipe0t pipe1t vlvSt1t vlvSt0b vlvHd0t vlvHd1t vlvSt1b)
    pipe /*block 2*/
    (Nr2 2 Nr2)
    simpleGrading (0.5 1 0.75)

/* Inlet port */
    // xMinus inlet port
    hex2D(inlXm0, inlXm1, inlXm2, inlXm3)
    inlet /*block 3*/
    (Nr Nr Nr2)
    simpleGrading (1 1 1)

/* Injectors */
    // xMinus injector
    hex2D(injXm0, injXm1, injXm2, injXm3)
    injector /*block 4*/
    (2 1 1)
    simpleGrading (1 1 1)
);


edges
(
    // Valve fillet
    arc vlvHd0t vlvSt0b evert(vlvFltRcos,  vlvFltRSym, vlvFltRZcos)
    arc vlvHd1t vlvSt1b evert(vlvFltRcos, -vlvFltRSym, vlvFltRZcos)
);


boundary
(
/* Pathes */
    inlet
    {
        type            patch;
        faces           (quad2D(inlXm1, inlXm2));
    }
    injection
    {
        type            patch;
        faces           (quad2D(injXm1, injXm2));
    }
    outlet
    {
        type            patch;
        faces           (topQuad(pipe0, pipe1, vlvSt0, vlvSt1));
    }
    axis
    {
        type            patch;
        faces           ((cylIn2b vlvHd2b vlvHd2b cylIn2b));
    }

/* Couples */
    //- ACMIs
    innerCouple1
    {
        type            patch;
        faces           (quad2D(cylIn0, cylIn1));
    }
    innerCouple2
    {
        type            patch;
        faces
        (
            // Valve patches
            (cylIn0b cylIn1b vlvHd1b vlvHd0b) // cylinder
            (vlvHd0t vlvHd1t pipe1t  pipe0t) // outer pipe
        );
    }
    outerCouple1
    {
        type            patch;
        faces
        (
            quad2D(inlXm3, inlXm0) // inlet port outlet
            quad2D(injXm3, injXm0) // injector outlet
        );
    }
    outerCouple2
    {
        type            patch;
        faces           (quad2D(cylOut0, cylOut1));
    }

    //- Cyclic
    cyclicBack
    {
        type            cyclic;
        neighbourPatch  cyclicFront;
        matchTolerance  0.00035;
        faces
        (
            botQuad(cylIn0, cylIn2, vlvHd2, vlvHd0) // inner cylinder
            quad2D(cylIn0, cylOut0) // outer cylinder
            (vlvSt0t pipe0t vlvSt0b vlvHd0t) // outer pipe
        );
    }
    cyclicFront
    {
        type            cyclic;
        neighbourPatch  cyclicBack;
        matchTolerance  0.00035;
        faces
        (
            botQuad(cylIn1, cylIn2, vlvHd2, vlvHd1) // inner cylinder
            quad2D(cylIn1, cylOut1) // outer cylinder
            (vlvSt1t pipe1t vlvSt1b vlvHd1t) // outer pipe
        );
    }

/* Walls */
    walls
    {
        type            wall;
        faces
        (
            // Cyinder top walls
            topQuad(cylIn0, cylOut0, cylOut1, cylIn1) // quarter

            // Inlet port walls
            botQuad(inlXm0, inlXm1, inlXm2, inlXm3)
            topQuad(inlXm0, inlXm1, inlXm2, inlXm3)
            quad2D(inlXm0, inlXm1)
            quad2D(inlXm2, inlXm3)

            // Injector walls
            botQuad(injXm0, injXm1, injXm2, injXm3)
            topQuad(injXm0, injXm1, injXm2, injXm3)
            quad2D(injXm0, injXm1)
            quad2D(injXm2, injXm3)
        );
    }
    piston
    {
        type            wall;
        faces
        (
            botQuad(cylIn0, cylIn1,  cylIn2,  cylIn2) // piston inner
            botQuad(cylIn0, cylOut0, cylOut1, cylIn1) // quarter
        );
    }
    valveHead
    {
        type            wall;
        faces
        (
            botQuad(vlvHd0, vlvHd1, vlvHd2, vlvHd2) // valve head bottom

            (vlvHd0t vlvSt0b vlvHd1t vlvSt1b) // quarter of valve head
        );
    }
    valveStem
    {
        type            wall;
        faces           (quad2D(vlvSt0, vlvSt1)); // quarter of valve stem
    }
);

mergePatchPairs
(
);

// ************************************************************************* //
