// a very quick script to plot some sample distributions from bunch_distributions_2018.root. the fills are
// basically randomly selected.

{
  TFile *f = new TFile("bunch_distributions_2018.root");
  const char *histo_names[6] = {"bx_6621", "bx_6737", "bx_6912",
				"bx_7037", "bx_7139", "bx_7328"};
  TCanvas *c1 = new TCanvas("c1", "c1", 1200, 800);
  c1->Divide(3,2);
  gStyle->SetOptStat(0);
  for (int i=0; i<6; ++i) {
    c1->cd(i+1);
    TH1D *h = (TH1D*)f->Get(histo_names[i]);
    h->Draw();
  }
  c1->Print("sample_bunch_distributions_2018.png");
}
