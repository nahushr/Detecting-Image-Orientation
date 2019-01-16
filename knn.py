import sys
import pandas as pd
import numpy as np

def knn_training(train_file, model_file):
	train_file = pd.read_csv("train-data.txt", delimiter = " ", header = None)
	train_file.to_csv("nearest_model.txt", sep=' ', header = None, index = False)

def knn_testing(train_file, model_file):
	train_file = pd.read_csv("nearest_model.txt", delimiter = " ", header = None)
	train_labels = train_file.iloc[:, [0, 1]]
	train_file = train_file.iloc[:, 2:].values

	test_file = pd.read_csv("test-data.txt", delimiter = " ", header = None)
	test_labels = test_file.iloc[:, [0, 1]]
	test_file = test_file.iloc[:, 2:].values

	accuracy_count = 0

	text_file = open("output.txt", "a")

	for i in range(test_file.shape[0]):
		dist = []
		orientation = {0:0, 90:0, 180:0, 270:0}

		for j in range(train_file.shape[0]):
			dist.append((train_labels.iloc[j, 0], train_labels.iloc[j, 1], np.linalg.norm(train_file[j] - test_file[i])))

		for k in range(7):
			minimum = min(dist, key = lambda t: t[2])
			orientation[minimum[1]] += 1
			dist.remove(minimum)

		actual_degree = test_labels.iloc[i, 1]
		predicted_degree = max(orientation, key=lambda degrees: orientation[degrees])

		if actual_degree == predicted_degree:
			accuracy_count += 1

		text_file.write(test_labels.iloc[i][0] + " " + str(max(orientation, key=lambda degrees: orientation[degrees])) + "\n")
		
		#print (test_labels.iloc[i][0], max(orientation, key=lambda degrees: orientation[degrees]))

	return accuracy_count*100/i


if sys.argv[1] == "train" and sys.argv[4] == "nearest":
	train_file = open(sys.argv[2], "r")
	model_file = open(sys.argv[3], "w")
	knn_training(train_file, model_file)

if sys.argv[1] == "test" and sys.argv[4] == "nearest":
	start_time = time.time()
	test_file = open(sys.argv[2], "r")
	model_file = open(sys.argv[3], "r")

	accuracy = knn_testing(test_file, model_file)
	print (accuracy)
