/*El código está preparado para leer un solo fichero o más de uno, según el
número de pruebas introduciro (nº de ficheros con los que se trabaja).
Los ficheros deben de tener el mismo nombre cambiando el ID.

Tras almacenar los datos en bloques correspondientes a cada array de cada
una de las board, se realiza el ajuste lineal de la curva IV para hallar la
resistencia.
Para dicho ajuste se trabaja en un rango concreto, por lo tanto este rango es
uno de los parámetros que puede variar al trabajar en condiciones de medida
disintas.
 
Tras calcular el valor de la resistencia y almacenar los resultados en un
histograma general. Después se generan otros para identificar cada una de
las board a través de colores.
Finalmente se generan los plot que contienen la información.
De forma opcional se pintan las curvas IV para comprobar que las medidas se
realicen correctamente y que no falle ningún array.*/

void RExtincion_V ()
{
    vector<double> vI, vV;
    vector<vector<double>> I,V;
    string cad,cad1,cad2,cad3;

    ifstream fich;
    double x,y,z,y0;
    int i,j,n,m;
    y0=0;
    
    m=1;
    
    cad1="/Users/ejimenez/Desktop/SiPM/Ficheros/RExtincion/FRIO/board";
    cad3="_direct.txt";
    
    cout << "Introduzca el numero de pruebas: ";
    cin >> n;
    
    for(i=0;i<n;i++)
    {
        cad2=to_string(m);
        cad=cad1+cad2+cad3;
        cout << cad << endl;
        fich.open(cad.c_str());
        
        fich >> z >> x >> y;
        
        while(fich.is_open() && !fich.eof())
        {
          fich >> z >> x >> y;
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
        fich.close();
        m++;
    }
    
    cout << "Nº de bloques de datos: " << V.size() << endl;
    
    double p,res;
    vector<double> r;
    
    TGraph *gr[V.size()];
    TF1 *f[V.size()];
    TCanvas *c1,*c2,*c3;
    
    TH1F *h = new TH1F("h","",30,50,60);

    for(i=0;i<V.size();i++)
    {
        gr[i] = new TGraph(V[i].size(), &V[i][0], &I[i][0]);
        f[i] = new TF1("f[i]","[0]+[1]*x",0.7,1.05);// At T_room 0.7,1.05
        //gr[i]->Fit("f[i]","R");
        p = f[i]->GetParameter(1);
        res=1000/p;
        r.push_back(res);
        h->Fill(res);
    }
    
    /*cout << r.size() << endl;
    for(i=0;i<6;i++)
        cout << i << " " << r.at(i) << endl;*/
    
    m=1;
    TH1F *h1[r.size()/6];
    
    for(i=0;i<r.size()/6;i++)
    {
        cad1="h"+to_string(m);
        cad2="board"+to_string(m);
        h1[i]=new TH1F(cad1.c_str(),cad2.c_str(),30,50,60);
        m++;
    }
    
    m=1;
    i=j=0;
    while(j<r.size())
    {
        if(j<6*m)
        {
            h1[i]->Fill(r.at(j));
            j++;
        }
        else
        {
            h1[i+1]->Fill(r.at(j));
            i++;
            j++;
            m++;
            //cout << i << " " << j << " " << m << endl;
        }
    }
    
    THStack *hs = new THStack("hs","");
    for(i=0;i<r.size()/6;i++)
        hs->Add(h1[i]);
    
    c1 = new TCanvas("c1","Histograma");
    c1->cd(1);
    //h->SetTitle("R_{q} at T_{Room}");
    h->GetXaxis()->SetTitle("R_{q}(#Omega)");
    h->Draw("");
    
    c2 = new TCanvas("c2","Conjunto");
    gStyle->SetPalette(1);
    c2->cd(1);
    hs->Draw("PFC"); //nostack
    //hs->SetTitle("LN2");
    hs->GetXaxis()->SetTitle("R_{q}(#Omega)");
    gPad->BuildLegend(0.3,0.21,0.3,0.21,"");
    
    //Curvas IV
    c3 = new TCanvas("c3","canvas");
    c3->cd(1);
    gr[0]->SetMarkerStyle(2);
    gr[0]->SetMarkerColor(1);
    gr[1]->SetMarkerStyle(3);
    gr[1]->SetMarkerColor(2);
    gr[2]->SetMarkerStyle(4);
    gr[2]->SetMarkerColor(6);
    gr[3]->SetMarkerStyle(5);
    gr[3]->SetMarkerColor(8);
    gr[4]->SetMarkerStyle(25);
    gr[4]->SetMarkerColor(9);
    gr[5]->SetMarkerStyle(26);
    gr[5]->SetMarkerColor(36);
    
    TMultiGraph *mg = new TMultiGraph();
    for(i=0;i<6;i++)
        mg->Add(gr[i]);
    
    mg->SetTitle("IV Curves - Forward bias");
    mg->GetXaxis()->SetTitle("Voltage [V]");
    mg->GetYaxis()->SetTitle("Current [mA]");
    mg->Draw("AP");
}
