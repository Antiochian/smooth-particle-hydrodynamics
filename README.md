# smooth-particle-hydrodynamics

I have been trying to implement a satisfactory fluid simulation for quite a long time now.
All of my homebrew ideas have failed, and I happen to be doing a Fluid Dynamics course at uni at the moment, so I figured I had a good excuse to delve into the quite technical field of professional high-level fluid simulation.

The technique I am learning is called "Smoothed-Particle Hydrodynamics", or SPH for short.

What is it?
-----
The key concept behind SPH is the discretization of spatial field quantities and spatial differential operators,e.g., gradient, divergence, curl, etc.

In practice, it is the approximation of a field as the convolution of a set of points with a smooth kernel function to produce efficient and stable models.
//To Do: Explain some of the maths behind this further...

Discretization Test
----
Before I launched into the project full throttle, I wanted to check my theoretical understanding was valid. To this end, I wrote a very inefficient and crude prototype script to test how the approximation would work for a known function.

The solid lines plotted on the top diagram are the z-values of a 2D analytic function along the parameterized red line through space shown on the bottom diagram. The dashed lines plotted on the top diagram are the corresponding approximations found by convolving the blue points (bottom graph) with a *cubic spline kernel*.
|Test results for three functions|Boundary undersampling diagram|
|:---:|:---:|
|![test graph](kernel_test_results.png)|![neighbourhood problem](neighbourhood_problem.PNG)|

The approximation seems to be appropriate for slowly-changing functions and away from boundaries. The boundary errors are caused by the fact that SPH relies on a "neighbourhood" of local particles to sum over, and once you get to the end of the region, the particles on the edge of the system no longer have a full neighbourhood, and so the approximation breaks down. The figure on the right illustrates this phenomenon.

Fast Neighbourhood Search Test
---
The compact support of the kernel function ensures that instead of summing over all particles, only the particles within the kernel support radius (h) need be considered. A cruicial technology to allow this to be leveraged is a fast neighbourhood search, which here I have implemented as a memory inefficient (but quite fast) hash table. The sample space is split into a grid of "h" spacing, and only particles in the one-ring around a target point need be considered in the count. Some illustrations are below.
|Example 1|Example 2|Example 3|Timings|
|:---:|:---:|:---:|:---:|
|![test1](neighbourhood_test_1.png)|![test2](neighbourhood_test_2.png)|![test3](neighbourhood_test_3.png)|![timings](timing_data.png)

Filling the hashtable takes O(n) time, and querying it takes O(1), where the constant time goes as h^2. Timing data is provided above.

Main algorithm implementation
----
W.I.P.

Roadmap
----
- [x] Test discretization and kernel convolution process
- [x] Test spatial partioning for fast neighbourhood search
- [x] Test Runge-Kutta differential solver
- [x] Separate Navier-Stokes equations into piecewise differential equations
- [ ] Investigate point splatting rendering techniques
- [ ] Explore alternate numerical methods
- [ ] Implementation of algorithm

(Extensions?)
- [ ] Interpolation between normals
- [ ] Refined numerical differential solutions
- [ ] C++ port
- [ ] GPU code port?
