Hi Nils!

That’s great that your pixel size matches our simulation size so well! We can check that off the list.

You are correct - I am referring to Marcus theory and your equation looks spot on.

The code we have calculates the values of J_{if} and \Delta E between all pairs of monomers within the molecular system of P3HT (within a certain cut-off of 1 nm). You are right that the DoS for P3HT can be found quite easily too (~100 meV) and most device-scale Monte Carlo simulations just pick random values from this distribution to account for energetic disorder (which is often sufficient). On the molecular level, however, the relative orientations and conformations of the monomers can have a massive difference on the electronic coupling, so to avoid these generalisations and to try and keep as ab initio as possible, we calculate them all from the ground up.

We then perform Kinetic Monte Carlo simulations to obtain the overall mobility for the morphology. The equation is very basic (and explained well in the papers that I linked you to last time) - we take a uniformly distributed random number, x, and divide it by the Marcus hopping rate, \Gamma_{if}, in order to obtain the hopping timescale \tau_{if}:

\displaystyle \tau_{if} = \frac{ln(x)}{\Gamma_{if}}.

Then, we repeat this for every single combination of monomers i and f, and create a chronological queue in ascending \tau_{if}. We then execute the first hop in the queue (because that is the one that is going to happen next), increment the simulation time by \tau_{if}, calculate the next lot of hops from the new chromophore, and repeat it until we reach the desired simulation time. Finally, by averaging over loads of carriers and loads of simulation times we can determine the diffusion coefficient of carriers in the system and then determine the mobility values that I showed at AIChE.

The subtlety here is that, for the work that you have suggested where we zoom out to see an entire thin film rather than just a small 10x10x10nm section, we don’t really want the mobility, but rather the distribution of hopping rates, \Gamma_{if}, that describe carrier motion between the pixels in your system. As a first pass, you could indeed use these as tuneable parameters and simply minimise the squared error between the resultant and our simulated mobilities for the various important hopping rates, i.e.:
1) Hopping from crystalline to crystalline A) along the direction of the electric field and B) perpendicular to the direction of the electric field (determined by the position of the electrodes)
2A), 2B) Hopping from crystalline to amorphous in both directions
3A), 3B) Hopping from amorphous to amorphous in both directions

Then, we could inject a carrier to a random pixel in your morphology, use the KMC algorithm to work out where it would hop to next, rinse and repeat until it has taken a statistically significant number of hops to calculate a meaningful mean squared displacement, and then obtain a full device-scale mobility.

It’s very interesting that transport across the fibers can be faster than along them - I can definitely see the importance of performing some KMC simulations to validate this. We should be able to see this behaviour unfold directly in front of us if we get this right!

Does this all make sense? Let me know if there’s anything else that you’re not sure about or need from me.

Cheers,

Matty
