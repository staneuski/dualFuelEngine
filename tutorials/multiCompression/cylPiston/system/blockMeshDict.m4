/*--------------------------------*- C++ -*----------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     | Website:  https://openfoam.org
    \\  /    A nd           | Version:  6
     \\/     M anipulation  |
\*---------------------------------------------------------------------------*/
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      blockMeshDict;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
// General m4 macros

changecom(//)changequote([,])
define(calc, [esyscmd(perl -e 'print ($1)')])
define(VCOUNT, 0)
define(vlabel, [[// ]Vertex $1 = VCOUNT define($1, VCOUNT)define([VCOUNT], incr(VCOUNT))])

define(PI, 3.14159265)
define(sind, sin((PI/180)*$1))
define(cosd, cos((PI/180)*$1))

define(hex2D, hex ($1Up $2Up $3Up $4Up $1Down $2Down $3Down $4Down))
define(upQuad, ($1Up $2Up $4Up $3Up))
define(downQuad, ($1Down $2Down $4Down $3Down))
define(sideQuad, ($1Down $2Down $2Up $1Up))

define(vert,  ($1 $2 $3))
define(evert, ($1 $2 $3))

// ########################################################################## //
// USER EDITABLE PART

convertToMeters     0.01;

define(D, 		    70) // cylinder bore

define(S, 	  	    280) // piston stroke

define(chamfer,     0) // cylinder chamfer

define(meshSize,    5) // relative to S & D

define(valveStroke, 15) // valve stroke

define(valveHead,   5) // valve head thickness

define(valveStemD,  10)

define(outletH,     40)

// END OF (NORMAL) USER EDITABLE PART
// ########################################################################## //

define(R,		  calc( D/2.0 ))

define(Rcos,	  calc( R*cosd(45.0) ))

define(innerR,	  calc( D/4.0 )) // also valve head diameter

define(innerRcos, calc( innerR*cosd(45.0) ))
	

define(valveFilletR, calc(innerR - valveStemD/2.0))

define(valveFilletRcos, calc(valveFilletR*cosd(45.0)))


define(rMeshSize, calc( R/meshSize ))

define(zMeshSize, calc( S/meshSize ))

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
	
vertices
(
	// Cylinder
		// Inner of piston
		/*00*/ vert(innerR,  0,      0) vlabel(cylIn0Down)
		/*01*/ vert(0,      -innerR, 0) vlabel(cylIn1Down)
		/*02*/ vert(-innerR, 0,      0) vlabel(cylIn2Down)
		/*03*/ vert(0,       innerR, 0) vlabel(cylIn3Down)
		
		// Outer of piston
		/*04*/ vert(R,  0, 0) vlabel(cylOut0Down)
		/*05*/ vert(0, -R, 0) vlabel(cylOut1Down)
		/*06*/ vert(-R, 0, 0) vlabel(cylOut2Down)
		/*07*/ vert(0,  R, 0) vlabel(cylOut3Down)
		
		// Upper inner cylinder
		/*08*/ vert(innerR,  0,      calc(S + chamfer)) vlabel(cylIn0Up)
		/*09*/ vert(0,      -innerR, calc(S + chamfer)) vlabel(cylIn1Up)
		/*10*/ vert(-innerR, 0,      calc(S + chamfer)) vlabel(cylIn2Up)
		/*11*/ vert(0,       innerR, calc(S + chamfer)) vlabel(cylIn3Up)
		
		// Upper of cylinder
		/*12*/ vert(R,  0, S) vlabel(cylOut0Up)
		/*13*/ vert(0, -R, S) vlabel(cylOut1Up)
		/*14*/ vert(-R, 0, S) vlabel(cylOut2Up)
		/*15*/ vert(0,  R, S) vlabel(cylOut3Up)

	// Valve
		// Valve head bottom
		/*16*/ vert(innerR,  0,      calc((S + chamfer) - valveStroke)) vlabel(valveHead0Down)
		/*17*/ vert(0,      -innerR, calc((S + chamfer) - valveStroke)) vlabel(valveHead1Down)
		/*18*/ vert(-innerR, 0,      calc((S + chamfer) - valveStroke)) vlabel(valveHead2Down)
		/*19*/ vert(0,       innerR, calc((S + chamfer) - valveStroke)) vlabel(valveHead3Down)

		// Valve head upper
		/*20*/ vert(innerR,  0,      calc((S + chamfer) - valveStroke + valveHead)) vlabel(valveHead0Up)
		/*21*/ vert(0,      -innerR, calc((S + chamfer) - valveStroke + valveHead)) vlabel(valveHead1Up)
		/*22*/ vert(-innerR, 0,      calc((S + chamfer) - valveStroke + valveHead)) vlabel(valveHead2Up)
		/*23*/ vert(0,       innerR, calc((S + chamfer) - valveStroke + valveHead)) vlabel(valveHead3Up)

		// Valve stem lower
		/*24*/ vert(calc(valveStemD/2.0),   0,                    calc((S + chamfer) - valveStroke + valveFilletR)) vlabel(valveStem0Down)
		/*25*/ vert(0,                     -calc(valveStemD/2.0), calc((S + chamfer) - valveStroke + valveFilletR)) vlabel(valveStem1Down)
		/*26*/ vert(-calc(valveStemD/2.0),  0,                    calc((S + chamfer) - valveStroke + valveFilletR)) vlabel(valveStem2Down)
		/*27*/ vert(0,                      calc(valveStemD/2.0), calc((S + chamfer) - valveStroke + valveFilletR)) vlabel(valveStem3Down)
		
		// Valve stem upper
		/*28*/ vert(calc(valveStemD/2.0),   0,                    calc((S + chamfer) + outletH)) vlabel(valveStem0Up)
		/*29*/ vert(0,                     -calc(valveStemD/2.0), calc((S + chamfer) + outletH)) vlabel(valveStem1Up)
		/*30*/ vert(-calc(valveStemD/2.0),  0,                    calc((S + chamfer) + outletH)) vlabel(valveStem2Up)
		/*31*/ vert(0,                      calc(valveStemD/2.0), calc((S + chamfer) + outletH)) vlabel(valveStem3Up)

	// Outer pipe
		/*32*/ vert(innerR,   0,      calc(S + outletH)) vlabel(pipe0Up)
		/*33*/ vert(0,       -innerR, calc(S + outletH)) vlabel(pipe1Up)
		/*34*/ vert(-innerR,  0,      calc(S + outletH)) vlabel(pipe2Up)
		/*35*/ vert(0,        innerR, calc(S + outletH)) vlabel(pipe3Up) 
);

blocks
(
	// Cylinder
		// Inner cylinder block (8 9 10 11 0 1 2 3)
		hex (valveHead0Down valveHead1Down valveHead2Down valveHead3Down cylIn0Down cylIn1Down cylIn2Down cylIn3Down)
		cylinder /*block 0*/
		(rMeshSize rMeshSize calc(zMeshSize - valveStroke/meshSize))
		simpleGrading (1 1 1)

		// 1st quarter of cylinder (8 12 13 9 0 4 5 1)
		hex2D(cylIn0, cylOut0, cylOut1, cylIn1)
		cylinder /*block 1*/
		(rMeshSize rMeshSize zMeshSize)
		simpleGrading (1 1 1)

		// 2nd quarter of cylinder (9 13 14 10 1 5 6 2)
		hex2D(cylIn1, cylOut1, cylOut2, cylIn2)
		cylinder /*block 2*/
		(rMeshSize rMeshSize zMeshSize)
		simpleGrading (1 1 1)

		// 3rd quarter of cylinder (10 14 15 11 2 6 7 3)
		hex2D(cylIn2, cylOut2, cylOut3, cylIn3)
		cylinder /*block 3*/
		(rMeshSize rMeshSize zMeshSize)
		simpleGrading (1 1 1)

		// 4th quarter of cylinder (11 15 12 8 3 7 4 0)
		hex2D(cylIn3, cylOut3, cylOut0, cylIn0)
		cylinder /*block 4*/
		(rMeshSize rMeshSize zMeshSize)
		simpleGrading (1 1 1)

	// Outer pipe
		// 1st quarter of the (outer) pipe
		hex (valveStem0Up pipe0Up pipe1Up valveStem1Up valveStem0Down valveHead0Up valveHead1Up valveStem1Down)
		pipe /*block 8*/
		(rMeshSize rMeshSize 10)
		simpleGrading (1 1 1)

		// 2nd quarter of the (outer) pipe
		hex (valveStem1Up pipe1Up pipe2Up valveStem2Up valveStem1Down valveHead1Up valveHead2Up valveStem2Down)
		pipe /*block 9*/
		(rMeshSize rMeshSize 10)
		simpleGrading (1 1 1)

		// 3rd quarter of the (outer) pipe
		hex (valveStem2Up pipe2Up pipe3Up valveStem3Up valveStem2Down valveHead2Up valveHead3Up valveStem3Down)
		pipe /*block 10*/
		(rMeshSize rMeshSize 10)
		simpleGrading (1 1 1)

		// 4th quarter of the (outer) pipe
		hex (valveStem3Up pipe3Up pipe0Up valveStem0Up valveStem3Down valveHead3Up valveHead0Up valveStem0Down)
		pipe /*block 11*/
		(rMeshSize rMeshSize 10)
		simpleGrading (1 1 1)
);

edges
(
	// Cylinder
		// Bottom of cylinder
		arc cylOut0Down cylOut1Down evert( Rcos, -Rcos, 0)
		arc cylOut1Down cylOut2Down evert(-Rcos, -Rcos, 0)
		arc cylOut2Down cylOut3Down evert(-Rcos,  Rcos, 0)
		arc cylOut3Down cylOut0Down evert( Rcos,  Rcos, 0)

		// Inner of piston (comment to make inner block as prism)
		arc cylIn0Down cylIn1Down evert( innerRcos, -innerRcos, 0)
		arc cylIn1Down cylIn2Down evert(-innerRcos, -innerRcos, 0)
		arc cylIn2Down cylIn3Down evert(-innerRcos,  innerRcos, 0)
		arc cylIn3Down cylIn0Down evert( innerRcos,  innerRcos, 0)

		// Upper of upper wall
		arc cylOut0Up cylOut1Up evert( Rcos, -Rcos, S)
		arc cylOut1Up cylOut2Up evert(-Rcos, -Rcos, S)
		arc cylOut2Up cylOut3Up evert(-Rcos,  Rcos, S)
		arc cylOut3Up cylOut0Up evert( Rcos,  Rcos, S)

		// Inner of upper wall (comment to make inner block as prism)
		arc cylIn0Up cylIn1Up evert( innerRcos, -innerRcos, calc(S + chamfer))
		arc cylIn1Up cylIn2Up evert(-innerRcos, -innerRcos, calc(S + chamfer))
		arc cylIn2Up cylIn3Up evert(-innerRcos,  innerRcos, calc(S + chamfer))
		arc cylIn3Up cylIn0Up evert( innerRcos,  innerRcos, calc(S + chamfer))

	// Valve
		// Valve head bottom
		arc valveHead0Down valveHead1Down evert( innerRcos, -innerRcos, calc(S + chamfer - valveStroke))
		arc valveHead1Down valveHead2Down evert(-innerRcos, -innerRcos, calc(S + chamfer - valveStroke))
		arc valveHead2Down valveHead3Down evert(-innerRcos,  innerRcos, calc(S + chamfer - valveStroke))
		arc valveHead3Down valveHead0Down evert( innerRcos,  innerRcos, calc(S + chamfer - valveStroke))

		// Valve head upper
		arc valveHead0Up valveHead1Up evert( innerRcos, -innerRcos, calc((S + chamfer) - valveStroke + valveHead))
		arc valveHead1Up valveHead2Up evert(-innerRcos, -innerRcos, calc((S + chamfer) - valveStroke + valveHead))
		arc valveHead2Up valveHead3Up evert(-innerRcos,  innerRcos, calc((S + chamfer) - valveStroke + valveHead))
		arc valveHead3Up valveHead0Up evert( innerRcos,  innerRcos, calc((S + chamfer) - valveStroke + valveHead))

		// Valve stem lower
		arc valveStem0Down valveStem1Down evert( calc(valveStemD/2.0*cosd(45.0)), -calc(valveStemD/2.0*cosd(45.0)), calc((S + chamfer) - valveStroke + valveFilletR))
		arc valveStem1Down valveStem2Down evert(-calc(valveStemD/2.0*cosd(45.0)), -calc(valveStemD/2.0*cosd(45.0)), calc((S + chamfer) - valveStroke + valveFilletR))
		arc valveStem2Down valveStem3Down evert(-calc(valveStemD/2.0*cosd(45.0)),  calc(valveStemD/2.0*cosd(45.0)), calc((S + chamfer) - valveStroke + valveFilletR))
		arc valveStem3Down valveStem0Down evert( calc(valveStemD/2.0*cosd(45.0)),  calc(valveStemD/2.0*cosd(45.0)), calc((S + chamfer) - valveStroke + valveFilletR))

		// Valve fillet
		arc valveHead0Up valveStem0Down evert( calc(innerR - valveFilletRcos), 0, calc((S + chamfer) - valveStroke + valveFilletRcos))
		arc valveHead1Up valveStem1Down evert( 0,-calc(innerR - valveFilletRcos), calc((S + chamfer) - valveStroke + valveFilletRcos))
		arc valveHead2Up valveStem2Down evert(-calc(innerR - valveFilletRcos), 0, calc((S + chamfer) - valveStroke + valveFilletRcos))
		arc valveHead3Up valveStem3Down evert( 0, calc(innerR - valveFilletRcos), calc((S + chamfer) - valveStroke + valveFilletRcos))

		// Valve stem upper
		arc valveStem0Up valveStem1Up evert( calc(valveStemD/2.0*cosd(45.0)), -calc(valveStemD/2.0*cosd(45.0)), calc((S + chamfer) + outletH))
		arc valveStem1Up valveStem2Up evert(-calc(valveStemD/2.0*cosd(45.0)), -calc(valveStemD/2.0*cosd(45.0)), calc((S + chamfer) + outletH))
		arc valveStem2Up valveStem3Up evert(-calc(valveStemD/2.0*cosd(45.0)),  calc(valveStemD/2.0*cosd(45.0)), calc((S + chamfer) + outletH))
		arc valveStem3Up valveStem0Up evert( calc(valveStemD/2.0*cosd(45.0)),  calc(valveStemD/2.0*cosd(45.0)), calc((S + chamfer) + outletH))

	// Outer pipe
		arc pipe0Up pipe1Up evert( innerRcos, -innerRcos, calc(S + outletH))
		arc pipe1Up pipe2Up evert(-innerRcos, -innerRcos, calc(S + outletH))
		arc pipe2Up pipe3Up evert(-innerRcos,  innerRcos, calc(S + outletH))
		arc pipe3Up pipe0Up evert( innerRcos,  innerRcos, calc(S + outletH))
);

boundary
(
    piston
    {
        type wall;
        faces
        (
			downQuad(cylIn0, cylIn1, cylIn2, cylIn3) // Piston inner
				
			downQuad(cylIn0, cylOut0, cylOut1, cylIn1) // 1st quarter of piston
			downQuad(cylIn1, cylOut1, cylOut2, cylIn2) // 2nd quarter of piston
			downQuad(cylIn2, cylOut2, cylOut3, cylIn3) // 3rd quarter of piston
			downQuad(cylIn3, cylOut3, cylOut0, cylIn0) // 4th quarter of piston				
        );
    }

	outlet
	{
		type patch;
		faces
		(
			upQuad(valveStem0, pipe0, pipe1, valveStem1) // 1st quarter of outlet
			upQuad(valveStem1, pipe1, pipe2, valveStem2) // 2nd quarter of outlet
			upQuad(valveStem2, pipe2, pipe3, valveStem3) // 3rd quarter of outlet
			upQuad(valveStem3, pipe3, pipe0, valveStem0) // 4th quarter of outlet
		);
	}

	valve
	{
		type wall;
        faces
        (
			downQuad(valveHead0, valveHead1, valveHead2, valveHead3) // valve head bottom

			// 1st quarter of valve
			// sideQuad(valveHead0, valveHead1)
			(valveHead0Up valveStem0Down valveHead1Up valveStem1Down)
			sideQuad(valveStem0, valveStem1)

			// 2nd quarter of valve
			(valveHead1Up valveStem1Down valveHead2Up valveStem2Down)
			sideQuad(valveStem1, valveStem2)

			// 3rd quarter of valve
			(valveHead2Up valveStem2Down valveHead3Up valveStem3Down)
			sideQuad(valveStem2, valveStem3)

			// 4th quarter of valve
			(valveHead3Up valveStem3Down valveHead0Up valveStem0Down)
			sideQuad(valveStem3, valveStem0)
							
        );
	}
	
	walls
    {
        type wall;
        faces
        (
			// 1st quarter of cylinder
			sideQuad(cylOut0, cylOut1)
			upQuad(cylIn0, cylOut0, cylOut1, cylIn1) // upper wall
			// upQuad(cylIn0, cylIn1, pipe0, pipe1)

			// 2nd quarter of cylinder
			sideQuad(cylOut1, cylOut2)
			upQuad(cylIn1, cylOut1, cylOut2, cylIn2) // upper wall

			// 3rd quarter of cylinder
			sideQuad(cylOut2, cylOut3) 
			upQuad(cylIn2, cylOut2, cylOut3, cylIn3) // upper wall

			// 4th quarter of cylinder
			sideQuad(cylOut3, cylOut0)
			upQuad(cylIn3, cylOut3, cylOut0, cylIn0) // upper wall
        );
    }
);

// ************************************************************************* //
