#!/usr/bin/env python
import argparse,ROOT,os,glob,sys
from pointDict import pointDict
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasStyle.C')
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasLabels.C')
ROOT.SetAtlasStyle()
ROOT.gStyle.SetPaintTextFormat('2.1f')

parser = argparse.ArgumentParser(add_help=False, description='Print DIDs')
parser.add_argument('input')
args = parser.parse_args()
fileList = glob.glob(args.input+'*')
cuts = ['derivation','trigger','pT_lead','HT','n_fatjet_5','btag','MJ_800']
eventCats = ['3jet_bveto_MJlow','3jet_btag_MJlow','4jet_bveto_MJlow','4jet_btag_MJlow','5jet_bveto_MJlow','5jet_btag_MJlow','3jet_bveto_MJhigh','3jet_btag_MJhigh','4jet_bveto_MJhigh','4jet_btag_MJhigh','5jet_bveto_MJhigh','5jet_btag_MJhigh']
catLabels = ['#splitline{200 GeV < M_{J}^{#Sigma} < 600 GeV}{#splitline{n_{fatjet} = 3}{b-veto}}',
'#splitline{200 GeV < M_{J}^{#Sigma} < 600 GeV}{#splitline{n_{fatjet} = 3}{b-tag}}',
'#splitline{200 GeV < M_{J}^{#Sigma} < 600 GeV}{#splitline{n_{fatjet} = 4}{b-veto}}',
'#splitline{200 GeV < M_{J}^{#Sigma} < 600 GeV}{#splitline{n_{fatjet} = 4}{b-tag}}',
'#splitline{200 GeV < M_{J}^{#Sigma} < 600 GeV}{#splitline{n_{fatjet} #geq 5}{b-veto}}',
'#splitline{200 GeV < M_{J}^{#Sigma} < 600 GeV}{#splitline{n_{fatjet} #geq 5}{b-tag}}',
'#splitline{M_{J}^{#Sigma} > 800 GeV}{#splitline{n_{fatjet} = 3}{b-veto}}',
'#splitline{M_{J}^{#Sigma} > 800 GeV}{#splitline{n_{fatjet} = 3}{b-tag}}',
'#splitline{M_{J}^{#Sigma} > 800 GeV}{#splitline{n_{fatjet} = 4}{b-veto}}',
'#splitline{M_{J}^{#Sigma} > 800 GeV}{#splitline{n_{fatjet} = 4}{b-tag}}',
'#splitline{M_{J}^{#Sigma} > 800 GeV}{#splitline{n_{fatjet} #geq 5}{b-veto}}',
'#splitline{M_{J}^{#Sigma} > 800 GeV}{#splitline{n_{fatjet} #geq 5}{b-tag}}']
sigDefs = ['njet_4_mj_6','njet_4_mj_65','njet_4_mj_7','njet_4_mj_75','njet_4_mj_8','njet_5_mj_6','njet_5_mj_65','njet_5_mj_7','njet_5_mj_75','njet_5_mj_8']
sigLabels= ['#splitline{n_{fatjet} #geq 4}{M_{J}^{#Sigma} > 600 GeV}',
'#splitline{n_{fatjet} #geq 4}{M_{J}^{#Sigma} > 650 GeV}',
'#splitline{n_{fatjet} #geq 4}{M_{J}^{#Sigma} > 700 GeV}',
'#splitline{n_{fatjet} #geq 4}{M_{J}^{#Sigma} > 750 GeV}',
'#splitline{n_{fatjet} #geq 4}{M_{J}^{#Sigma} > 800 GeV}',
'#splitline{n_{fatjet} #geq 5}{M_{J}^{#Sigma} > 600 GeV}',
'#splitline{n_{fatjet} #geq 5}{M_{J}^{#Sigma} > 650 GeV}',
'#splitline{n_{fatjet} #geq 5}{M_{J}^{#Sigma} > 700 GeV}',
'#splitline{n_{fatjet} #geq 5}{M_{J}^{#Sigma} > 750 GeV}',
'#splitline{n_{fatjet} #geq 5}{M_{J}^{#Sigma} > 800 GeV}']

catLatex = [ROOT.TLatex() for label in catLabels]
outFile = ROOT.TFile.Open('yield_plots.root','RECREATE')
cutflowList = [ROOT.TH2D('cutflow_'+str(i),cuts[i],21,1050,2100,220,-200,2000) for i in range(len(cuts))]
effList = [ROOT.TH2D('eff_'+str(i),cuts[i]+' efficiency',21,1050,2100,220,-200,2000) for i in range(len(cuts))]
eventCatList = [ROOT.TH2D('eventCat_'+str(i+1),eventCats[i],21,1050,2100,220,-200,2000) for i in range(len(eventCats))]
sigDefList = [ROOT.TH2D('sigdef_'+str(i+1),sigDefs[i],21,1050,2100,220,-200,2000) for i in range(len(sigDefs))]
dsidHist = ROOT.TH2D('dsid','dsid',21,1050,2100,220,-200,2000)
c = [ROOT.TCanvas('c'+str(i),cuts[i],800,600) for i in range(len(cuts))]
c2 = [ROOT.TCanvas('c_2_'+str(i),cuts[i]+' eff.',800,600) for i in range(len(cuts))]
c3 = [ROOT.TCanvas('c_3_'+str(i),eventCats[i],800,600) for i in range(len(eventCats))]
c4 = [ROOT.TCanvas('c_4_'+str(i),sigDefs[i],800,600) for i in range(len(sigDefs))]

