# complex-ricepile
This project simulates the Oslo model [1-3] in complexity science, which shows that some responses of a system to a slowly-driven perturbation are irrespective of its scale. The perturbation was simulated by a continuous addition of "rice grains" to a system of certain length (number of sites), and the response was measured by toppling of the grains to the neighbouring site.

Program written in Python. Combine all the ```.py``` files in the same directory for the code to run.

File ```simulate\ricepile.py``` contains the simulation for the Oslo model. Other files are used to produce the plots as shown in ```ComplexityReport.pdf```.

# References
1.  K. Christensen, A. Corral, V. Frette, J. Feder, and T. Jøssang, Tracer dispersion in a
self-organized critical system, Phys. Rev. Lett. 77, 107–110 (1996).
2.  K. Christensen and N.R. Moloney, Complexity and Criticality, ICP (2005).
3.  G. Pruessner, Self-organised Criticality, Cambridge University Press (2012).

# Acknowledgements
Credits to Prof. Kim Christensen for designing the project, and Max Falkenberg McGillivray for the code for log-binning of the data (```logbin6_2_2018.py```).
