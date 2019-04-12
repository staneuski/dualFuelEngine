# Application
**multicompCompressFluid**

##Group

**grpBasicSolvers**

# Description
Potential flow solver which solves for the velocity potential, to calculate the flux-field, from which the velocity field is obtained by reconstructing the flux.

## Solver details
The potential flow solution is typically employed to generate initial fields or full Navier-Stokes codes.  The flow is evolved using the equation:
$$
{\bigtriangledown}^{2} \Phi = div(\vec{U})
$$
Where:
| Variable     	  | Meaning    				| Dimension   |
|:---------------:| ----------------------- |:-----------:|
| $$\Phi$$     	  | Velocity potential  	| $$m^2/s$$	  |
| $$\vec{U}$$     | Velocity 				| $$m/s$$	  |


The corresponding pressure field could be calculated from the divergence of the Euler equation:
$$
{\bigtriangledown}^{2} p + \Delta\left(\Delta(\vec{U}\otimes\vec{U})\right) = 0
$$
but this generates excessive pressure variation in regions of large velocity gradient normal to the flow direction.  A better option is to calculate the pressure field corresponding to velocity variation along the stream-lines:
$$
{\bigtriangledown}^{2} p + \Delta{\vec{F}\cdot\Delta(\vec{U}\otimes\vec{U}})= 0
$$
where the flow direction tensor $$\vec{F}$$ is obtained from ($$\otimes$$ - тензорное произведение):
$$
\vec{F} = \hat{\vec{U}}\otimes\hat{\vec{U}}
$$

**Required fields**
| Field     	  | Meaning    				| Dimension   |
|:---------------:| ----------------------- |:-----------:|
|   $$U$$     	  | Velocity 			  	| $$m/s$$	  |

**Optional fields**
| Field     	  | Meaning    				| Dimension   |
|:---------------:| ----------------------- |:-----------:|
|   $$U$$     	  | Velocity 			  	| $$m/s$$	  |
|	$$p$$         | Kinematic pressure      | $$m^2/s^2$$ |
|	$$\Phi$$      | Velocity potential 		| $$m/s$$	  |

Velocity potential generated from $$p$$ (if present) or $$U$$ if not present

**Options**

| Flag	     	        | Meaning   			  								   |
|----------------------:| -------------------------------------------------------- |
|	`-writep`   	    | Write the Euler pressure								   |
|	`-writePhi `		| Write the final velocity potential					   |
|	`-initialiseUBCs`   | Update the velocity boundaries before solving for $$\Phi$$	|
