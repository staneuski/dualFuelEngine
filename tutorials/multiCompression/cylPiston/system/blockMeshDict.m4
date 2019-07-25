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

define(hex2D, hex ($1Up $2Up $3Up $4Up $1Down $2Down $3Down $4Down))
define(quad2D, ($2Up $1Up $1Down $2Down))
define(upQuad, ($1Up $2Up $4Up $3Up))
define(downQuad, ($1Down $2Down $4Down $3Down))
define(sideQuad, ($1Down $2Down $2Up $1Up))

define(vert,  ($1 $2 $3))
define(evert, ($1 $2 $3))

// ########################################################################## //
// USER EDITABLE PART

convertToMeters 0.01;

define(D, 		    70) // cylinder bore

define(S, 	  	   280) // piston stroke

define(meshSize,     5) // relative to S & D

define(valveStroke, 30) // valve stroke

define(valveHead,    3) // valve head thickness

define(valveStemD,   10)

define(outletH,      40)

// END OF (NORMAL) USER EDITABLE PART
// ########################################################################## //

define(R,		  calc( D/2.0 ))

define(Rcos,	  calc( R*cos((PI/180)*45.0) ))

define(innerR,	  calc( D/4.0 ))

define(innerRcos, calc( innerR*cos((PI/180)*45.0) ))
	

define(valveFilletR, calc(innerR - valveStemD/2.0))

define(valveFilletRcos, calc(valveFilletR*cos((PI/180)*45.0)))


define(rMeshSize, calc( R/meshSize ))

define(zMeshSize, calc( S/meshSize ))

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
	
vertices
(
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
	/*08*/ vert(innerR,  0,      S) vlabel(cylIn0Up)
	/*09*/ vert(0,      -innerR, S) vlabel(cylIn1Up)
	/*10*/ vert(-innerR, 0,      S) vlabel(cylIn2Up)
	/*11*/ vert(0,       innerR, S) vlabel(cylIn3Up)
	
	// Upper of cylinder
	/*12*/ vert(R,  0, S) vlabel(cylOut0Up)
	/*13*/ vert(0, -R, S) vlabel(cylOut1Up)
	/*14*/ vert(-R, 0, S) vlabel(cylOut2Up)
	/*15*/ vert(0,  R, S) vlabel(cylOut3Up)

	// Valve head bottom
	/*16*/ vert(innerR,  0,      calc(S - valveStroke - valveHead)) vlabel(valveHead0Down)
	/*17*/ vert(0,      -innerR, calc(S - valveStroke - valveHead)) vlabel(valveHead1Down)
	/*18*/ vert(-innerR, 0,      calc(S - valveStroke - valveHead)) vlabel(valveHead2Down)
	/*19*/ vert(0,       innerR, calc(S - valveStroke - valveHead)) vlabel(valveHead3Down)

	// Valve head upper
	/*20*/ vert(innerR,  0,      calc(S - valveStroke)) vlabel(valveHead0Up)
	/*21*/ vert(0,      -innerR, calc(S - valveStroke)) vlabel(valveHead1Up)
	/*22*/ vert(-innerR, 0,      calc(S - valveStroke)) vlabel(valveHead2Up)
	/*23*/ vert(0,       innerR, calc(S - valveStroke)) vlabel(valveHead3Up)

	// Valve stem lower
	/*24*/ vert(calc(valveStemD/2.0),   0,                    calc((S - valveStroke) + valveFilletR)) vlabel(valveStem0Down)
	/*25*/ vert(0,                     -calc(valveStemD/2.0), calc((S - valveStroke) + valveFilletR)) vlabel(valveStem1Down)
	/*26*/ vert(-calc(valveStemD/2.0),  0,                    calc((S - valveStroke) + valveFilletR)) vlabel(valveStem2Down)
	/*27*/ vert(0,                      calc(valveStemD/2.0), calc((S - valveStroke) + valveFilletR)) vlabel(valveStem3Down)
	
	// Valve stem upper
	/*28*/ vert(calc(valveStemD/2.0),   0,                    calc(S + outletH)) vlabel(valveStem0Up)
	/*29*/ vert(0,                     -calc(valveStemD/2.0), calc(S + outletH)) vlabel(valveStem1Up)
	/*30*/ vert(-calc(valveStemD/2.0),  0,                    calc(S + outletH)) vlabel(valveStem2Up)
	/*31*/ vert(0,                      calc(valveStemD/2.0), calc(S + outletH)) vlabel(valveStem3Up)
);

