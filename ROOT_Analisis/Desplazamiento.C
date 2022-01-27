#include "TCanvas.h"
#include "TMath.h"
#include "TH1.h"
#include "TF1.h"
#include "TRandom.h"
#include "TSpectrum.h"
#include "TVirtualFitter.h"

/*Se generan una serie de funciones gaussianas de forma aleatoria que serán
utilizadas posteriormente para ajustar los picos encontrados con la función
'search'. Estas gaussianas servirán para encontrar el valor de la ganancia
al ser calculada esta como la diferencia de distancia entre los picos
encontrados (ratio de carga recogida)*/

Int_t npeaks=10;
Double_t fpeaks(Double_t *x, Double_t *par) {
    Double_t  result = 0;
    for (Int_t p=0;p<npeaks;p++) {
        Double_t norm  = par[3*p];
        Double_t mean  = par[3*p+1];
        Double_t sigma = par[3*p+2];
        
        result += norm*TMath::Gaus(x[0],mean,sigma);
    }
    return result;
}

/*Comienza lo que es realmente la macro utilizada para la localizacion de los
picos y el cálculo de la ganancia.
Al comienzo se declaran las variables que van a almacenar el valor para el rango
del histograma original y se leen los valores desde fichero. Estos valores son
los que rellenan este primer histograma.*/

