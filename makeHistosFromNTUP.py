#!/usr/bin/env python
import ROOT,sys,math
import argparse
from pointDict import pointDict
parser = argparse.ArgumentParser(add_help=False, description='Make histograms')
parser.add_argument('input')
parser.add_argument( '--treeName', dest="treeName", default="nominal", help="Tree Name to run on")
parser.add_argument( '--rescale', dest='rescale',action='store_true',default=False,help='Rescale xsec')
args = parser.parse_args()

f = ROOT.TFile.Open(args.input)
if not f:
    print 'File not found. Exiting.',f
    sys.exit(1)
#print 'file: ',args.input
#print 'tree name: ',args.treeName
t = f.Get('outTree/'+args.treeName)
if not t:
    print 'Tree %s not found. Exiting.' % args.treeName
    sys.exit(1)
mdHistName = ''
dsid = ''
for key in f.GetListOfKeys():
    if 'MetaData' in key.GetName():
        mdHistName = key.GetName()
        dsid = mdHistName.split('_')[2]
        print 'DSID: %s nEntries = %i SumOfWeights = %i' %(dsid,t.GetEntries(),f.Get(mdHistName).GetBinContent(3))
        sys.exit(0)
if not mdHistName:
    print 'MetaData Hist not found. Exiting.'
    sys.exit(1)
    

outFileName = 'hists/output_'+dsid+'_'+args.treeName+'.root'
outFile = ROOT.TFile.Open(outFileName,'RECREATE')
h_cutflow = ROOT.TH1F('h_cutflow','h_cutflow',7,0.5,7.5)
h_cutflow.GetXaxis().SetBinLabel(1,'derivation')
h_cutflow.GetXaxis().SetBinLabel(2,'trigger')
h_cutflow.GetXaxis().SetBinLabel(3,'H_{T} > 1 TeV')
h_cutflow.GetXaxis().SetBinLabel(4,'p_{T}^{lead} > 200 GeV')
h_cutflow.GetXaxis().SetBinLabel(5,'n_{fatjet} #geq 5')
h_cutflow.GetXaxis().SetBinLabel(6,'b-tag')
h_cutflow.GetXaxis().SetBinLabel(7,'M_{J} > 800 GeV')

h_eventCat = ROOT.TH1F('h_eventcat','event categories',18,0.5,18.5)
h_eventCat.GetXaxis().SetBinLabel(1,'= 3 jet, b-veto, total')
h_eventCat.GetXaxis().SetBinLabel(2,'= 3 jet, b-tag, total')
h_eventCat.GetXaxis().SetBinLabel(3,'= 3 jet, b-inc, total')
h_eventCat.GetXaxis().SetBinLabel(4,'= 3 jet, b-veto, 200 < MJ < 600')
h_eventCat.GetXaxis().SetBinLabel(5,'= 3 jet, b-tag, 200 < MJ < 600')
h_eventCat.GetXaxis().SetBinLabel(6,'= 3 jet, b-inc, 200 < MJ < 600')
h_eventCat.GetXaxis().SetBinLabel(7,'= 4 jet, b-veto, total')
h_eventCat.GetXaxis().SetBinLabel(8,'= 4 jet, b-tag, total')
h_eventCat.GetXaxis().SetBinLabel(9,'= 4 jet, b-inc, total')
h_eventCat.GetXaxis().SetBinLabel(10,'= 4 jet, b-veto, 200 < MJ < 600')
h_eventCat.GetXaxis().SetBinLabel(11,'= 4 jet, b-tag, 200 < MJ < 600')
h_eventCat.GetXaxis().SetBinLabel(12,'= 4 jet, b-inc, 200 < MJ < 600')
h_eventCat.GetXaxis().SetBinLabel(13,'#geq 5 jet, b-veto, total')
h_eventCat.GetXaxis().SetBinLabel(14,'#geq 5 jet, b-tag, total')
h_eventCat.GetXaxis().SetBinLabel(15,'#geq 5 jet, b-inc, total')
h_eventCat.GetXaxis().SetBinLabel(16,'#geq 5 jet, b-veto, 200 < MJ < 600')
h_eventCat.GetXaxis().SetBinLabel(17,'#geq 5 jet, b-tag, 200 < MJ < 600')
h_eventCat.GetXaxis().SetBinLabel(18,'#geq 5 jet, b-inc, 200 < MJ < 600')


