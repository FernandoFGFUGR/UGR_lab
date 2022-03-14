/*Las dos primera funciones que se encuentran en el código son las encargadas
de buscar el máximo de 1/I(dI/dV) para determinar así el voltaje de rotura.
 
La función máximo busca dicho punto a través del punto discreto de máximo
valor tras realizar la derivada.
 
La función gauss realiza la búsqueda del punto a través de un ajuste gaussino
dentro del rango en el que se estime que se encontrará el valor del voltaje.
Por ello, uno de los parámetros a variar dentro de esta función será el rango
donde se realiza el ajuste. {Cabe la opción de elimnar dicho rango y trabajar
con todos los puntos de la gráfica; esto se evito debido a la inestabilidad
que presentan los resultados tras hacer la derivada al trabajar con valores
discreto}*/

void maximo(vector<vector<double>>& a, vector<vector<double>>& b, vector<double>& m)
{
    int i,j;
    double aux,aux1;
    
    for(i=0;i<a.size();i++)
    {
        aux=0;
        for(j=0;j<a[i].size();j++)
        {
            if(aux<a[i][j])
            {
                aux=a[i][j];
                aux1=b[i][j];
            }
        }
        m.push_back(aux1);
    }
        
    return;
}
    
void gauss(int n, vector<vector<double>>& a, vector<vector<double>>& b, vector<vector<double>>& c, vector<double>& r)
{
    int i;
    double p;
    
    TGraph *gr1[n];
    TF1 *f[n];
    
    for(i=0;i<a.size();i++)
    {
        gr1[i]=new TGraph(a[i].size(), &a[i][0], &c[i][0]);
        f[i]=new TF1("f[i]","gaus(0)",24,30); //24,30 frio
        gr1[i]->Fit("f[i]","R");
        p = f[i]->GetParameter(1);
        r.push_back(p);
    }
    
    return;
}

/*Comienza la macro para ROOT. El código está preparado para poder leer y
almacenar los datos de diversos ficheros que se hayan guardado con un nombre
común y solo difieran en la ID de la board con la que se trabaja.
Se pide al usuario el número de pruebas que corresponde con el número de
ficheros con los que se va a trabajar.
 
Tras leer los ficheros se calcula la derivada de la intensidad y tras la
llamada a las funciones se rellenan los diversos histogramas, uno para cada
función y otro mostrando la diferencia entre los valores encontrados con
cada una de las funciones.
 
Finalmente para comprobar que ninguno de los arrays es defectuoso se declara
un nuevo histograma en el que a través de colores podremos distinguir los
resultado para V_br asociados a cada una de las board*/

