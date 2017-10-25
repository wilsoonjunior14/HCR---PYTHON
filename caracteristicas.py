import scipy.ndimage as nd
import scipy.misc as ms
import cv2
import numpy as np

class wocr:
    imagem = "";

    def __init__(self,link):
        #obj = process.Processamento(link);
        self.imagem = nd.imread(link, 1)
        self.imagem = 255 - self.imagem;
        #self.imagem = cv2.equalizeHist(self.imagem);
        self.imagem = self.prepara_imagem();

    # CALCULA A DISTANCIA ENTRE DOIS PONTOS
    def distancia(self,x1, y1, x2, y2):
        return np.sqrt(np.power(y2 - y1, 2) + np.power(x2 - x1, 2));

    # DIVIDE A IMAGEM EM REGIOES
    def regiao(self,xi,xf,yi,yf):
        contador = 0;
        for i in range(xi,xf):
            for j in range(yi,yf):
                if(self.imagem[i,j] == 0):
                    contador = contador + 1;
        return float(contador);

    # FAZ A BINARIZACAO DA IMAGEM
    def prepara_imagem(self):
        x,y = self.imagem.shape;
        for i in range(0,x):
            for j in range(0,y):
                if(self.imagem[i,j] < 150):
                    self.imagem[i,j] = 0;
                else:
                    self.imagem[i,j] = 1;
        return self.imagem;

    # PERCORRE A IMAGEM EM BUSCA DE PIXELS PRETOS
    def percorre(self,imagem, xi, xf, step1, yi, yf, step2):
        for i in range(xi, xf, step1):
            for j in range(yi, yf, step2):
                if (imagem[i, j] == 0):
                    return [i, j];

    # CALCULA AREA DA IMAGEM
    def calcula_area(self,imagem):
        x, y = imagem.shape;
        contador = 0;
        for i in range(0, x):
            for j in range(0, y):
                if (imagem[i, j] == 0):
                    contador = contador + 1;
        return float(contador);

    # CALCULA PERIMETRO DA IMAGEM
    def calcula_perimetro(self,imagem):
        kernel = np.ones((2, 2), np.uint8);
        erode = cv2.erode(imagem, iterations=1, kernel=kernel);
        imagem_borda = imagem - erode;
        x, y = imagem.shape;
        contador = 0;
        for i in range(0, x):
            for j in range(0, y):
                if (imagem_borda[i, j] == 255):
                    contador = contador + 1;
        return float(contador);

    # ENCONTRA PONTOS DE PIXELS
    def ponto(self,imagem):
        x, y = imagem.shape;
        pontos = [];
        for i in range(0, x):
            linha = [];
            for j in range(0, y):
                if (imagem[i, j] == 0):
                    linha.append([i, j]);
            if (linha.__len__() > 1):
                pontos.append(linha[0]);
                pontos.append(linha[linha.__len__() - 1]);
        return pontos;

    def histograma_horizontal(self,imagem):
        return sum((np.transpose(imagem)==0));

    def histograma_vertical(self,imagem):
        return sum((imagem==0));

    def borda_topo(self):
        x, y = np.shape(self.imagem);
        pontos = [];
        for i in range(0, x, 1):
            for j in range(0, y, 1):
                if (self.imagem[i, j] == 0):
                    pontos.append(self.distancia(0,j,i,j));
        return min(pontos);

    def borda_esquerda(self):
        x,y = np.shape(self.imagem);
        pontos=[];
        for i in range(0,x,1):
            for j in range(0,y,1):
                if(self.imagem[j,i] == 0):
                    pontos.append(self.distancia(j,0,j,i));
        return min(pontos);

    def borda_direita(self):
        x,y = self.imagem.shape;
        pontos=[];
        pts = [];
        for i in range(0,x,1):
            for j in range(y-1,0,-1):
                if(self.imagem[i,j]==0):
                    pts.append([i,j])
                    pontos.append(self.distancia(i,y-1,i,j));
        return min(pontos);

    def borda_baixo(self):
        x,y = self.imagem.shape;
        pontos=[];
        for i in range(x-1,0,-1):
            for j in range(0,y,1):
                if(self.imagem[i,j]==0):
                    pontos.append(self.distancia(x-1,j,i,j));
        return min(pontos);

    def borda_diag_esq_baixo(self):
        x,y = self.imagem.shape;
        pontos=[];
        for i in range(0,x):
            for j in range(0,y):
                if(i==j and self.imagem[i,j]==0):
                    pontos.append(self.distancia(0,0,i,j));
        if (pontos.__len__() == 0):
            return self.distancia(0, 0, x, y);
        else:
            return min(pontos);

    def borda_diag_esq_cima(self):
        x,y = self.imagem.shape;
        pontos=[];
        for i in range(x-1,0,-1):
            for j in range(0,y):
                if(i==j and self.imagem[i,j]==0):
                    pontos.append(self.distancia(x-1,0,i,j));
        if(pontos.__len__()==0):
            return self.distancia(0,0,x,y);
        else:
            return min(pontos);

    def borda_diag_dir_baixo(self):
        x,y = self.imagem.shape;
        pontos=[];
        for i in range(0,x):
            for j in range(y-1,0,-1):
                if(i==j and self.imagem[i,j]==0):
                    pontos.append(self.distancia(0,y-1,i,j));
        if (pontos.__len__() == 0):
            return self.distancia(0, 0, x, y);
        else:
            return min(pontos);

    def borda_diag_dir_cima(self):
        x,y = self.imagem.shape;
        pontos=[];
        for i in range(x-1,0,-1):
            for j in range(y-1,0,-1):
                if(i==j and self.imagem[i,j]==0):
                    pontos.append(self.distancia(x-1,y-1,i,j));
        if (pontos.__len__() == 0):
            return self.distancia(0, 0, x, y);
        else:
            return min(pontos);

    def faixa_hor_esq_dir(self,xi,xf,yi,yf):
        x,y = self.imagem.shape;
        pontos=[];
        for i in range(xi,xf,-1):
            for j in range(yi,yf,1):
                if(self.imagem[i,j]==0):
                    pontos.append(self.distancia(x-1,j,i,j));
        if(pontos.__len__()==0):
            return self.distancia(0,0,x,y);
        else:
            return min(pontos);

    def faixa_hor_dir_esq(self, xi, xf, yi, yf):
        x, y = self.imagem.shape;
        pontos = [];
        for i in range(xi, xf, 1):
            for j in range(yi, yf, 1):
                if (self.imagem[i, j] == 0):
                    pontos.append(self.distancia(0, j, i, j));
        if (pontos.__len__() == 0):
           return self.distancia(0, 0, x, y);
        else:
           return min(pontos);

    def faixa_ver_esq_dir(self,xi,xf,yi,yf):
        x,y = self.imagem.shape;
        pontos=[];
        for i in range(xi,xf,1):
            for j in range(yi,yf,1):
                if (self.imagem[i, j] == 0):
                    pontos.append(self.distancia(i,0,i,j));
        if (pontos.__len__() == 0):
           return self.distancia(0, 0, x, y);
        else:
           return min(pontos);

    def faixa_ver_dir_esq(self, xi, xf, yi, yf):
        x, y = self.imagem.shape;
        pontos = [];
        for i in range(xi, xf, 1):
            for j in range(yi, yf, -1):
                if (self.imagem[i, j] == 0):
                    pontos.append(self.distancia(i, y-1, i, j));
        if (pontos.__len__() == 0):
             return self.distancia(0, 0, x, y);
        else:
             return min(pontos);

    def density(self):
        x, y = self.imagem.shape;
        densidade = [];
        for i in range(0, x - 6, 7):
            for j in range(0, y - 6, 7):
                densidade.append(float(sum(sum(self.imagem[i:i + 7, j:j + 7] == 0))));
        return densidade;

    def profiles(self,profiles):
        x,y = self.imagem.shape
        for i in range(0, x):
            booleano = False;
            for j in range(0, y):
                if (self.imagem[i, j] == 0 and not booleano):
                    profiles.append(self.distancia(i, 0, i, j));
                    booleano = True;
            if (not booleano):
                profiles.append(self.distancia(0, 0, 0, 28));

        for i in range(0, x):
            booleano = False;
            for j in range(y - 1, 0, -1):
                if (self.imagem[i, j] == 0 and not booleano):
                    profiles.append(self.distancia(i,0,i,j));
                    booleano = True;
            if (not booleano):
                profiles.append(self.distancia(0,0,0,28));

        for i in range(0, x):
             booleano = False;
             for j in range(0, y, 1):
                 if (self.imagem[j, i] == 0 and not booleano):
                    profiles.append(self.distancia(0, i, j, i));
                    booleano = True;
             if (not booleano):
                 profiles.append(self.distancia(0,0,0,28))

        for i in range(x - 1, -1, -1):
              booleano = False;
              for j in range(x - 1, -1, -1):
                  if (self.imagem[j, i] == 0 and not booleano):
                    profiles.append(self.distancia(x, i, j, i));
                    booleano = True;
                        # new_img[j:x, i] = 255;
              if (not booleano):
                  profiles.append(self.distancia(0,0,0,28));

    def crossings(self,atb):
        x, y = np.shape(self.imagem)
        for i in range(0, x):
            count = 0
            for j in range(0, y - 1):
                if (self.imagem[i, j] == 1 and self.imagem[i, j + 1] == 0):
                    count += 1
            atb.append(count)

        for i in range(0, x):
            count = 0
            for j in range(0, y - 1):
                if (self.imagem[j, i] == 1 and self.imagem[j + 1, i] == 0):
                    count += 1
            atb.append(count)

    # CONSTROI TODOS OS ATRIBUTOS DA IMAGEM
    def atributos(self):
        atb = [];
        x,y = self.imagem.shape;

        #regiao 4x4
        #atb.append(self.regiao(0,x/4,0,y/4)/self.calcula_area(self.imagem));
        #atb.append(self.regiao(x/4,x/2,0,y/4)/self.calcula_area(self.imagem));
        #atb.append(self.regiao(x/2,(3*x)/4,0,y/4)/self.calcula_area(self.imagem));
        #atb.append(self.regiao((3*x)/4,x,0,y/4)/self.calcula_area(self.imagem));

        #atb.append(self.regiao(0,x/4,y/4,y/2)/self.calcula_area(self.imagem));
        #atb.append(self.regiao(x/4,x/2,y/4,y/2)/self.calcula_area(self.imagem));
        #atb.append(self.regiao(x/2,(3*x)/4,y/4,y/2)/self.calcula_area(self.imagem));
        #atb.append(self.regiao((3*x)/4,x,y/4,y/2)/self.calcula_area(self.imagem));

        #atb.append(self.regiao(0,x/4,y/2,(3*y)/4)/self.calcula_area(self.imagem));
        #atb.append(self.regiao(x/4,x/2,y/2,(3*y)/4)/self.calcula_area(self.imagem));
        #atb.append(self.regiao(x/2,(3*x)/4,y/2,(3*y)/4)/self.calcula_area(self.imagem));
        #atb.append(self.regiao((3*x)/4,x,y/2,(3*y)/4)/self.calcula_area(self.imagem));

        #atb.append(self.regiao(0,x/4,(3*y)/4,y)/self.calcula_area(self.imagem));
        #atb.append(self.regiao(x/4,x/2,(3*y)/4,y)/self.calcula_area(self.imagem));
        #atb.append(self.regiao(x/2,(3*x)/4,(3*y)/4,y)/self.calcula_area(self.imagem));
        #atb.append(self.regiao((3*x)/4,x,(3*y)/4,y)/self.calcula_area(self.imagem));

        #regiao 4x1
        #atb.append(self.regiao(0,x/4,0,y)/self.calcula_area(self.imagem));
        #atb.append(self.regiao(x/4,x/2,0,y)/self.calcula_area(self.imagem));
        #atb.append(self.regiao(x/2,(3*x)/4,0,y)/self.calcula_area(self.imagem));
        #atb.append(self.regiao((3*x)/4,x,0,y)/self.calcula_area(self.imagem));

        #regiao 1x4
        #atb.append(self.regiao(0,x,0,y/4)/self.calcula_area(self.imagem));
        #atb.append(self.regiao(0,x,y/4,y/2)/self.calcula_area(self.imagem));
        #atb.append(self.regiao(0,x,y/2,(3*y)/4)/self.calcula_area(self.imagem));
        #atb.append(self.regiao(0,x,(3*y)/4,y)/self.calcula_area(self.imagem));

        # coloca histogramas
        # histograma horizontal
        hist_horizontal = self.histograma_horizontal(self.imagem);
        for value in hist_horizontal:
           atb.append(float(value));

        # histograma vertical
        hist_vertical = self.histograma_vertical(self.imagem);
        for value in hist_vertical:
           atb.append(float(value));

        #huM = cv2.HuMoments(cv2.moments(self.imagem));
        #for i in huM:
        #    atb.append(i[0]);

        #MOMENTOS DE ZERNIKE
        #atb.append(zernik.Zernikemoment(self.imagem,0,0)[1]);
        #atb.append(zernik.Zernikemoment(self.imagem, 1, 1)[1]);
        #atb.append(zernik.Zernikemoment(self.imagem, 2, 0)[1]);
        #atb.append(zernik.Zernikemoment(self.imagem, 2, 2)[1]);
        #atb.append(zernik.Zernikemoment(self.imagem, 3, 1)[1]);
        #atb.append(zernik.Zernikemoment(self.imagem, 3, 3)[1]);
        #atb.append(zernik.Zernikemoment(self.imagem, 4, 0)[1]);
        #atb.append(zernik.Zernikemoment(self.imagem, 4, 2)[1]);
        #atb.append(zernik.Zernikemoment(self.imagem, 4, 4)[1]);
        #atb.append(zernik.Zernikemoment(self.imagem, 5, 1)[1]);
        #atb.append(zernik.Zernikemoment(self.imagem, 5, 3)[1]);
        #atb.append(zernik.Zernikemoment(self.imagem, 5, 5)[1]);


        # ATRIBUTOS DE CO-OCORRENCIA
        #for k in matrixco.matrixco(self.imagem).getAtributos():
        #   atb.append(k);
        #atb.append(self.borda_esquerda());
        #atb.append(self.borda_topo());
        #atb.append(self.borda_direita());
        #atb.append(self.borda_baixo());
        #atb.append(self.borda_diag_esq_cima());
        #atb.append(self.borda_diag_esq_cima());
        #atb.append(self.borda_diag_dir_cima());
        #atb.append(self.borda_diag_dir_baixo());

        # METODO DAS BORDAS COM FAIXAS SOBREPOSTAS
        #atb.append(self.faixa_hor_esq_dir(27,0,0,6));
        #atb.append(self.faixa_hor_esq_dir(27,0,7,13));
        #atb.append(self.faixa_hor_esq_dir(27,0,14,20));
        #atb.append(self.faixa_hor_esq_dir(27,0,21,27));
        #atb.append(self.faixa_hor_dir_esq(0,27,0,6));
        #atb.append(self.faixa_hor_dir_esq(0,27,7,13));
        #atb.append(self.faixa_hor_dir_esq(0,27,14,20));
        #atb.append(self.faixa_hor_dir_esq(0,27,21,27));
        #atb.append(self.faixa_ver_esq_dir(0, 6, 0, 27));
        #atb.append(self.faixa_ver_esq_dir(7, 13, 0, 27));
        #atb.append(self.faixa_ver_esq_dir(14, 20, 0, 27));
        #atb.append(self.faixa_ver_esq_dir(21, 27, 0, 27));
        #atb.append(self.faixa_ver_dir_esq(0, 6, 27, 0));
        #atb.append(self.faixa_ver_dir_esq(7, 13, 27, 0));
        #atb.append(self.faixa_ver_dir_esq(14, 20, 27, 0));
        #atb.append(self.faixa_ver_dir_esq(21, 27, 27, 0));

        # DENSIDADES REGIONAIS
        #for i in self.density():
        #    atb.append(i);

        self.profiles(atb)
        #self.crossings(atb)

        #IMAGEM
        #for i in range(0,x):
         #   for j in range(0,y):
         #       atb.append(self.imagem[i,j]);


        return atb;
