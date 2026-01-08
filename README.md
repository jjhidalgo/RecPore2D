# RecPore2D
Generation of 2D porous media geometry with regular or random packing of discs. The resulting geometries can be exported to [**Gmsh**](https://gmsh.info/), [**OpenSCAD**](https://openscad.org/) and [**SnappyHexMesh**](https://openfoamwiki.net/index.php/SnappyHexMesh) formats.

### 🧩 Code Structure

**Source Modules**

- **RecPore2D.py** – Core generator of 2D porous media using regular or random disc packings.  
- **PoreError.py** – Exception manager for RecPore2.  
- **PyGmsh.py** – Wrapper for Gmsh geometry export.  
- **PyGrain.py** – Grain creation and configuration.  
- **PyOpenSCAD.py** – Wrapper for OpenSCAD export.  
- **PySnappy.py** – Wrapper for SnappyHexMesh dictionary generation.
- **plotGeo.py** – script for plotting a gmsh mesh file by gmsh lib (cases of meshtype='gmsh').


**Templates**

- `blockMeshDict.tmpl` – Template blockMesh configuration.  
- `snappy.tmpl` – Template SnappyHexMesh configuration.  

**Examples / Tests**

- `test.py` – Example for regular packing.  
- `test-rnd.py` – Example for random packing.  
- `testsnappy.py` – Example SnappyHexMesh generation. 
- `zz.py` – Extra example SnappyHexMesh generation included in this tutorial. 

### 🔬 Acknowledgements

- **Project MHetScale (FP7‑IDEAS‑ERC‑617511)** – European Research Council  
- **Project Mec‑MAT (CGL2016‑80022‑R)** – Spanish Ministry of Economy and Competitiveness  

## 📘 Tutorial: Building a 2D mesh for OpenFOAM (snappyHexMesh) 

This tutorial provides a complete workflow to generate a **2D pore‑scale mesh** using RecPore2D outputs. General steps are:  
1. **RecPore2D** - python code for the geometry generation.  
2. `blockMesh`  - instruction for building a regular mesh of the shape container in 3D.
3. `snappyHexMesh`  - instruction for building pores/grains meshing in 3D.
4. `extrudeMesh`  - instruction for transform the 3D mesh to a 2D mesh case.

A complete example is included in every step.

### 1. Set geometry properties in RecPore2D sources and inputs

- Specify `ngrains_max` among others parameters in **RecPore2D.py**.
- Edit domain size and random/regular packing settings in **tests/zz.py**.


### 2. Run RecPore2D program

Type the following at the RecPore2D folder (program working folder) to generate requested output files: **blockMeshDict** & **snappyHexMeshDict** in this case:

```
python -m tests.zz
```
In case of writing the stl files, that files can be open in paraview.

### 3. Prepare the openFoam working case directory

Copy & Paste the following generated files into the `system` folder from your openFoam case:
```
blockMeshDict
snappyHexMeshDict
```
 **ExtrudeMeshDict** and **meshQualityDict** can be obtained from the openFoam sources at `openfoam13\etc\caseDicts\mesh\generation`.

### 4. Edit `blockMeshDict` file

#### 4.1. Change from patches to boundary (in order to update the sentences to newer versions of openFoam). As example:
```	
	//From
	patches
	(
		wall top
		(
		 (2 1 5 6)
		)

		wall left
		(
		 (3 7 6 2)
		)

		wall right
		(
		 (0 1 5 4)
		)

		wall bottom
		(
		 (3 0 4 7)
		)

		empty ground
		(
		 (0 3 2 1)
		)

		empty ceiling
		(
		 (4 5 6 7)
		)
	);

	//To
	boundary
	(
		top
		{
			type wall;
			faces
			(
				(2 1 5 6)
			);
		}
		left
		{
			type patch;
			faces
			(
				(3 7 6 2)
			);
		}
		right
		{
			type patch;
			faces
			(
				(0 1 5 4)
			);
		}
		bottom
		{
			type wall;
			faces
			(
				(3 0 4 7)
			);
		}
		ground
		{
			type wall;
			faces
			(
				(0 3 2 1)
			);
		}
		ceiling
		{
			type wall;
			faces
			(
				(4 5 6 7)
			);
		}
		
	);
```
#### 4.2. Adapt the required nb of elements in every direction. AS example:
```
	//From
	blocks
	(
		hex (0 1 2 3 4 5 6 7) (200 200 200) simpleGrading (1 1 1)
	);
	
	//To
	blocks
	(
		hex (0 1 2 3 4 5 6 7) (50 200 1) simpleGrading (1 1 1)
	);
```
	
### 5. Edit `snappyHexMeshDict` file

#### 5.1. Check the z direction coordenates of **EVERY** cylinder exported from RedPore2D and add a patchInfo.name to group, and facilitate later use at the initial setup of the case (boundary conditions, etc). The last is optional, only in case of huge number of grains. As example:

```
	//From
	geometry
	{
	grain1
	{
	  type searchableCylinder;
		point1 (0.26047804305688177 0.03688629483928196 0.5); //minZ
		point2 (0.26047804305688177 0.03688629483928196 1.0); //maxZ
		radius 0.003175521571776009;
	}
	
	//To
	geometry
	{
	grain1
	{
	  type searchableCylinder;
		point1 (0.26047804305688177 0.03688629483928196 0.1); //minZ
		point2 (0.26047804305688177 0.03688629483928196 0.2); //maxZ
		radius 0.003175521571776009;
		
		patchInfo #group grains by patchInfo.name
		{
			type wall;
			name grains;
		}
	}
```
#### 5.2. Check the z coordenate of locationInMesh. It should be into the domain. As example:
```
	//From
	// Mesh selection
    // ~~~~~~~~~~~~~~

    // After refinement patches get added for all refinementSurfaces and
    // all cells intersecting the surfaces get put into these patches. The
    // section reachable from the locationInMesh is kept.
    // NOTE: This point should never be on a face, always inside a cell, even
    // after refinement.
    locationInMesh (0.31998706673528254 0.03728451441883222 0.1); //minZ
	
	//To
	// Mesh selection
    // ~~~~~~~~~~~~~~

    // After refinement patches get added for all refinementSurfaces and
    // all cells intersecting the surfaces get put into these patches. The
    // section reachable from the locationInMesh is kept.
    // NOTE: This point should never be on a face, always inside a cell, even
    // after refinement.
    locationInMesh (0.31998706673528254 0.03728451441883222 0.15); //minZ
```

### 6. Edit `extrudeMeshDict` file
The file include specifications of the extrusion process settings:

```
sourcePatches    (ground); //minZ

exposedPatchName ceiling; //maxZ

extrudeModel     linearNormal; //model extrusion

linearNormalCoeffs //settings of the model
{
    nLayers      1;
    expansionRatio 1.0;
    thickness    0.01; //final thickness in case (check it in paraview)
}
```

### 7. Run meshing process in openFoam

```
blockMesh
checkMesh
snappyHexMesh
extrudeMesh
```

### 8. Set as empty the 3D to 2D walls in `polyMesh/boundary`

As example:

```
	ground
    {
        type            wall; 					//from wall
        inGroups        List<word> 1(wall);		//from wall
        nFaces          42839;
        startFace       82431;
    }
    ceiling
    {
        type            wall;					//from wall
        inGroups        List<word> 1(wall);		//from wall
        nFaces          42839;
        startFace       125270;
    }


	ground
    {
        type            empty;					//to empty
        inGroups        List<word> 1(empty);	//to empty
        nFaces          42839;
        startFace       82431;
    }
    ceiling
    {
        type            empty;					//to empty
        inGroups        List<word> 1(empty);	//to empty
        nFaces          42839;
        startFace       125270;
    }
```

### 9. Check/Include in state fields files `0/p` & `0/U`
Set ground and ceiling walls as empty (2D walls) and set grains walls conditions as zeroGradient for p and noSlip for U. As example:

```
    ground
    {
        type            empty;
    }
	
	ceiling
    {
        type             empty;
    }

	//In p:
	grain1
	{
				 type            zeroGradient;
	}
	grain2
	{
				 type            zeroGradient;
	}
	etc..
	
	//In U:
	grain1
	{
				 type            noSlip;
	}
	grain2
	{
				 type            noSlip;
	}
	etc..
	
	//Or if u group the geometries by a pathInfo.name:
	//In p:
	grains
	{
				 type            zeroGradient;
	}
	
	//In U:
	grains
	{
				 type            noSlip;
	}
```

### 10. Visualizate the mesh in *paraView*

```
paraFoam
```