void VRotura_V ()
{
    int i,j,n,m,c;
    string cad,cad1,cad2,cad3;
    
    double x,y,z,z0;
    ifstream fich;
    
    vector<double> vI,vV;
    vector<vector<double>> V,I;

    z0=0;
    m=1;
    
    cad1="/Users/ejimenez/Desktop/SiPM/Ficheros/VRotura/FRIO/board";
    cad3="_inverse.txt";
    
    cout << "Introduzca el numero de pruebas: ";
    cin >> n;
    
    for(i=0;i<n;i++)
    {
        cad2=to_string(m);
        cad=cad1+cad2+cad3;
        cout << cad << endl;
        fich.open(cad.c_str());
        
        while(fich.is_open() && !fich.eof())
        {
            fich >> x >> y >> z;
            
            if(z>=z0)
            {
                vI.push_back(y);
                vV.push_back(z);
                z0=z;
            }
            else
            {
                I.push_back(vI);
                V.push_back(vV);
                vI.clear();
                vV.clear();
                vI.push_back(y);
                vV.push_back(z);
                z0=0;
            }
        }
        fich.close();
        m++;
    }
    
    cout << "Numero de bloques: " << V.size() << endl;
    
    double difI,difV,dif;
    vector<double> result1,result2;
    vector<vector<double>> VBR,VBR1;
    
    
    for(i=0;i<V.size();i++)
    {
        for(j=0;j<V[i].size();j++)
        {
            difI=I[i][j+1]-I[i][j];
            difV=V[i][j+1]-V[i][j];
            dif=(1/I[i][j])*(difI/difV);
            if(dif<=30 && dif>-5)
            {
                result1.push_back(dif);
                result2.push_back(V[i][j]);
            }
                
        }
        VBR.push_back(result1);    //Resultados para la derivada
        VBR1.push_back(result2);  //Coord X de los puntos dI/dV almacenados
        result1.clear();
        result2.clear();
    }
    
    TH1F *h1 = new TH1F("Maximo","",40,24,30);
    TH1F *h2 = new TH1F("Gauss","",30,24,30);
    TH1F *h3 = new TH1F("Diferencia","",30,-1,1);
    
    vector<double> max, vR;
            
    maximo(VBR,VBR1,max);
    gauss(V.size(),V,I,VBR,vR);

    for(i=0;i<V.size();i++)
    {
        h1->Fill(max.at(i));
        h2->Fill(vR.at(i));
        
        dif=max.at(i)-vR.at(i);
        h3->Fill(dif);
        
        //cout << i << " " << max.at(i) << " " << vR.at(i) << endl;
    }
    
    m=1;
    TH1F *h4[max.size()/6];

    for(i=0;i<max.size()/6;i++)
    {
        cad1="h"+to_string(m);
        cad2="board"+to_string(m);
        h4[i]=new TH1F(cad1.c_str(),cad2.c_str(),30,26.5,27.5);
        m++;
    }
    
    m=1;
    i=j=0;
    while(j<max.size())
    {
        if(j<6*m)
        {
            h4[i]->Fill(vR.at(j));
            j++;
        }
        else
        {
            h4[i+1]->Fill(vR.at(j));
            i++;
            j++;
            m++;
            //cout << i << " " << j << " " << m << endl;
        }
    }
    
    THStack *hs = new THStack("hs","");
    for(i=0;i<max.size()/6;i++)
        hs->Add(h4[i]);

    TGraph *gr[V.size()],*gr1[V.size()];
    TCanvas *c1,*c2,*c3,*c4,*c5;
    
    c1 = new TCanvas("c1","maximo");
    c1->cd(1);
    h1->GetXaxis()->SetTitle("V_{br} (V)");
    h1->Draw();
    
    c2 = new TCanvas("c2","gauss");
    c2->cd(1);
    h2->GetXaxis()->SetTitle("V_{br} (V)");
    h2->Draw();
    
    c3 = new TCanvas("c3","Diferencia");
    c3->cd(1);
    h3->Draw();
    
    c4 = new TCanvas("c4","Conjunto");
    gStyle->SetPalette(1);
    c4->cd(1);
    hs->Draw("PFC");
    //hs->SetTitle("V_{br} at T_{room}");
    hs->GetXaxis()->SetTitle("V_{br} (V)");
    gPad->BuildLegend(0.21,0.05,0.21,0.05,"");
    
/*Para comprobar posibles fallos en el funcionamiento de los sensores se
pintan (opcionalmente) las curvas IV. Pueden pintarse las curvas asociadas a
cada uno de los arrays de una board, basta con cambiar el número de curva.*/
    
    for(i=0;i<V.size();i++)
    {
        gr[i]=new TGraph(V[i].size(), &V[i][0], &I[i][0]);
        gr1[i]=new TGraph(VBR1[i].size(), &VBR1[i][0], &VBR[i][0]);
    }
        
    c5 = new TCanvas("c5","Curvas IV");
    c5->cd(1);
    
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

    mg->SetTitle("IV Curves - Reverse bias");
    mg->GetXaxis()->SetTitle("Voltage [V]");
    mg->GetYaxis()->SetTitle("Current [mA]"); // "1/I(dI/dV)"
    mg->Draw("AP");
    
}