h_sigYield = ROOT.TH1F('h_sigyield','signal yield',20,0.5,20.5)
h_sigYield.GetXaxis().SetBinLabel(1,'n_{fatjet} #geq 4, b-tag, M_{J}^{#Sigma} > 0.6 TeV')
h_sigYield.GetXaxis().SetBinLabel(2,'n_{fatjet} #geq 4, b-tag, M_{J}^{#Sigma} > 0.65 TeV')
h_sigYield.GetXaxis().SetBinLabel(3,'n_{fatjet} #geq 4, b-tag, M_{J}^{#Sigma} > 0.7 TeV')
h_sigYield.GetXaxis().SetBinLabel(4,'n_{fatjet} #geq 4, b-tag, M_{J}^{#Sigma} > 0.75 TeV')
h_sigYield.GetXaxis().SetBinLabel(5,'n_{fatjet} #geq 4, b-tag, M_{J}^{#Sigma} > 0.8 TeV')

h_sigYield.GetXaxis().SetBinLabel(6,'n_{fatjet} #geq 4, b-inc, M_{J}^{#Sigma} > 0.6 TeV')
h_sigYield.GetXaxis().SetBinLabel(7,'n_{fatjet} #geq 4, b-inc, M_{J}^{#Sigma} > 0.65 TeV')
h_sigYield.GetXaxis().SetBinLabel(8,'n_{fatjet} #geq 4, b-inc, M_{J}^{#Sigma} > 0.7 TeV')
h_sigYield.GetXaxis().SetBinLabel(9,'n_{fatjet} #geq 4, b-inc, M_{J}^{#Sigma} > 0.75 TeV')
h_sigYield.GetXaxis().SetBinLabel(10,'n_{fatjet} #geq 4, b-inc, M_{J}^{#Sigma} > 0.8 TeV') 

h_sigYield.GetXaxis().SetBinLabel(11,'n_{fatjet} #geq 5, b-tag, M_{J}^{#Sigma} > 0.6 TeV')
h_sigYield.GetXaxis().SetBinLabel(12,'n_{fatjet} #geq 5, b-tag, M_{J}^{#Sigma} > 0.65 TeV')
h_sigYield.GetXaxis().SetBinLabel(13,'n_{fatjet} #geq 5, b-tag, M_{J}^{#Sigma} > 0.7 TeV')
h_sigYield.GetXaxis().SetBinLabel(14,'n_{fatjet} #geq 5, b-tag, M_{J}^{#Sigma} > 0.75 TeV')
h_sigYield.GetXaxis().SetBinLabel(15,'n_{fatjet} #geq 5, b-tag, M_{J}^{#Sigma} > 0.8 TeV')

h_sigYield.GetXaxis().SetBinLabel(16,'n_{fatjet} #geq 5, b-inc, M_{J}^{#Sigma} > 0.6 TeV')
h_sigYield.GetXaxis().SetBinLabel(17,'n_{fatjet} #geq 5, b-inc, M_{J}^{#Sigma} > 0.65 TeV')
h_sigYield.GetXaxis().SetBinLabel(18,'n_{fatjet} #geq 5, b-inc, M_{J}^{#Sigma} > 0.7 TeV')
h_sigYield.GetXaxis().SetBinLabel(19,'n_{fatjet} #geq 5, b-inc, M_{J}^{#Sigma} > 0.75 TeV')
h_sigYield.GetXaxis().SetBinLabel(20,'n_{fatjet} #geq 5, b-inc, M_{J}^{#Sigma} > 0.8 TeV') 


h_MJ3 = ROOT.TH1F('h_MJ3','M_{J}^{#Sigma}, n_{fatjet} #geq 3',15,0,1500)
h_MJ = ROOT.TH1F('h_MJ','M_{J}^{#Sigma}',15,0,1500)

trigs = ['HLT_ht850_L1J100','HLT_ht850_L1J75']

htCut = 1000.0
jetPtCut = 50.0
fatJetPtCut = 200.0
jetEtaCut = 2.8
fatJetEtaCut = 2.0
leadJetPtCut = 200.0
fatjetMpTCut = 0.8
lumi = 6.0

denom=0
nEntries = t.GetEntries()
for entry in range(nEntries):
    t.GetEntry(entry)
    denom+=t.weight_jet_SFFix70[0]

