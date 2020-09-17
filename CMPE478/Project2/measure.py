import subprocess
from timeit import timeit
import csv
from collections import defaultdict

sizes = [23,47,71]
processors = [1, 2**3, 3**3, 4**3]
# Used for increasing precision. Makes run longer.
nof_reps = 2


def run(size, proc, number):
	# Get caches hot
	timeit(
		stmt=f'subprocess.run(["mpiexec","-n", "{proc}","--oversubscribe","a.out","{size}"], stdout=subprocess.DEVNULL)', 
		setup="import subprocess",
		number=1
	)
	return timeit(
		stmt=f'subprocess.run(["mpiexec","-n", "{proc}","--oversubscribe","a.out","{size}"], stdout=subprocess.DEVNULL)', 
		setup="import subprocess",
		number=number
	) / number


def measure_size(size, number=1):
	ts = list()
	for p in processors:
		ts.append(run(size, p, number))
		print(f"Done size {s} with proc {p} in {ts[-1]:.1f} secs.")

	speedups = list()
	for t in ts[1:]:
		speedups.append(f"{ts[0]/t:.1f}")

	ts = [f"{t:.2f}" for t in ts]

	return [size] + ts + speedups


rows = list()
for s in sizes:
	rows.append(measure_size(s, nof_reps))


with open("results.csv", "w", newline="") as f:
	w = csv.writer(f)
	ts_headers = [f"T{p}" for p in processors]
	speed_headers = [f"S{p}" for p in processors[1:]]
	w.writerow(["N"] + ts_headers + speed_headers)

	w.writerows(rows)
