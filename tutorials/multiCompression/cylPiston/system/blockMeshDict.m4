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
define(quad2D, ($2Up $1Up zz$1Down $2Down))
define(upQuad, ($1Up $2Up $4Up $3Up))
define(downQuad, ($1Down $2Down $4Down $3Down))
define(sideQuad, ($1Down $2Down $2Up $1Up))

define(vert,  ($1 $2 $3))
define(xyArc, ($1 $2 $3))

// ########################################################################## //
// USER EDITABLE PART

convertToMeters 0.01;

define(D, 		 70) // cylinder bore

define(S, 	  	 280) // piston stroke

define(meshSize, 5) // relative to S & D

// END OF (NORMAL) USER EDITABLE PART
// ########################################################################## //

define(R,		  calc( D/2.0 ))

define(Rcos,	  calc( R*cos((PI/180)*45.0) ))

define(innerR,	  calc( D/4.0 ))

define(innerRcos, calc( innerR*cos((PI/180)*45.0) ))
	
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
);

blocks
(
	// Inner cylinder block (8 9 10 11 0 1 2 3)
    hex2D(cylIn0, cylIn1, cylIn2, cylIn3) /*block 0*/
	(rMeshSize rMeshSize zMeshSize)
    simpleGrading (1 1 1)
		
	// 1st quarter of cylinder (8 12 13 9 0 4 5 1)
    hex2D(cylIn0, cylOut0, cylOut1, cylIn1) /*block 1*/
    (rMeshSize rMeshSize zMeshSize)
    simpleGrading (1 1 1)

	// 2nd quarter of cylinder (9 13 14 10 1 5 6 2)
	hex2D(cylIn1, cylOut1, cylOut2, cylIn2) /*block 2*/
	(rMeshSize rMeshSize zMeshSize)
	simpleGrading (1 1 1)

	// 3rd quarter of cylinder (10 14 15 11 2 6 7 3)
    hex2D(cylIn2, cylOut2, cylOut3, cylIn3) /*block 3*/
    (rMeshSize rMeshSize zMeshSize)
    simpleGrading (1 1 1)

    // 4th quarter of cylinder (11 15 12 8 3 7 4 0)
    hex2D(cylIn3, cylOut3, cylOut0, cylIn0) /*block 4*/
    (rMeshSize rMeshSize zMeshSize)
    simpleGrading (1 1 1)
);

edges
(
	// Bottom of cylinder
	arc cylOut0Down cylOut1Down xyArc( Rcos, -Rcos, 0)
	arc cylOut1Down cylOut2Down xyArc(-Rcos, -Rcos, 0)
	arc cylOut2Down cylOut3Down xyArc(-Rcos,  Rcos, 0)
	arc cylOut3Down cylOut0Down xyArc( Rcos,  Rcos, 0)
		
	// Inner of piston (comment to make inner block as prism)
	arc cylIn0Down cylIn1Down xyArc( innerRcos, -innerRcos, 0)
	arc cylIn1Down cylIn2Down xyArc(-innerRcos, -innerRcos, 0)
	arc cylIn2Down cylIn3Down xyArc(-innerRcos,  innerRcos, 0)
	arc cylIn3Down cylIn0Down xyArc( innerRcos,  innerRcos, 0)
	
	// Upper of upper wall
	arc cylOut0Up cylOut1Up xyArc( Rcos, -Rcos, S)
	arc cylOut1Up cylOut2Up xyArc(-Rcos, -Rcos, S)
	arc cylOut2Up cylOut3Up xyArc(-Rcos,  Rcos, S)
	arc cylOut3Up cylOut0Up xyArc( Rcos,  Rcos, S)
		
	// Inner of upper wall (comment to make inner block as prism)
	arc cylIn0Up cylIn1Up xyArc( innerRcos, -innerRcos, S)
	arc cylIn1Up cylIn2Up xyArc(-innerRcos, -innerRcos, S)
	arc cylIn2Up cylIn3Up xyArc(-innerRcos,  innerRcos, S)
	arc cylIn3Up cylIn0Up xyArc( innerRcos,  innerRcos, S)
);

boundary
(
    walls
    {
        type wall;
        faces
        (
			upQuad(cylIn0, cylIn1, cylIn2, cylIn3)  // Upper inner
			
			sideQuad(cylOut0, cylOut1) // 1st quarter of cylinder
			sideQuad(cylOut1, cylOut2) // 2nd quarter of cylinder
			sideQuad(cylOut2, cylOut3) // 3rd quarter of cylinder
			sideQuad(cylOut3, cylOut0) // 4th quarter of cylinder
				
			upQuad(cylIn0, cylOut0, cylOut1, cylIn1) // 1st quarter of upper wall
			upQuad(cylIn1, cylOut1, cylOut2, cylIn2) // 2nd quarter of upper wall
			upQuad(cylIn2, cylOut2, cylOut3, cylIn3) // 3rd quarter of upper wall
			upQuad(cylIn3, cylOut3, cylOut0, cylIn0) // 4th quarter of upper wall
        );
    }
	
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
);

// ************************************************************************* //