lumiLatex = ROOT.TLatex()
for file in fileList:
    f = ROOT.TFile.Open(file)
    if not f:
        print 'File not found',f
        sys.exit(1)
    h = f.Get('h_cutflow')
    hEC = f.Get('h_eventcat')
    hSD = f.Get('h_sigyield')
    if not h or not hEC:
        print 'cutflow hist not found',f
        sys.exit(1)
    dsid = int( file.split('.')[0].split('_')[1] )
    mG = pointDict[dsid][0]
    mX = pointDict[dsid][1]
    dsidHist.Fill(mG,mX,dsid)
    if mX > 10 and dsid != 403105:
        for i in range(len(cuts)):
            cutflowList[i].Fill(mG,mX,h.GetBinContent(i+1))
            if i == 0:
                effList[i].Fill(mG,mX,1)
                effList[i].GetXaxis().SetTitle('m_{#tilde{g}} [GeV]')
                effList[i].GetYaxis().SetTitle('m_{#tilde{#chi}_{1}^{0}} [GeV]')
            else:
                effList[i].Fill(mG,mX,h.GetBinContent(i+1)/h.GetBinContent(i))
            cutflowList[i].GetXaxis().SetTitle('m_{#tilde{g}} [GeV]')
            cutflowList[i].GetYaxis().SetTitle('m_{#tilde{#chi}_{1}^{0}} [GeV]')
        for i in range(len(eventCats)):
            eventCatList[i].Fill(mG,mX,hEC.GetBinContent(i+1))
            eventCatList[i].GetXaxis().SetTitle('m_{#tilde{g}} [GeV]')
            eventCatList[i].GetYaxis().SetTitle('m_{#tilde{#chi}_{1}^{0}} [GeV]')
        for i in range(len(sigDefs)):
            sigDefList[i].Fill(mG,mX,hSD.GetBinContent(i+1)*0.83)
            sigDefList[i].GetXaxis().SetTitle('m_{#tilde{g}} [GeV]')
            sigDefList[i].GetYaxis().SetTitle('m_{#tilde{#chi}_{1}^{0}} [GeV]')
outFile.Write()
j=0
for i in range(len(cutflowList)):
    j+=1
    c[i].cd()
    cutflowList[i].SetMarkerSize(2.2)
    cutflowList[i].Draw('text')
    ROOT.ATLASLabel(0.2,0.85,'Internal')
    lumiLatex.DrawLatexNDC(0.65,0.825,'#int L dt = 6.0 fb^{-1}')
    c[i].SaveAs('/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/SignalYields/Gtt_EventCategories/0'+str(j)+'_'+cuts[i]+'.pdf')

for i in range(len(effList)):
    j+=1
    c2[i].cd()
    effList[i].SetMarkerSize(2.2)
    effList[i].Draw('text')
    ROOT.ATLASLabel(0.2,0.85,'Internal')
    lumiLatex.DrawLatexNDC(0.65,0.825,'#int L dt = 6.0 fb^{-1}')
    if j < 10:
        c2[i].SaveAs('/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/SignalYields/Gtt_EventCategories/0'+str(j)+'_'+cuts[i]+'_efficiency.pdf')
    else:
        c2[i].SaveAs('/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/SignalYields/Gtt_EventCategories/'+str(j)+'_'+cuts[i]+'_efficiency.pdf')    

for i in range(len(eventCatList)):
    j+=1
    c3[i].cd()
    eventCatList[i].SetMarkerSize(2.2)
    eventCatList[i].Draw('text')
    ROOT.ATLASLabel(0.2,0.85,'Internal')
    lumiLatex.DrawLatexNDC(0.65,0.825,'#int L dt = 6.0 fb^{-1}')
    catLatex[i].DrawLatexNDC(0.2,0.75,catLabels[i])
    if j < 10:
        c3[i].SaveAs('/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/SignalYields/Gtt_EventCategories/0'+str(j)+'_'+eventCats[i]+'.pdf')
    else:
        c3[i].SaveAs('/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/SignalYields/Gtt_EventCategories/'+str(j)+'_'+eventCats[i]+'.pdf')

for i in range(len(sigDefList)):
    j+=1
    c4[i].cd()
    sigDefList[i].SetMarkerSize(2.2)
    sigDefList[i].Draw('text')
    ROOT.ATLASLabel(0.2,0.85,'Internal')
    lumiLatex.DrawLatexNDC(0.65,0.825,'#int L dt = 6.0 fb^{-1}')
    catLatex[i].DrawLatexNDC(0.2,0.75,sigLabels[i])
    if j < 10:
        c4[i].SaveAs('/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/SignalYields/Gtt_EventCategories/0'+str(j)+'_'+sigDefs[i]+'.pdf')
    else:
        c4[i].SaveAs('/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/SignalYields/Gtt_EventCategories/'+str(j)+'_'+sigDefs[i]+'.pdf')

