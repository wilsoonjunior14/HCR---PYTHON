from sklearn import datasets
from sklearn import svm
from sklearn.multiclass import OneVsRestClassifier
from sklearn.multiclass import OneVsOneClassifier
from sklearn.multiclass import OutputCodeClassifier
import numpy as np
import caracteristicas
import glob
from scipy.sparse import *
from sklearn.feature_selection import VarianceThreshold
from sklearn.decomposition import PCA
import segmentation
import cv2
import time
from sklearn import metrics

a = time.time();


atributos = [];
saidas = [];
atributos_saida = [0,1,2,3,4,5,6,7,8,9];
for i in range(0,10,1):
    contador = 0;
    for imagem in glob.glob("../data/training/"+str(i)+"/*.png"):
        objeto = caracteristicas.wocr(imagem);
        atributos.append(objeto.atributos())
        saidas.append(atributos_saida[i]);
        contador = contador + 1;
        print(imagem+" -- "+str(contador));


contador=0
saidas_teste=[]
data_test=[]
for i in range(0,10,1):
    contador = 0;
    for imagem in glob.glob("../data/testing/"+str(i)+"/*.png"):
        objeto = caracteristicas.wocr(imagem);
        data_test.append(objeto.atributos())
        saidas_teste.append(atributos_saida[i]);
        contador = contador + 1;
        print(imagem+" -- "+str(contador));

print(np.shape(atributos))
print(np.shape(data_test))
new_atbs = atributos;
data_test = np.matrix(data_test)
data_test = data_test/max(max(new_atbs))
atributos = np.matrix(atributos)
new_atbs = atributos/max(max(new_atbs))
new_atbs = np.asarray(new_atbs)
print(np.shape(atributos))
print(np.shape(data_test))

svm = OneVsOneClassifier(svm.SVC(C=10,kernel='rbf',gamma=0.1));
svm.fit(new_atbs,saidas);
resultados = svm.predict(data_test);

print("PRECISION/RECALL/F1-SCORE");
print metrics.classification_report(saidas_teste,resultados);
print("ACCURACY")
print metrics.accuracy_score(saidas_teste,resultados)
print("Matriz de Confusao")
print metrics.confusion_matrix(saidas_teste,resultados);
b = time.time();

c = b-a;
print("tempo "+str(c));
