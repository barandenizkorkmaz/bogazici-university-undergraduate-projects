## How To Compile & Run
#### Program
To run the main program, use this command:
```bash
mpic++ main.cpp
mpirun -np <P> [--oversubscribe] a.out <N> [--print]
```
P: Number of Processors
N: The Grid Spacing
--print: [OPTIONAL] argument for visualization of actual and calculated cubes.

##### Assumptions:
1. N is a valid integer.
2. N + 1 is evenly divided by cube root of P (Number of Processors)
3. --print option is only enabled for visualization purposes.

NOTE: The number of processors must be perfect cubes, like 1, 8, 27, 64.

##########

#### Plots
To create the plots, run:
```bash
mpirun -np <P> a.out <N> > <N>_<P>
python3 plot.py <N>_<P>
```
Exp:
```bash
mpirun -np 8 a.out 59 > 59_8
python3 plot.py 59_8
```
This commands capture the output of a run and uses them to create the plots. They get saved to the folder. 
The program also prints the difference between our result and the ground truth.

NOTE: plot.py assumes that the name of executable file is `a.out`

#### Times and Speedups
To measure run times and speedups, you need the `measure.py` program. 
In it, you need to specify the parameters. For example:
```python
sizes = [23,47,71]
processors = [1, 2**3, 3**3, 4**3]
nof_reps = 2
```
Runs the program for 3\*4=12 configurations. 
Repetition count increases the precision. 
One dummy run is performed but not measured for every configuration for caching purposes.

NOTE: measure.py assumes that the name of executable file is `a.out`

An example `results.csv`:

N	T1	T8	T27	T64	S8	S27	S64
23	0.6	0.42	0.98	1.73	1.4	0.6	0.3
47	19.7	5.54	9.47	11.94	3.6	2.1	1.7
71	159.05	45.59	66.59	57.94	3.5	2.4	2.7

