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

#   ESTRUTURA DO PROJETO
#   sources:
#           - DATA (FOLDER)
#               - TRAINING (FOLDERS)
#               - TESTING (FOLDERS)
#           - MAIN (FOLDER)
#               - svm7.py (FILE MAIN)
#               - caracteristicas.py (FILE)
#               - process.py (FILE)
#
#
# carregando as imagens de treinamento da base de dados MNIST
# situada em um diretorio externo ao de execucao desse arquivo
#
#

atributos = [];
saidas = [];
atributos_saida = [0,1,2,3,4,5,6,7,8,9];
# varrer todas as imagens de treinamento, de todos seus caracteres
for i in range(0,10,1):
    contador = 0;
    # abrindo cada imagem da pasta de caracteres
    for imagem in glob.glob("../data/training/"+str(i)+"/*.png"):
        # extraindo caracteristicas
        objeto = caracteristicas.wocr(imagem);
        # adicionando ao vetor multidimensional de caracteristicas
        atributos.append(objeto.atributos())
        # salvando as classes de cada imagem
        saidas.append(atributos_saida[i]);
        contador = contador + 1;
        print(imagem+" -- "+str(contador));


contador=0
saidas_teste=[]
data_test=[]
# carregar todas as imagens de teste
# situadas em um diretorio externo ao do arquivo
for i in range(0,10,1):
    contador = 0;
    for imagem in glob.glob("../data/testing/"+str(i)+"/*.png"):
        # extraindo caracteristicas
        objeto = caracteristicas.wocr(imagem);
        # salvando no vetor multidimensional de caracteristicas de teste
        data_test.append(objeto.atributos())
        saidas_teste.append(atributos_saida[i]);
        contador = contador + 1;
        print(imagem+" -- "+str(contador));
# mostrando dimensoes de cada vetor de caracteristicas
print(np.shape(atributos))
print(np.shape(data_test))
# normalizacao dos dados 
# para facilitar a compreensao do classificador
new_atbs = atributos;
data_test = np.matrix(data_test)
data_test = data_test/max(max(new_atbs))
atributos = np.matrix(atributos)
new_atbs = atributos/max(max(new_atbs))
new_atbs = np.asarray(new_atbs)
print(np.shape(atributos))
print(np.shape(data_test))

# criando um classificador SVM com estrategia de classificacao ONE AGAINST ONE
# de kernel Radial Basis Function
svm = OneVsOneClassifier(svm.SVC(C=10,kernel='rbf',gamma=0.1));
# treinamento dos dados
svm.fit(new_atbs,saidas);
# predicao dos dados
resultados = svm.predict(data_test);

# apresentacao do desempenho do classificador
print("PRECISION/RECALL/F1-SCORE");
print metrics.classification_report(saidas_teste,resultados);
print("ACCURACY")
print metrics.accuracy_score(saidas_teste,resultados)
print("Matriz de Confusao")
print metrics.confusion_matrix(saidas_teste,resultados);
b = time.time();

c = b-a;
print("tempo "+str(c));
