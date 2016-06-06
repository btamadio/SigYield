#!/usr/bin/env python
import argparse,ROOT,os,glob,sys
from pointDict import pointDict
from array import *
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasStyle.C')
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasLabels.C')
ROOT.SetAtlasStyle()
parser = argparse.ArgumentParser(add_help=False, description='Print DIDs')
parser.add_argument('input')
parser.add_argument('output')
args = parser.parse_args()
fileList = glob.glob(args.input+'*')
#dictionaries from dsid -> mj
xVals = range(600,810,10)
yVals = {}
dsidList = [403558,403561,403563,403571,403574,403577,403587,403591,403595,403608,403610,403611,403613,403614]
#dsidList = [403560,403563,403571,403574,403577,403587,403591,403595,403608,403610,403611,403613,403614]
colorList = [ROOT.kRed,ROOT.kBlue,ROOT.kViolet,ROOT.kCyan,ROOT.kOrange,ROOT.kGreen,ROOT.kGray,ROOT.kBlack,ROOT.kYellow]
#colorList = [ROOT.kRed,ROOT.kRed,ROOT.kRed,ROOT.kBlue,ROOT.kBlue,ROOT.kViolet,ROOT.kViolet,ROOT.kViolet]
#widthList = [1,2,4,2,4,1,2,4]
keyList = []

for fi in fileList:
    f = ROOT.TFile.Open(fi)
    if not f:
        print 'File not found',f
        sys.exit(1)
    h = f.Get('h_MJ')
    if not h:
        print 'MJ hist not found',f
        sys.exit(1)
    dsid = int( fi.split('.')[0].split('_')[1] )
    keyList.append(dsid)
    yVals[dsid]=[]
    for xVal in xVals:
        yVals[dsid].append(h.Integral(h.FindBin(xVal),h.FindBin(13000)))

outFile = ROOT.TFile.Open(args.output,'RECREATE')
graphs = {}
c = ROOT.TCanvas('c','c',800,600)
leg = ROOT.TLegend(0.55,0.5,0.8,0.9)
leg.SetBorderSize(0)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.SetTextSize(0.03)

mg = ROOT.TMultiGraph()

i = 0
isRPV6 = False
for key in sorted(keyList):
    if pointDict[key][1] == 0:
        isRPV6 = True
    c.cd()
    if key in dsidList:
        graphs[key] = ROOT.TGraph(len(xVals),array('d',xVals),array('d',yVals[key]))
        graphs[key].SetName('graph_'+str(key))
        graphs[key].SetLineColor(colorList[i])
        graphs[key].SetLineWidth(4)
        i+=1
        mg.Add(graphs[key])
        legLabel = 'm_{#tilde{g}} = '+str(pointDict[key][0])+' GeV'
        if not isRPV6:
            legLabel += ', m_{#tilde{#chi}_{1}^{0}} = '+str(pointDict[key][1])+'GeV'
        leg.AddEntry(graphs[key],legLabel,'l')

mg.Draw('AL')
mg.SetMaximum(mg.GetHistogram().GetMaximum()*1.5)
mg.GetXaxis().SetTitle('M_{J}^{#Sigma} cut')
mg.GetYaxis().SetTitle('signal yield')
mg.GetXaxis().SetLimits(590,810)

leg.Draw()
ROOT.ATLASLabel(0.25,0.85,'Internal')
lumiLatex = ROOT.TLatex()
njetLat = ROOT.TLatex()
lumiLatex.DrawLatexNDC(0.25,0.75,'#int L dt = 6.0 fb^{-1}')
njetLat.DrawLatexNDC(0.25,0.65,'n_{fatjet} #geq 5')
