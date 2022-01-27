
#include "SortDiego.h"

void makeGraph(string fileName) {

  const double halfPE = 4.7e-3;
  vector<double> vT, vV;
  
  ifstream ifs(fileName.c_str());
  double t, v;
  int count=0;
  //while(ifs.is_open() && !ifs.eof() && count< 1.e+5){
  while(ifs.is_open() && !ifs.eof()){
    count++;
    ifs >> t >> v;
    //if(-v < halfPE) v = 0;
    vT.push_back(t);
    vV.push_back(-v);
  }
  ifs.close();
  TGraphErrors *gr = new TGraphErrors(vT.size(), &vT[0], &vV[0], 0, 0);
  auto nPoints = gr->GetN(); // number of points in your TGraph

  TH1D *h = new TH1D("","",nPoints, vT.at(0), vT.at(nPoints-1));
  for(int i=0; i < nPoints; ++i) {
    double x,y;
    gr->GetPoint(i, x, y);
    h->Fill(x,y); 
  }

  Int_t maxNumPeaks = 15000;
  TSpectrum *s = new TSpectrum(maxNumPeaks);
  //Int_t nfound = s->Search(h,1.e-6,"nobackground noMarkov goff",0.5);
  //Int_t nfound = s->Search(h,1.e-3,"noMarkov goff",0.25);
  Int_t nfound = s->Search(h,2,"nobackground noMarkov goff",0.5);//0.12);
  if(!(nfound < maxNumPeaks)) {cout<<"BREAK execution ==> you need to increase the value of maxNumPeaks"<<endl; exit(0);}
  printf("Found %d candidate peaks to fit   DCR %g Hz\n",nfound, nfound/(3.e-3));
  Double_t *xpeaks;
  xpeaks = s->GetPositionX();

  TH1F *h2 = (TH1F*)h->Clone("h2");
  
  
  TCanvas *c = new TCanvas("c", "canvas", 1000, 500);
  c->cd(1);
  gr->GetXaxis()->SetTitle("Time [s]");
  gr->GetYaxis()->SetTitle("Amplitud [V]");
  gr->SetMarkerStyle(7);
  gr->Draw("apl");
  h->SetLineColor(2);
  h->SetMarkerColor(2);
  //h->Draw("same hist");
  vector<double> peakT, peakV, deltaT, deltaV;
  TLine* line[nfound];
  for (Int_t p=0;p<nfound;p++) {
    Double_t xp = xpeaks[p];
    Int_t bin = h->GetXaxis()->FindBin(xp);
    Double_t yp = h->GetBinContent(bin);
    line[p] = new TLine(xp, 0.,xp,2*halfPE);
    line[p]->SetLineColor(4);
    line[p]->SetLineWidth(1);
    line[p]->SetLineStyle(kDashed);
    line[p]->Draw("same");

    peakT.push_back(xp);
    peakV.push_back(yp);
    // cout<<p<<"  "<<xp<<"  "<<yp<<endl;  
  }
  //cout<<"================================"<<endl;
  c->Update();
  c->Modified();
  //c->WaitPrimitive();


  Sort(peakT, peakV);
  //for(int i=0; i<peakT.size(); i++)
  //  cout<<i<<"  T="<<peakT.at(i)<<"  V="<<peakV.at(i)<<endl;
  TH1D *h_intertime = new TH1D("","",1e+2, 0, 1.e-4);
  for(int i=0; i<peakT.size()-1; i++) {
    double interT = peakT.at(i+1) - peakT.at(i);
    deltaT.push_back(interT);
    deltaV.push_back(peakV.at(i+1)/(2*halfPE));
    h_intertime->Fill(interT);
  }

  TGraphErrors *gT = new TGraphErrors(deltaT.size(), &deltaT[0], &deltaV[0], 0, 0);
  TCanvas *c1 = new TCanvas("c1", "canvas", 400, 600);
  c1->Divide(1,2);
  c1->cd(1);
  gT->GetXaxis()->SetTitle("Delay Time [s]");
  gT->GetYaxis()->SetTitle("Amplitud [p.e.]");
  gT->SetMarkerStyle(3);
  gT->Draw("ap");

  c1->cd(2);
  h_intertime->Draw();

  
  c1->Update();
  c1->Modified();
  //c1->WaitPrimitive();
  
  
  
  
}

void analisis() {
  
  //string fileName3 = "test10kSa_or_8_ns.txt";
  //string fileName3 = "test20kSa_or_3_2_ns.txt";
  //string fileName3 = "very_dark.txt";
  //string fileName3 = "test100kSa_or_0_8_ns.txt";
  //string fileName3 = "waveform_hmmts.txt";
  string fileName3 = "/Users/ejimenez/Desktop/SiPM/Ficheros/DCR/test10kSa_or_8_ns.txt";
  makeGraph(fileName3);
  
  
 
}