blocks
(
	// Cylinder
		// // Inner cylinder block (8 9 10 11 0 1 2 3)
		// hex2D(cylIn0, cylIn1, cylIn2, cylIn3) /*block 0*/
		// (rMeshSize rMeshSize zMeshSize)
		// simpleGrading (1 1 1)
			
		// // 1st quarter of cylinder (8 12 13 9 0 4 5 1)
		// hex2D(cylIn0, cylOut0, cylOut1, cylIn1) /*block 1*/
		// (rMeshSize rMeshSize zMeshSize)
		// simpleGrading (1 1 1)

		// // 2nd quarter of cylinder (9 13 14 10 1 5 6 2)
		// hex2D(cylIn1, cylOut1, cylOut2, cylIn2) /*block 2*/
		// (rMeshSize rMeshSize zMeshSize)
		// simpleGrading (1 1 1)

		// // 3rd quarter of cylinder (10 14 15 11 2 6 7 3)
		// hex2D(cylIn2, cylOut2, cylOut3, cylIn3) /*block 3*/
		// (rMeshSize rMeshSize zMeshSize)
		// simpleGrading (1 1 1)

		// // 4th quarter of cylinder (11 15 12 8 3 7 4 0)
		// hex2D(cylIn3, cylOut3, cylOut0, cylIn0) /*block 4*/
		// (rMeshSize rMeshSize zMeshSize)
		// simpleGrading (1 1 1)

	// Valve
		// Head
		hex2D(valveHead0, valveHead1, valveHead2, valveHead3) /*block 5*/
		(4 4 1)
		simpleGrading (1 1 1)

		// // Fillet
		hex (valveStem0Down valveStem1Down valveStem2Down valveStem3Down valveHead0Up valveHead1Up valveHead2Up valveHead3Up) /*block 6*/
		(4 4 10)
		simpleGrading (1 1 1)

		// Stem
		hex2D(valveStem0, valveStem1, valveStem2, valveStem3) /*block 7*/
		(4 4 25)
		simpleGrading (1 1 1)
);

