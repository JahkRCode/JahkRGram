import csv
import pickle
import numpy as np
import pandas as pd

def main(path_pickle,path_csv):

    file = open(path_pickle, 'rb')
    loadedPickles = pickle.load(file)
    logPickle = open(path_csv, 'wb')

    pickle.dump(loadedPickles, logPickle)

main(path_pickle='./InstagramComments_.p', path_csv='./a.csv')