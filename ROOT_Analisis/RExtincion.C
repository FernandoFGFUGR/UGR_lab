//Resistencia de extinción

#include "TGraph.h"
#include "TMultiGraph.h"
#include "TF1.h"
#include "TH1.h"

void RExtincion ()
{
    /*Lectura de los datos del fichero. Parala lectura declaramos dos
    listas de datos, dos vector para almacenar esas listas.
    Tal y como leemos los datos y dividimos en lista de listas estamos
    creando una de más*/
    
    vector<double> vI, vV;
    vector<vector<double>> I,V;

    ifstream ifs("/Users/ejimenez/Desktop/SiPM/Ficheros/RExtincion/RExtincion_0.txt");
    double x, y, z, y0;
    int i,count;
    y0=0;
    count=0;
    while(ifs.is_open() && !ifs.eof())
    {
      count++;
      ifs >> z >> x >> y;
      
      if(y!=0)
      {
          vI.push_back(x); //Vector para la intensidad
          vV.push_back(y); //Vector para el voltaje
      }
      else
      {
          I.push_back(vI);
          V.push_back(vV);
          vI.clear();
          vV.clear();
          vI.push_back(x);
          vV.push_back(y);
      }
      
    }
    ifs.close();
    
    cout << "Nº de bloques de datos: " << V.size() << endl;
    
    
    /*Se crean las gráficas y se ajustan los valores para la R.
    Para ello hay que acceder dentro del vector de vectores
    a cada una de las listas*/
    
    double p,r;
    vector<double> vR;
    
    TGraph *gr[V.size()-1];
    TF1 *f[V.size()-1];
    TCanvas *c1,*c2;
    
    TH1F *h = new TH1F("h","",100,45,55);
    
    for(i=0;i<=V.size()-2;i++)
    {
        gr[i] = new TGraph(V[i].size(), &V[i][0], &I[i][0]);
        f[i] = new TF1("f[i]","[0]+[1]*x",0.8,1.14);
        gr[i]->Fit("f[i]","R");
        p = f[i]->GetParameter(1);
        r=1000/p;
        vR.push_back(r);
        cout << r << endl;
        h->Fill(r);
    }
    
    //Pintamos las gráficas y los ajustes
    c1 = new TCanvas("c1","canvas");
    c1->cd(1);
    gr[1]->SetMarkerStyle(4);
    gr[1]->SetMarkerColor(1);
    gr[3]->SetMarkerStyle(26);
    gr[3]->SetMarkerColor(8);
    gr[4]->SetMarkerStyle(27);
    gr[4]->SetMarkerColor(9);

    TMultiGraph *mg = new TMultiGraph();
    mg->Add(gr[1]);
    mg->Add(gr[3]);
    mg->Add(gr[4]);

    mg->GetXaxis()->SetTitle("Voltaje [V]");
    mg->GetYaxis()->SetTitle("Intensidad [mA]");
    mg->Draw("AP");
    
    c2 = new TCanvas("c2","canvas");
    c2->cd(1);
    h->GetXaxis()->SetTitle("r(#Omega)");
    h->Draw();
}
