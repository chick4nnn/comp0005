import random
from math import atan2

import matplotlib.pyplot as plt


# fetches the bottom most point in set of points given.
def find_bottom_most(points: list) -> tuple:
	ref = points[0]
	for p in points:
		if p[1] < ref[1] or (p[1] == ref[1] and p[0] < ref[0]):
			ref = p
	return ref

# gets the polar angle from two points by using arctan on the y and x distance.
def cal_polar_angle(p1: tuple, p2: tuple) -> float:
	return atan2(p2[1] - p1[1], p2[0] - p1[0])

# calculates the distance between two given points.
def cal_distance(p1: tuple, p2: tuple) -> float:
	return (p2[1] - p1[1]) ** 2 + (p2[0] - p1[0]) ** 2

# gets the determinant for p1, p2 and p3 to determine whether it is a clockwise or anticlockwise turn.
def determinant(p1: tuple, p2: tuple, p3: tuple) -> float:
	return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

def merge(angles: dict, points: list, aux: list, ref: tuple, low: int, mid: int, high: int):
	for i in range(low, high + 1):
		aux[i] = points[i]

	first_p_counter = low
	second_p_counter = mid + 1
	for counter in range(low, high + 1):
		if first_p_counter > mid:
			points[counter] = aux[second_p_counter]
			second_p_counter = second_p_counter + 1
		elif second_p_counter > high:
			points[counter] = aux[first_p_counter]
			first_p_counter = first_p_counter + 1
		elif angles[aux[second_p_counter]] < angles[aux[first_p_counter]]:
			points[counter] = aux[second_p_counter]
			second_p_counter = second_p_counter  + 1
		elif angles[aux[second_p_counter]] == angles[aux[first_p_counter]]:
			if cal_distance(aux[second_p_counter], ref) < cal_distance(aux[first_p_counter], ref):
				points[counter] = aux[second_p_counter]
				second_p_counter = second_p_counter + 1
		else:
			points[counter] = aux[first_p_counter]
			first_p_counter = first_p_counter + 1

def merge_sort(angles: dict, points: list, aux: list, ref: tuple, low: int, high: int):
	if (high <= low):
		return
	
	mid = low + ((high - low) // 2)

	merge_sort(angles, points, aux, ref, low, mid)
	merge_sort(angles, points, aux, ref, mid + 1, high)
	if angles[points[mid]] < angles[points[mid + 1]]:
		return
	
	merge(angles, points, aux, ref, low, mid, high)

def grahamscan(inputSet: list) -> list:
	ref = find_bottom_most(inputSet)
	angles = dict([(tuple(point), cal_polar_angle(point, ref)) for point in inputSet])

	merge_sort(angles, inputSet, [None] * len(inputSet), ref, 0, len(inputSet) - 1)

	stack = []
	for point in inputSet:
		while len(stack) > 1 and determinant(stack[-2], stack[-1], point) < 0:
			del stack[-1]

		stack.append(point)
	return stack

def genPoint() -> tuple:
	return (random.randint(0, 32767), random.randint(0, 32767))

def genPoints(limit: int) -> list:
	return [genPoint() for _ in range(limit)]

inputSet = genPoints(300)
outputSet = grahamscan(inputSet)

plt.figure()

input_xs, input_ys = zip(*inputSet)
plt.scatter(input_xs, input_ys)

outputSet.append(outputSet[0])
output_xs, output_ys = zip(*outputSet)
plt.plot(output_xs, output_ys)
plt.show()