void Desplazamiento(Int_t np=10) {
    
    TH1F *h,*h2,*h3;
    double min, max;
    string fileName = "/Users/ejimenez/Desktop/SiPM/Ficheros/Ganancia/testx.txt";
    ifstream ifs(fileName.c_str());
    
    ifs >> min >> max;
    cout << min << " " << max << endl;
    
    npeaks = TMath::Abs(np);
    h = new TH1F("h","",250/*500*/,min/*9*/,max/*9*/);
    
    int count=0;
    double valor;
    vector<double> vs;
    if(!ifs.is_open()){
        cout << "Error al abrir el fichero" << endl;
    }
    else{
        while(ifs.is_open() && !ifs.eof()){
            count++;
            ifs >> valor;
            h->Fill(valor);
            vs.push_back(valor);
        }
    }
    ifs.close();
    
    
    int entradas = h->GetEntries();
    cout << "Entradas: " << entradas << endl;
    
// Generate n peaks at random
    Double_t par[3*npeaks];
    
    
/*Buscamos los candidatos a pico a través de TSpectrum. Declaramos la variable
's' asociada como puntero a la clase ya mencionada.
Ponemos dos veces más de picos de los que se esperan para que no se generen
problemas con el almacenamiento. Buscamos los picos a través de 'Search'. Las
variables de esta función son el histograma en el que buscar, la desviación
opciones del algoritmo de búsquedad y el umbral bajo el cual se descartan
los picos (este umbral variará en función de los datos analizados.)*/
    
    TSpectrum *s = new TSpectrum(2*npeaks);
    Int_t nfound = s->Search(h,2/*2*/,"nobackground noMarkov",0.2/*0.015*/);
    printf("Found %d candidate peaks to fit\n",nfound);
    if (np <0) return;
    
/*Loop on all found peaks. Eliminate peaks at the background level.
Encontrados los picos, se inicializan los parámetros de las guassinas a través
de la posición de los mismo. (La desviación es una cte, entiendo que será un
parámetro variable)*/
    
    npeaks = 0;
    Double_t *xpeaks;
    xpeaks = s->GetPositionX();
    
    for (Int_t p=0;p<nfound;p++)
    {
        Double_t xp = xpeaks[p];
        Int_t bin = h->GetXaxis()->FindBin(xp);
        Double_t yp = h->GetBinContent(bin);
        par[3*npeaks] = yp; // "norm"
        par[3*npeaks+1] = xp; // "mean"
        par[3*npeaks+2] = 1.e-11/*1.e-11*/; // "sigma"
        npeaks++;
    }

/*Desplazamiento de los picos y el resto de puntos del histograma para ajustar
el pedestal de ruido electrónico a cero.
Lo primero es calcular la distancia que hay entre el centro del pico del
pedestal al cero del eje de abcisas. Una vez hecho esto se desplazan todos los
puntos del histograma esa misma cantidad.*/

    int i;
    double dist,min1,max1;
        
    dist=par[1];
    cout << "Distancia al origen del primer pico: " << dist << endl;
    if(dist>0)
    {
        min1=min-dist;
        max1=max-dist;
    }
    else
    {
        min1=min-dist;
        max1=max-dist;
    }
    
    
    for(i=0;i<vs.size();i++)
    {
        if(dist>0)
            vs.at(i)=vs.at(i)-dist;
        else
            vs.at(i)=vs.at(i)-dist;
    }
        
        
    h3 = new TH1F("h3","",250,min1,max1);
    for(i=0;i<vs.size();i++)
        h3->Fill(vs.at(i));
    
    TCanvas *c1 = new TCanvas("c1","c1",10,10,800,600);
    c1->cd(1);
    h3->SetStats(0);
    h3->SetLineWidth(2);
    h3->SetLineColor(1);
    h3->GetYaxis()->SetTitle("Counts");
    h3->GetXaxis()->SetTitle("Charge [V #times s]");
    h3->Draw();
    
    h2 = (TH1F*)h3->Clone("h2");

/*Habiendo desplazado todos los puntos para que se centre el pedestal en cero,
volvemos a buscar los picos*/

    TSpectrum *s1 = new TSpectrum(2*npeaks);
    nfound = s1->Search(h3,2/*2*/,"nobackground noMarkov",0.2/*0.015*/);
    printf("Found %d candidate peaks to fit\n",nfound);
    if (np <0) return;

// Loop on all found peaks. Eliminate peaks at the background level

    npeaks = 0;
    xpeaks = s1->GetPositionX();
    
    TLine* line[nfound];
        
    for (Int_t p=0;p<nfound;p++)
    {
        Double_t xp = xpeaks[p];
        Int_t bin = h3->GetXaxis()->FindBin(xp);
        Double_t yp = h3->GetBinContent(bin);
        par[3*npeaks] = yp; // "norm"
        par[3*npeaks+1] = xp; // "mean"
        par[3*npeaks+2] = 1.e-11/*1.e-11*/; // "sigma"
            
        line[p]= new TLine(xp,0.,xp,yp);
        line[p]->SetLineColor(9);
        line[p]->SetLineWidth(1);
        line[p]->SetLineStyle(kDashed);
        line[p]->Draw("same");
            
        cout<<"peak "<<p<<" norm: "<<yp<<"  mean: "<<xp<<" sigma: "<<par[3*npeaks+2]<<endl;
        npeaks++;
    }

/*Ajustamos los picos encontrados a las funciones gaussianas correspondientes*/

    printf("Found %d useful peaks to fit\n",npeaks);
    printf("Now fitting: Be patient\n");
    TF1 *fit = new TF1("fit",fpeaks,-5.e-9/*9*/,42.e-9/*9*/,3*npeaks);
    fit->SetParameters(par);
    fit->SetNpx(1000);
    for (Int_t p=0;p<nfound;p++)
    {
        cout<<"means are: par"<<3*p+1<<"  :"<<par[3*p+1]<<endl;
        fit->FixParameter(3*p+1,par[3*p+1]);
    }
    
    h2->Fit("fit", "QR0");
    fit->SetLineColor(4);
    //fit->Draw("same");
    double Rscope = 1000000/*50.*/;//Ohms
    double e = 1.6e-19;//Coulombs
    double Gain = (par[4] - par[1])/(Rscope*e);
    cout << Gain << endl;
        
    TLatex *ganancia = new TLatex();
    ganancia->SetTextSize(0.03);
    char num[60];
    sprintf(num,"Gain = %2.2e",Gain);
    ganancia->DrawLatex(par[4]*1.3, par[3], num);
}

