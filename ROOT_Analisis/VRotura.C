//Voltaje de rutura

#include "TGraph.h"
#include "TF1.h"

void VRotura ()
{
    //Lectura de los datos del fichero
    vector<double> vI,vV;
    vector<vector<double>> I,V,VBR;
    
    ifstream ifs("/Users/ejimenez/Desktop/SiPM/Ficheros/VRotura/Completo.txt");
    double x,y,z,y0;
    int count=0;
    y0=0;
    while(ifs.is_open() && !ifs.eof())
    {
        count++;
        ifs >> z >> x >> y;
        
        if(y>=y0)
        {
            vI.push_back(x);
            vV.push_back(y);
            y0=y;
        }
        else
        {
            I.push_back(vI);
            V.push_back(vV);
            vI.clear();
            vV.clear();
            vI.push_back(x);
            vV.push_back(y);
            y0=0;
        }
        
    }
    ifs.close();
    
    cout << V.size() << endl;
    /*int n;
    for(n=0;n<6;n++)
    {
        cout << I[n][0] << " " << V[n][0] << endl;
    }*/
    
    
    //Tenemos que calcular dI/dV para hallar el máximo
    int i,j;
    double difI,difV,dif;
    vector<double> result;
    for(i=0;i<V.size();i++)
    {
        for(j=0;j<V[i].size();j++)
        {
            difI=I[i][j+1]-I[i][j];
            difV=V[i][j+1]-V[i][j];
            dif=(1/I[i][j])*(difI/difV);
            result.push_back(dif);
        }
        VBR.push_back(result);
        result.clear();
    }
    
    cout << VBR.size() << endl;
    
    //Graficamos el resultado y ajustamos el pico
    double p;
    vector<double> vR;
    
    TGraph *gr[V.size()],*gr1[V.size()];
    TF1 *f[V.size()];
    TCanvas *c1,*c2,*c3;
    
    TH1F *h = new TH1F("h","",100,31,33);
    
    for(i=0;i<V.size();i++)
    {
        gr[i]=new TGraph(V[i].size(), &V[i][0], &I[i][0]);
        gr1[i]=new TGraph(V[i].size(), &V[i][0], &VBR[i][0]);
        f[i]=new TF1("f[i]","gaus(0)",31,34);
        gr1[i]->Fit("f[i]","R");
        p = f[i]->GetParameter(1);
        vR.push_back(p);
        h->Fill(p);
    }
    
    //Pintamos los datos y el ajuste
    c1 = new TCanvas("c1","canvas");
    c1->cd(1);
    
    gr[0]->SetMarkerStyle(4);
    gr[0]->SetMarkerColor(1);
    gr[1]->SetMarkerStyle(26);
    gr[1]->SetMarkerColor(8);
    gr[2]->SetMarkerStyle(27);
    gr[2]->SetMarkerColor(9);

    TMultiGraph *mg = new TMultiGraph();
    mg->Add(gr[0]);
    mg->Add(gr[1]);
    mg->Add(gr[2]);
    mg->GetXaxis()->SetTitle("Voltaje [V]");
    mg->GetYaxis()->SetTitle("Intenidad [mA]");
    mg->Draw("AP");
    
    c2 = new TCanvas("c2","canvas");
    c2->cd(1);
    gr1[0]->SetMarkerStyle(4);
    gr1[0]->SetMarkerColor(1);
    gr1[1]->SetMarkerStyle(26);
    gr1[1]->SetMarkerColor(8);
    gr1[2]->SetMarkerStyle(27);
    gr1[2]->SetMarkerColor(9);

    TMultiGraph *mg1 = new TMultiGraph();
    mg1->Add(gr1[0]);
    mg1->Add(gr1[1]);
    mg1->Add(gr1[2]);
    mg1->GetXaxis()->SetTitle("Voltaje [V]");
    mg1->GetYaxis()->SetTitle("1/I*dI/dV");
    mg1->Draw("AP");
    
    c3 = new TCanvas("c3","canvas");
    c3->cd(1);
    h->GetXaxis()->SetTitle("V_{br} (V)");
    h->Draw();
}
