import numpy as np
from numpy import linalg as LA
import sys

#Find a directed (and documented) network graph and analyze using page rank.
#Please vary the probability and report what happens to the pagerank vector.

#Exercise 11. Consider again the web in Figure 2.1, with the addition of a page 5 that links to
#page 3, where page 3 also links to page 5. Calculate the new ranking by finding the eigenvector of
#M (corresponding to lambda = 1) that has positive components summing to one. Use m = 0.15.
#Exercise 12. Add a sixth page that links to every page of the web in the previous exercise, but
#to which no other page links. Rank the pages using A, then using M with m = 0.15, and compare
#the results.

if len(sys.argv)<=1:
	filename="wolfe_primates.csv"
else:
    filename = sys.argv[1]


def getdata(filename):  #opens file as matrix and adds columns or rows with 1's on the diagonal to make square
    datamatrix = np.genfromtxt(filename, delimiter=',')
    #datamatrix = np.array([[0.5, 0], [0, 1], [0.5,0]])
    #datamatrix=np.array([[0,0,0,0.5,0],[0.33,0,0,0,0],[0.33,0.5,0,0.5,1]])
    #data for num11
    #datamatrix=np.array([[0,0,0,0.5,0],[0.33,0,0,0,0],[0.33,0.5,0,0.5,1],[0.33,0.5,0.5,0,0],[0,0,0.5,0,0]])
    #data for num12
    #datamatrix = np.array(
    #   [[0, 0, 0, 0.5, 0, 0.2], [0.33, 0, 0, 0, 0, 0.2], [0.33, 0.5, 0, 0.5, 1,0.2], [0.33, 0.5, 0.5, 0, 0,0.2], [0, 0, 0.5, 0, 0,0.2],[0,0,0,0,0,0]])
    height,width = datamatrix.shape
    nsize=np.maximum(width, height)
    if width==nsize:
        for i in range(nsize - height):
            datamatrix=np.vstack((datamatrix,np.repeat(0.0, width)))

    elif height==nsize:
        datamatrix=np.transpose(datamatrix)
        for i in range(nsize-width):
            datamatrix = np.vstack((datamatrix,np.repeat(0.0, height)))
        datamatrix = np.transpose(datamatrix)
    else:
        print "What happened with your dimensions, dude?"
        return None
    print width,height, nsize
    colsums = datamatrix.sum(axis=0)
    for i in range(nsize):
        if colsums[i]==0:
            datamatrix[i][i] = 1
    return datamatrix


def colstochastic(filename): #makes it column stoachastic
    datamatrix=getdata(filename)
    width, height = datamatrix.shape
    colsums=datamatrix.sum(axis=0)
    CSmatrix=np.empty([width, height])
    for i in range(height):
        for j in range(width):
            CSmatrix[j,i]=np.divide(datamatrix[j,i], colsums[i])
    #print CSmatrix
    return CSmatrix

def googlematrix(filename,alpha):  #applies the google formula
    CSMatrix=colstochastic(filename)
    width, height = CSMatrix.shape
    A=np.multiply(1-alpha,CSMatrix)
    numpoints=np.multiply(width,height)
    array= np.repeat(1.0, numpoints).reshape(width, height)
    B = np.multiply(alpha/height, array)
    GMatrix=np.add(A,B)
    powerM=LA.matrix_power(GMatrix, 100)
    return powerM

def pagerank(filename,alpha): #finds the eigenvector and returns the maximum value
    #the eigenspace of a positive, column stochastic matrix has dimension 1
    matrix=googlematrix(filename, alpha)
    width, height = matrix.shape
    x = np.repeat(1.0 / height, height)
    PRvector = matrix.dot(x)
    print "the page rank vector is", PRvector
    maxrank=np.amax(PRvector)
    index = np.where(PRvector == maxrank)
    print "The maximum rank is:", maxrank
    print "From node:", index[0][0]+1
    return (PRvector, maxrank, index[0][0])


def randp(filename, numtrials): #runs a series of trials on pagerank with different probabilities
    randalpha=np.random.uniform(0,1, numtrials)
    alpharanks=[]
    alphaindices=[]
    for i in range(len(randalpha)):
        run=pagerank(filename, randalpha[i])
        alpharanks.append(run[1])
        alphaindices.append(run[2]+1)
    resultsmatrix = np.vstack((randalpha, alpharanks))
    resultsmatrix = np.vstack((resultsmatrix, alphaindices))
    print "The random alphas are",randalpha
    print "The winning rank for each alpha is", alpharanks
    print "The winning index for each alpha is", alphaindices
    return resultsmatrix



randp('wolfe_primates.csv',10)