edges
(
	// Cylinder
		// // Bottom of cylinder
		// arc cylOut0Down cylOut1Down evert( Rcos, -Rcos, 0)
		// arc cylOut1Down cylOut2Down evert(-Rcos, -Rcos, 0)
		// arc cylOut2Down cylOut3Down evert(-Rcos,  Rcos, 0)
		// arc cylOut3Down cylOut0Down evert( Rcos,  Rcos, 0)
			
		// // Inner of piston (comment to make inner block as prism)
		// arc cylIn0Down cylIn1Down evert( innerRcos, -innerRcos, 0)
		// arc cylIn1Down cylIn2Down evert(-innerRcos, -innerRcos, 0)
		// arc cylIn2Down cylIn3Down evert(-innerRcos,  innerRcos, 0)
		// arc cylIn3Down cylIn0Down evert( innerRcos,  innerRcos, 0)
		
		// // Upper of upper wall
		// arc cylOut0Up cylOut1Up evert( Rcos, -Rcos, S)
		// arc cylOut1Up cylOut2Up evert(-Rcos, -Rcos, S)
		// arc cylOut2Up cylOut3Up evert(-Rcos,  Rcos, S)
		// arc cylOut3Up cylOut0Up evert( Rcos,  Rcos, S)
			
		// // Inner of upper wall (comment to make inner block as prism)
		// arc cylIn0Up cylIn1Up evert( innerRcos, -innerRcos, S)
		// arc cylIn1Up cylIn2Up evert(-innerRcos, -innerRcos, S)
		// arc cylIn2Up cylIn3Up evert(-innerRcos,  innerRcos, S)
		// arc cylIn3Up cylIn0Up evert( innerRcos,  innerRcos, S)

		// // Inner of upper
		// arc cylIn0Up cylIn1Up evert( innerRcos, -innerRcos, S)
		// arc cylIn1Up cylIn2Up evert(-innerRcos, -innerRcos, S)
		// arc cylIn2Up cylIn3Up evert(-innerRcos,  innerRcos, S)
		// arc cylIn3Up cylIn0Up evert( innerRcos,  innerRcos, S)

	// Valve
		// Valve head bottom
		arc valveHead0Down valveHead1Down evert( innerRcos, -innerRcos, calc(S - valveStroke - valveHead))
		arc valveHead1Down valveHead2Down evert(-innerRcos, -innerRcos, calc(S - valveStroke - valveHead))
		arc valveHead2Down valveHead3Down evert(-innerRcos,  innerRcos, calc(S - valveStroke - valveHead))
		arc valveHead3Down valveHead0Down evert( innerRcos,  innerRcos, calc(S - valveStroke - valveHead))

		// Valve head upper
		arc valveHead0Up valveHead1Up evert( innerRcos, -innerRcos, calc(S - valveStroke))
		arc valveHead1Up valveHead2Up evert(-innerRcos, -innerRcos, calc(S - valveStroke))
		arc valveHead2Up valveHead3Up evert(-innerRcos,  innerRcos, calc(S - valveStroke))
		arc valveHead3Up valveHead0Up evert( innerRcos,  innerRcos, calc(S - valveStroke))

		// Valve stem lower
		arc valveStem0Down valveStem1Down evert( calc(valveStemD/2.0*cos((PI/180)*45.0)), -calc(valveStemD/2.0*cos((PI/180)*45.0)), calc((S - valveStroke) + valveFilletR))
		arc valveStem1Down valveStem2Down evert(-calc(valveStemD/2.0*cos((PI/180)*45.0)), -calc(valveStemD/2.0*cos((PI/180)*45.0)), calc((S - valveStroke) + valveFilletR))
		arc valveStem2Down valveStem3Down evert(-calc(valveStemD/2.0*cos((PI/180)*45.0)),  calc(valveStemD/2.0*cos((PI/180)*45.0)), calc((S - valveStroke) + valveFilletR))
		arc valveStem3Down valveStem0Down evert( calc(valveStemD/2.0*cos((PI/180)*45.0)),  calc(valveStemD/2.0*cos((PI/180)*45.0)), calc((S - valveStroke) + valveFilletR))

		// Valve Fillet
		arc valveHead0Up valveStem0Down evert( calc(innerR - valveFilletRcos), 0, calc(S - valveStroke + valveFilletR/4.0))
		arc valveHead1Up valveStem1Down evert( 0,-calc(innerR - valveFilletRcos), calc(S - valveStroke + valveFilletR/4.0))
		arc valveHead2Up valveStem2Down evert(-calc(innerR - valveFilletRcos), 0, calc(S - valveStroke + valveFilletR/4.0))
		arc valveHead3Up valveStem3Down evert( 0, calc(innerR - valveFilletRcos), calc(S - valveStroke + valveFilletR/4.0))

		// Valve stem upper
		arc valveStem0Up valveStem1Up evert( calc(valveStemD/2.0*cos((PI/180)*45.0)), -calc(valveStemD/2.0*cos((PI/180)*45.0)), calc(S + outletH))
		arc valveStem1Up valveStem2Up evert(-calc(valveStemD/2.0*cos((PI/180)*45.0)), -calc(valveStemD/2.0*cos((PI/180)*45.0)), calc(S + outletH))
		arc valveStem2Up valveStem3Up evert(-calc(valveStemD/2.0*cos((PI/180)*45.0)),  calc(valveStemD/2.0*cos((PI/180)*45.0)), calc(S + outletH))
		arc valveStem3Up valveStem0Up evert( calc(valveStemD/2.0*cos((PI/180)*45.0)),  calc(valveStemD/2.0*cos((PI/180)*45.0)), calc(S + outletH))

);

boundary
(
    walls
    {
        type wall;
        faces
        (
			// upQuad(cylIn0, cylIn1, cylIn2, cylIn3)  // Upper inner
			
			// sideQuad(cylOut0, cylOut1) // 1st quarter of cylinder
			// sideQuad(cylOut1, cylOut2) // 2nd quarter of cylinder
			// sideQuad(cylOut2, cylOut3) // 3rd quarter of cylinder
			// sideQuad(cylOut3, cylOut0) // 4th quarter of cylinder
				
			// upQuad(cylIn0, cylOut0, cylOut1, cylIn1) // 1st quarter of upper wall
			// upQuad(cylIn1, cylOut1, cylOut2, cylIn2) // 2nd quarter of upper wall
			// upQuad(cylIn2, cylOut2, cylOut3, cylIn3) // 3rd quarter of upper wall
			// upQuad(cylIn3, cylOut3, cylOut0, cylIn0) // 4th quarter of upper wall
        );
    }
	
    piston
    {
        type wall;
        faces
        (
			// downQuad(cylIn0, cylIn1, cylIn2, cylIn3) // Piston inner
				
			// downQuad(cylIn0, cylOut0, cylOut1, cylIn1) // 1st quarter of piston
			// downQuad(cylIn1, cylOut1, cylOut2, cylIn2) // 2nd quarter of piston
			// downQuad(cylIn2, cylOut2, cylOut3, cylIn3) // 3rd quarter of piston
			// downQuad(cylIn3, cylOut3, cylOut0, cylIn0) // 4th quarter of piston				
        );
    }
);

// ************************************************************************* //
