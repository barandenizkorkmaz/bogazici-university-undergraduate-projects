import sys
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import numpy as np
import subprocess

if len(sys.argv) < 2:
	print("first argument is the name of output file")
	sys.exit(1)

out_filename = sys.argv[1]

with open(out_filename) as f:
    lines = f.readlines()

total_error = float(lines[-1].split("=")[1])
print("Error:", total_error)
lines = lines[:-3]


iters = list()
errs = list()
for l in lines:
    it_er = l.rstrip().split()
    it = int(it_er[0].split("=")[1])
    er = float(it_er[1].split("=")[1])
    iters.append(it)
    errs.append(er)

plt.plot(iters, np.log(errs))
plt.title(f"Error vs Iterations (Logarithmic Scale) (Source: {out_filename})")
plt.xlabel("Iteration Number")
plt.ylabel("Error Value (Log)")
plt.savefig(f"{out_filename}_log", dpi=200)

plt.clf()

plt.plot(iters, errs)
plt.title(f"Error vs Iterations (Source: {out_filename})")
plt.xlabel("Iteration Number")
plt.ylabel("Error Value")
plt.savefig(f"{out_filename}_norm", dpi=200)

print("Written the plot images into the folder.")