for entry in range(nEntries):
    t.GetEntry(entry)
    passTrig = False
    passLeadJet = False
    ht = 0.0
    nBTag = 0
    mj = 0.0
    nJet = 0
    nFatJet = 0
    iCut = 1
    eventCat = 0
    rescale = 1
    if args.rescale:
        xsec = pointDict[int(dsid)][2]
        rescale= xsec/t.weight_xs
    w = t.weight_jet_SFFix70.at(0)*rescale*1E6*lumi*t.weight/denom
    #all events in derivation
    h_cutflow.Fill(iCut,w)
    iCut+=1

    #pass trigger
    for passedTrig in t.passedTriggers:
        for trig in trigs:
            if trig == passedTrig:
                passTrig = True
    if not passTrig:
        continue
    h_cutflow.Fill(iCut,w)
    iCut+=1

    #pass ht and ptlead cuts
    for i in range(t.jet_clean_passLooseBad.size()):
        if t.jet_pt.at(i) > jetPtCut and abs(t.jet_eta.at(i)) < jetEtaCut and t.jet_clean_passLooseBad.at(i) == 1:
            ht+=t.jet_pt.at(i)
            if t.jet_pt.at(i) > leadJetPtCut:
                passLeadJet = True
            if t.jet_isFix70.at(i) == 1:
                nBTag += 1
    if ht < htCut:
        continue
    h_cutflow.Fill(iCut,w)
    iCut+=1
    if not passLeadJet:
        continue
    h_cutflow.Fill(iCut,w)
    iCut+=1

    #calculate MJ and count fat jets
    ptMList = []
    for i in range(t.fatjet_pt.size()):
        if t.fatjet_pt.at(i) > fatJetPtCut and abs(t.fatjet_eta.at(i)) < fatJetEtaCut and t.fatjet_m.at(i)/t.fatjet_pt.at(i) < fatjetMpTCut:
            nFatJet += 1
            ptMList.append( (t.fatjet_pt.at(i),t.fatjet_m.at(i)) )
    ptMList.sort(key=lambda tup: tup[0], reverse = True)
    for mi in ptMList[0:min(4,len(ptMList))]:
        mj += mi[1]
    
    #fill NR yields
    if nFatJet == 3:
        if nBTag == 0:
            h_eventCat.Fill(1,w)
        else:
            h_eventCat.Fill(2,w)
        h_eventCat.Fill(3,w)
        if mj > 200 and mj < 600:
            if nBTag == 0:
                h_eventCat.Fill(4,w)
            else:
                h_eventCat.Fill(5,w)
            h_eventCat.Fill(6,w)
    if nFatJet == 4:
        if nBTag == 0:
            h_eventCat.Fill(7,w)
        else:
            h_eventCat.Fill(8,w)
        h_eventCat.Fill(9,w)
        if mj > 200 and mj < 600:
            if nBTag == 0:
                h_eventCat.Fill(10,w)
            else:
                h_eventCat.Fill(11,w)
            h_eventCat.Fill(12,w)
    if nFatJet >= 5:
        if nBTag == 0:
            h_eventCat.Fill(13,w)
        else:
            h_eventCat.Fill(14,w)
        h_eventCat.Fill(15,w)
        if mj > 200 and mj < 600:
            if nBTag == 0:
                h_eventCat.Fill(16,w)
            else:
                h_eventCat.Fill(17,w)
            h_eventCat.Fill(18,w)
    
    #Fill SR yields
    if nFatJet >= 4:
        if nBTag >= 1:
            if mj > 600:
                h_sigYield.Fill(1,w)
            if mj > 650:
                h_sigYield.Fill(2,w)
            if mj > 700:
                h_sigYield.Fill(3,w)
            if mj > 750:
                h_sigYield.Fill(4,w)
            if mj > 800:
                h_sigYield.Fill(5,w)
        if mj > 600:
            h_sigYield.Fill(6,w)
        if mj > 650:
            h_sigYield.Fill(7,w)
        if mj > 700:
            h_sigYield.Fill(8,w)
        if mj > 750:
            h_sigYield.Fill(9,w)
        if mj > 800:
            h_sigYield.Fill(10,w)
    if nFatJet >= 5:
        if nBTag >= 1:
            if mj > 600:
                h_sigYield.Fill(11,w)
            if mj > 650:
                h_sigYield.Fill(12,w)
            if mj > 700:
                h_sigYield.Fill(13,w)
            if mj > 750:
                h_sigYield.Fill(14,w)
            if mj > 800:
                h_sigYield.Fill(15,w)
        if mj > 600:
            h_sigYield.Fill(16,w)
        if mj > 650:
            h_sigYield.Fill(17,w)
        if mj > 700:
            h_sigYield.Fill(18,w)
        if mj > 750:
            h_sigYield.Fill(19,w)
        if mj > 800:
            h_sigYield.Fill(20,w)

    if nFatJet >= 3 and nBTag >= 1:
        h_MJ3.Fill(mj,w)
    if nFatJet < 5:
        continue
    h_cutflow.Fill(iCut,w)
    iCut+=1
    if nBTag < 1:
        continue
    h_cutflow.Fill(iCut,w)
    iCut+=1
    h_MJ.Fill(mj,w)
    if mj < 800:
        continue
    h_cutflow.Fill(iCut,w)

outFile.Write()
