import numpy as np

class matrixco:
    matriz="";


    def __init__(self,matriz):
        self.matriz = matriz;

    # ELEMENTOS A DIREITA
    def getDireita(self):
        x, y = self.matriz.shape;
        count00 = 0;
        count01 = 0;
        count10 = 0;
        count11 = 0;
        for i in range(0, x):
            for j in range(0, y - 1):
                if (self.matriz[i, j] == 0 and self.matriz[i, j + 1] == 0):
                    count00 += 1;
                if (self.matriz[i, j] == 0 and self.matriz[i, j + 1] == 255):
                    count01 += 1;
                if (self.matriz[i, j] == 255 and self.matriz[i, j + 1] == 0):
                    count10 += 1;
                if (self.matriz[i, j] == 255 and self.matriz[i, j + 1] == 255):
                    count11 += 1;
        somatorio = count00 + count01 + count10 + count11;
        return [count00, count01, count10,
                count11];

    # ELEMENTOS ABAIXO
    def getAbaixo(self):
        x,y = self.matriz.shape;
        count00 = 0;
        count01 = 0;
        count10 = 0;
        count11 = 0;
        for i in range(0, x - 1):
            for j in range(0, y):
                if (self.matriz[i, j] == 0 and self.matriz[i + 1, j] == 0):
                    count00 += 1;
                if (self.matriz[i, j] == 0 and self.matriz[i + 1, j] == 255):
                    count01 += 1;
                if (self.matriz[i, j] == 255 and self.matriz[i + 1, j] == 0):
                    count10 += 1;
                if (self.matriz[i, j] == 255 and self.matriz[i + 1, j] == 255):
                    count11 += 1;
        somatorio = count00 + count01 + count10 + count11;
        return [count00, count01, count10,
                count11];
    # ELEMENTOS A DIREITA E ACIMA
    def getDireitaeAcima(self):
        x,y = self.matriz.shape;
        count00 = 0;
        count01 = 0;
        count10 = 0;
        count11 = 0;
        for i in range(1, x):
            for j in range(0, y - 1):
                if (self.matriz[i, j] == 0 and self.matriz[i - 1, j] == 0 and self.matriz[i, j + 1] == 0):
                    count00 += 1;
                if (self.matriz[i, j] == 0 and self.matriz[i - 1, j] == 255 and self.matriz[i, j + 1] == 255):
                    count01 += 1;
                if (self.matriz[i, j] == 1 and self.matriz[i - 1, j] == 0 and self.matriz[i, j + 1] == 0):
                    count10 += 1;
                if (self.matriz[i, j] == 1 and self.matriz[i - 1, j] == 255 and self.matriz[i, j + 1] == 255):
                    count11 += 1;
        somatorio = count00 + count01 + count10 + count11;
        return [count00, count01,count10,
                count11];

    # ELEMENTOS A DIREITA E ABAIXO
    def getDireitaeAbaixo(self):
        x,y = self.matriz.shape;
        count00 = 0;
        count01 = 0;
        count10 = 0;
        count11 = 0;
        for i in range(0, x - 1):
            for j in range(0, y - 1):
                if (self.matriz[i, j] == 0 and self.matriz[i + 1, j] == 0 and self.matriz[i, j + 1] == 0):
                    count00 += 1;
                if (self.matriz[i, j] == 0 and self.matriz[i + 1, j] == 255 and self.matriz[i, j + 1] == 255):
                    count01 += 1;
                if (self.matriz[i, j] == 255 and self.matriz[i + 1, j] == 0 and self.matriz[i, j + 1] == 0):
                    count10 += 1;
                if (self.matriz[i, j] == 255 and self.matriz[i + 1, j] == 255 and self.matriz[i, j + 1] == 255):
                    count11 += 1;
        somatorio = count00+count01+count10+count11;
        return [count00,count01,count10,
                count11];
    # ATRIBUTOS DAS MATRIZES DE CO-OCORRENCIA
    def getAtributos(self):
        lista = [];
        for i in self.getDireita():
            lista.append(i);
        for i in self.getAbaixo():
            lista.append(i);
        for i in self.getDireitaeAbaixo():
            lista.append(i);
        for i in self.getDireitaeAcima():
            lista.append(i);
        return lista;
