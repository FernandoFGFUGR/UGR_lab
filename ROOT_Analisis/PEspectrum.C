/// \file
/// \ingroup tutorial_spectrum
/// \notebook
/// Illustrates how to find peaks in histograms.
///
/// This script generates a random number of gaussian peaks
/// on top of a linear background.
/// The position of the peaks is found via TSpectrum and injected
/// as initial values of parameters to make a global fit.
/// The background is computed and drawn on top of the original histogram.
///
/// This script can fit "peaks' heights" or "peaks' areas" (comment out
/// or uncomment the line which defines `__PEAKS_C_FIT_AREAS__`).
///
/// To execute this example, do (in ROOT 5 or ROOT 6):
///
/// ~~~{.cpp}
///  root > .x peaks.C  (generate 10 peaks by default)
///  root > .x peaks.C++ (use the compiler)
///  root > .x peaks.C++(30) (generates 30 peaks)
/// ~~~
///
/// To execute only the first part of the script (without fitting)
/// specify a negative value for the number of peaks, eg
///
/// ~~~{.cpp}
///  root > .x peaks.C(-20)
/// ~~~
///
/// \macro_output
/// \macro_image
/// \macro_code
///
/// \author Rene Brun
 
#include "TCanvas.h"
#include "TMath.h"
#include "TH1.h"
#include "TF1.h"
#include "TRandom.h"
#include "TSpectrum.h"
#include "TVirtualFitter.h"

Int_t npeaks = 10;
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

void PEspectrum(Int_t np=10) {
  npeaks = TMath::Abs(np);
  TH1F *h = new TH1F("h","",500,-1.e-9,4.e-9);
  //TH1F *h = new TH1F("h","",500,-1,5);
  //string fileName = "final_histo_charge.txt";
  string fileName = "/Users/ejimenez/Desktop/SiPM/Ficheros/Ganancia/test.txt";
  ifstream ifs(fileName.c_str());
  double vs;
  int count=0;
  if(!ifs.is_open()){
    cout << "Error al abrir el fichero" << endl;
  }
  else{
    while(ifs.is_open() && !ifs.eof()){
    count++;
    ifs >> vs;
    //cout << vs;
    //h->Fill(vs*1.e+9);
    h->Fill(vs);
  }
  }
  ifs.close();

  // Generate n peaks at random
  Double_t par[3*npeaks];
  TCanvas *c1 = new TCanvas("c1","c1",10,10,800,600);
  c1->cd(1);
  h->SetStats(0);
  h->SetLineWidth(2);
  h->SetLineColor(1);
  h->GetYaxis()->SetTitle("Counts");
  h->GetXaxis()->SetTitle("Charge [V #times s]");
  h->Draw();

  TH1F *h2 = (TH1F*)h->Clone("h2");
  // Use TSpectrum to find the peak candidates
  TSpectrum *s = new TSpectrum(2*npeaks);
  Int_t nfound = s->Search(h,2,"nobackground noMarkov",0.015);
  printf("Found %d candidate peaks to fit\n",nfound);
  if (np <0) return;
  // Loop on all found peaks. Eliminate peaks at the background level
  npeaks = 0;
  Double_t *xpeaks;
  xpeaks = s->GetPositionX();
  for (Int_t p=0;p<nfound;p++) {
    Double_t xp = xpeaks[p];
    Int_t bin = h->GetXaxis()->FindBin(xp);
    Double_t yp = h->GetBinContent(bin);
    par[3*npeaks] = yp; // "norm"
    par[3*npeaks+1] = xp; // "mean"
    par[3*npeaks+2] = 1.e-11; // "sigma"
    //par[3*npeaks+2] = 1.e0; // "sigma"

    cout<<"peak "<<p<<" norm: "<<yp<<"  mean: "<<xp<<" sigma: "<<par[3*npeaks+2]<<endl;
    npeaks++;
  }
  printf("Found %d useful peaks to fit\n",npeaks);
  printf("Now fitting: Be patient\n");
  TF1 *fit = new TF1("fit",fpeaks,-1.e-9,5.e-9,3*npeaks);
  //TF1 *fit = new TF1("fit",fpeaks,-1.,5.,3*npeaks);
  fit->SetParameters(par);
  fit->SetNpx(1000);
  for (Int_t p=0;p<nfound;p++) {
    cout<<"means are: par"<<3*p+1<<"  :"<<par[3*p+1]<<endl;
    fit->FixParameter(3*p+1,par[3*p+1]);
  }
  h2->Fit("fit", "QR0");
  fit->SetLineColor(4);
  fit->Draw("same");
  double Rscope = 50.;//Ohms
  double e = 1.6e-19;//Coulombs
  double Gain = (par[7] - par[4])/(Rscope*e);
  
  TLatex *ganancia = new TLatex();
  ganancia->SetTextSize(0.03);
  char num[60];
  sprintf(num,"Gain = %2.2e",Gain); 
  ganancia->DrawLatex(par[4]*1.3, par[3], num);  

}
