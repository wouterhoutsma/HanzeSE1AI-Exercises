# MACHINE LEARNING OPGAVE 3
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import random

from sklearn.datasets import fetch_mldata
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.metrics import confusion_matrix

import urllib.request
from urllib.error import HTTPError

print ("Laden van de data en zetten van de X en de y")
# alternatieve methode van laden: https://github.com/ageron/handson-ml/issues/7 (in de except een alternatieve manier)
try:
	mnist = fetch_mldata('MNIST original')
except HTTPError as e:
    print("Could not download MNIST data from mldata.org, trying alternative...")

    # Alternative method to load MNIST, if mldata.org is down
    from scipy.io import loadmat
    mnist_alternative_url = "https://github.com/amplab/datascience-sp14/raw/master/lab7/mldata/mnist-original.mat"
    mnist_path = "./mnist-original.mat"
    response = urllib.request.urlopen(mnist_alternative_url)
    with open(mnist_path, "wb") as f:
        content = response.read()
        f.write(content)
    mnist_raw = loadmat(mnist_path)
    mnist = {
        "data": mnist_raw["data"].T,
        "target": mnist_raw["label"][0],
        "COL_NAMES": ["label", "data"],
        "DESCR": "mldata.org dataset: mnist-original",
    }
    print("Success!")
X,y = mnist['data'], mnist['target']

# X.shape = 7000, 784
# y.shape = 7000, 1

test_waarde = 36000 
some_digit = X[test_waarde] 