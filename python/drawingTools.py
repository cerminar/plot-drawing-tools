# %load python/drawingTools.py

from __future__ import absolute_import
from __future__ import print_function
import ROOT
import math
import uuid
import pandas as pd
import six
from six.moves import range
import array
import pprint
import os

# some useful globals, mainly to deal with ROOT idiosyncrasies
c_idx = 0
p_idx = 0
colors = [1, 632-4, 416+1, 600-3, 616+1, 432-3]
colors.extend(list(range(1, 12)))


marker_styles = [8, 21, 22, 23, 33, 33, 33, 33, 33, 33, 33, 33]
stuff = []
f_idx = 0

ROOT.gStyle.SetOptTitle(False)
ROOT.gStyle.SetPadBottomMargin(0.13)
ROOT.gStyle.SetPadLeftMargin(0.13)
ROOT.gStyle.SetPadRightMargin(0.13)
ROOT.gStyle.SetOptStat(False)
# ROOT.gStyle.SetPalette()
# ROOT.gStyle.SetCanvasBorderMode(0)
# ROOT.gStyle.SetCanvasColor(0)


# def DrawPrelimLabel(canvas):
#     canvas.cd()
#     tex = ROOT.TLatex()
#     global stuff
#     stuff.append(tex)
#     tex.SetTextSize(0.03)
#     tex.DrawLatexNDC(0.13,0.91,"#scale[1.5]{CMS} #scale[1.]{Phase-2 Simulation}")
#     tex.DrawLatexNDC(0.49,0.91,"14TeV, 7.5#times10^{34}cm^{-2}s^{-1}, 200 PU")

#     tex.Draw("same");
#     return

def SaveCanvas(canvas, name):
    canvas.cd()
    canvas.SaveAs(name+'.pdf')


# void SaveCanvas(TCanvas* c, TString PlotName = "myPlotName")
# {
#   c->cd();
#   c->SaveAs(PlotName + ".pdf");
#   c->SaveAs(PlotName + ".root");

#   return;
# }

def getText(text, ndc_x, ndc_y):
    global stuff
    rtext = ROOT.TLatex(ndc_x, ndc_y, text)
    stuff.append(rtext)
    rtext.SetNDC(True)
    # rtext.SetTextFont(40)
    rtext.SetTextSize(0.03)
    return rtext


def getLegend(x1=0.7, y1=0.71, x2=0.95, y2=0.85):
    global stuff
    legend = ROOT.TLegend(x1, y1, x2, y2)
    stuff.append(legend)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)
    legend.SetTextSize(0.03)
    return legend


def newCanvas(name=None, title=None, height=600, width=800, xdiv=0, ydiv=0, form=4):
    global c_idx
    if name is None:
        name = 'c_{}'.format(uuid.uuid4().hex[:6])
        c_idx += 1
    if title is None:
        title = name
    # print name, title, width, height
    canvas = ROOT.TCanvas(name, title, width, height)
    if(xdiv*ydiv != 0):
        canvas.Divide(xdiv, ydiv)
    global stuff
    stuff.append(canvas)
    return canvas


def drawAndProfileX(plot2d, miny=None, maxy=None, do_profile=True, options='', text=None):
    global p_idx
    if miny and maxy:
        plot2d.GetYaxis().SetRangeUser(miny, maxy)
    c = newCanvas()
    c.SetGrid(1, 1)
    c.cd()
    plot2d.Draw(options)
    ROOT.gPad.SetGrid(1, 1)
    ROOT.gStyle.SetGridColor(15)

    if do_profile:
        profname = plot2d.GetName()+'_prof_'+str(p_idx)
        p_idx += 1
        firstbin = 1
        lastbin = -1
        prof = plot2d.ProfileX(profname, firstbin, lastbin, 's')
        prof.SetMarkerColor(2)
        prof.SetLineColor(2)
        prof.Draw('same')

    if text:
        rtext = getText(text, 0.15, 0.85)
        rtext.Draw('same')

    c.Draw()


class ColorPalette(object):
    def __init__(self):
        self.color_base = [
            ROOT.kBlue+4,
            ROOT.kAzure+1,
            ROOT.kViolet+5,
            ROOT.kViolet,
            ROOT.kPink-9,
            ROOT.kRed-4,
            ROOT.kOrange+1,
            ROOT.kGreen+1,
            ROOT.kYellow-3]

    def __getitem__(self, idx):
        color = 0
        if idx < len(self.color_base):
            color = self.color_base[idx]
        else:
            mod = int(idx / len(self.color_base))
            sign = 1
            if mod % 2:
                sign = -1
            index = idx-mod*len(self.color_base)
            # print (f'mod: {mod}, index: {index}, sign: color: {self.color_base[index]+sign*mod*5}')
            color = self.color_base[index]+sign*10
        # print (f'get color: {color} for idx: {idx}')
        return color


class DrawConfig(object):
    def __init__(self):
        self.do_stats = False
        self.marker_size = 0.5
        self.marker_styles = [id for id in range(20, 50)]

#         self.canvas_sizes = (800, 600)
        self.canvas_sizes = (600, 600)
        # SetMargin (Float_t left, Float_t right, Float_t bottom, Float_t top)
#         self.canvas_margins = (0.13, 0.3, 0.13, 0.1)
        self.canvas_margins = (0.13, 0.13, 0.13, 0.1)
        self.canvas_margins_div = (0.13, 0.13, 0.13, 0.1)
        self.legend_position = (0.6, 0.7)
        self.legend_size = (0.26, 0.1)
        self.additional_text = []
        self.additional_text_size = 0.03

    @property
    def colors(self):
        return ColorPalette()


tdr_config = DrawConfig()
tdr_config.additional_text.append(
    (0.13, 0.91, "scale[1.5]{CMS} scale[1.]{Phase-2 Simulation}"))
tdr_config.additional_text.append(
    (0.69, 0.91, "14TeV, 200 PU"))

rleg_config = DrawConfig()
rleg_config.canvas_sizes = (800, 600)
rleg_config.canvas_margins = (0.13, 0.3, 0.13, 0.1)
rleg_config.legend_position = (0.7, 0.71)
rleg_config.legend_size = (0.25, 0.14)


class RatioPlot(object):
    def __init__(self, id_num, h_num, id_den, h_den):
        self.id_num = id_num
        self.id_den = id_den
        if 'TH' in h_num.ClassName():
            self.histo = h_num.Clone()
            self.histo.Divide(h_den)
        elif 'TGraph' in h_num.ClassName():
            if h_num.GetN() != h_den.GetN():
                raise ValueError(f'[RatioPlot] num and den {h_num.ClassName()} objs have different # of points: ({h_num.GetN() } and {h_den.GetN()} resp.)')
            npoints = h_num.GetN()
            x_den_buf = h_den.GetX()
            x_den_buf.reshape((npoints,))
            x_den = array.array('d', x_den_buf)
            x_num_buf = h_den.GetX()
            x_num_buf.reshape((npoints,))
            x_num = array.array('d', x_num_buf)
            y_den_buf = h_den.GetY()
            y_den_buf.reshape((npoints,))
            y_den = array.array('d', y_den_buf)
            y_num_buf = h_num.GetY()
            y_num_buf.reshape((npoints,))
            y_num = array.array('d', y_num_buf)
            y_ratio = [1.]*npoints
            for id in range(0, npoints):
                if x_num[id] != x_den[id]:
                    raise ValueError(f'[RatioPlot] num and den {h_num.ClassName()} objs have diff. ascissa {x_num[id]} and {x_den[id]} for point {id}')
                if y_den[id] == 0:
                    if y_num[id] == 0:
                        y_ratio[id] = 1
                    else:
                        y_ratio[id] = 99999
                else:
                    y_ratio[id] = y_num[id]/y_den[id]
                # print(f'{id}: y_num: {y_num[id]} y_den: {y_den[id]}')

            self.histo = ROOT.TGraph(npoints, x_num, array.array('d', y_ratio))


class DrawMachine(object):
    def __init__(self, config):
        global stuff
        self.config = config
        self.histos = []
        stuff.append(self.histos)
        self.labels = []
        self.overlay = True
        self.canvas = None
        self.legend = None
        self.ratio_histos = []
        return

    def addHistos(self, histograms, labels):
        for hidx, hist in enumerate(histograms):
            histo_class = hist.ClassName()
            if 'TH2' in histo_class or 'TH3' in histo_class:
                self.overlay = False

            # clone the histo
            d_hist = hist.Clone(uuid.uuid4().hex[:6])
#             if 'TGraph' in histo_class:
#                 d_hist.SetTitle(';'+';'.join(hist.GetTitle().split(';')[1:]))
#             else:
            d_hist.SetTitle(';{};{}'.format(hist.GetXaxis().GetTitle(), hist.GetYaxis().GetTitle()))
            # drop the title
            #             d_hist.SetTitle("")
            self.histos.append(d_hist)
            self.labels.append(labels[hidx])
        return

    def drawAdditionalText(self):
        tex = ROOT.TLatex()
        global stuff
        stuff.append(tex)
        tex.SetTextSize(self.config.additional_text_size)
        for txt in self.config.additional_text:
            tex.DrawLatexNDC(txt[0], txt[1], txt[2])
        tex.Draw("same")

    def formatHisto(self, hidx, hist, options=''):
        histo_class = hist.ClassName()
        hist.UseCurrentStyle()
        # print (f'format histo of class {histo_class}')
        if 'TGraph' in histo_class:
            hist.SetMarkerSize(self.config.marker_size)
            hist.SetMarkerStyle(self.config.marker_styles[hidx])
            if self.overlay:
                hist.SetMarkerColor(self.config.colors[hidx])
                hist.SetLineColor(self.config.colors[hidx])
        elif 'TH1' in histo_class:
            hist.SetLineColor(self.config.colors[hidx])
            if 'hist' not in options:
                hist.SetMarkerSize(self.config.marker_size)
                hist.SetMarkerStyle(self.config.marker_styles[hidx])
                hist.SetMarkerColor(self.config.colors[hidx])
        else:
            hist.SetStats(self.config.do_stats)
            if self.overlay:
                hist.SetLineColor(self.config.colors[hidx])

    def formatHistos(self, options=''):
        for hidx, hist in enumerate(self.histos):
            self.formatHisto(hidx, hist, options)

    def formatRatioHistos(self, options=''):
        for hist in self.ratio_histos:
            self.formatHisto(hist.id_num, hist.histo, options)

    def createCanvas(self, do_ratio=False):
        if self.canvas is not None:
            return

        xdiv = 0
        ydiv = 0

        c_width, c_height = self.config.canvas_sizes

        if not self.overlay:
            xdiv = 2
            ydiv = math.ceil(float(len(self.histos))/2)
            c_width = 1000.
            c_height = 500*ydiv
        else:
            if do_ratio:
                c_height = c_height+200
                xdiv = 1
                ydiv = 2

        self.canvas = newCanvas(name=None,
                                title=None,
                                height=int(c_height),
                                width=int(c_width),
                                xdiv=int(xdiv),
                                ydiv=int(ydiv))
        if self.overlay:
            self.canvas.SetMargin(self.config.canvas_margins[0],
                                  self.config.canvas_margins[1],
                                  self.config.canvas_margins[2],
                                  self.config.canvas_margins[3])
        else:
            self.canvas.SetMargin(self.config.canvas_margins_div[0],
                                  self.config.canvas_margins_div[1],
                                  self.config.canvas_margins_div[2],
                                  self.config.canvas_margins_div[3])
        return

    def createLegend(self):
        if self.legend is not None:
            return
        self.legend = getLegend(self.config.legend_position[0],
                                self.config.legend_position[1],
                                self.config.legend_position[0]+self.config.legend_size[0],
                                self.config.legend_position[1]+self.config.legend_size[1])
        for hidx, hist in enumerate(self.histos):
            histo_class = hist.ClassName()
            if 'TGraph' not in histo_class:
                self.legend.AddEntry(hist, self.labels[hidx], 'lP')
            else:
                self.legend.AddEntry(hist, self.labels[hidx], 'P')

    def addRatioHisto(self, id_num, id_den):
        if len(self.ratio_histos) != 0:
            if id_den not in [rh.id_den for rh in self.ratio_histos]:
                print(f'***Warning: ratio histo can not be added, since id_den: {id_den} != from existing ratio plots!')
                return
        try:
            ratio = RatioPlot(id_num, self.histos[id_num], id_den, self.histos[id_den])
            self.ratio_histos.append(ratio)
        except Exception as inst:
            print(f"***Warning: Ratio plot can not be added: {str(inst)}")

    def draw(self,
             text,
             options='',
             norm=False,
             y_log=False,
             x_log=False,
             y_min=None,
             y_max=None,
             x_min=None,
             x_max=None,
             y_axis_label=None,
             x_axis_label=None,
             v_lines=None,
             h_lines=None,
             do_profile=False,
             do_ratio=False,
             y_min_ratio=0.7,
             y_max_ratio=1.3):

        global p_idx
        global stuff

        if len(self.ratio_histos) == 0:
            do_ratio = False

        self.formatHistos(options)
        self.createCanvas(do_ratio=do_ratio)
        if self.overlay:
            self.createLegend()

        if not do_ratio:
            self.canvas.cd()
        else:
            self.canvas.cd(1)
            ROOT.gPad.SetPad(0, 0.2, 1, 1.0)
            ROOT.gPad.SetBottomMargin(0)
            self.canvas.cd(2)
            ROOT.gPad.SetPad(0, 0, 1, 0.2)
            ROOT.gPad.SetTopMargin(0)
            ROOT.gPad.SetFrameFillColor(0)
            ROOT.gPad.SetFrameBorderMode(0)
            ROOT.gPad.SetFrameFillColor(0)
            ROOT.gPad.SetFrameBorderMode(0)
            ROOT.gPad.SetBottomMargin(0.26)
            self.canvas.cd(1)

        drawn_histos = []
        for hidx, hist in enumerate(self.histos):
            histo_class = hist.ClassName()

            opt = options
            if 'TGraph' in histo_class:
                opt = 'P'+options
            if hidx:
                if self.overlay:
                    opt = 'same,'+opt
            else:
                if 'TGraph' in histo_class:
                    opt = opt+'A'

            if not self.overlay:
                self.canvas.cd(hidx+1)

            d_hist = hist
            if norm:
                d_hist = hist.DrawNormalized(opt, 1.)
            else:
                d_hist.Draw(opt)

            if not self.overlay:
                if text:
                    newtext = '{}: {}'.format(self.labels[hidx], text)
                    rtext = getText(newtext, 0.15, 0.85)
                    rtext.Draw('same')
                    self.drawAdditionalText()

            if do_profile:
                p_idx += 1
                prof = d_hist.ProfileX(d_hist.GetName()+'_prof_'+str(p_idx),
                                       1, -1, 's')
                prof.SetMarkerColor(2)
                prof.SetLineColor(2)
                prof.Draw('same')

            drawn_histos.append(d_hist)

            # we now set the axis properties
            y_min_value = y_min
            y_max_value = y_max

            if y_min is None:
                y_min_value = min([hist.GetBinContent(hist.GetMinimumBin()) for hist in drawn_histos if 'TGraph' not in hist.ClassName() and 'TF1' not in hist.ClassName()] +
                                  [min(hist.GetY()) for hist in drawn_histos if 'TGraph' in hist.ClassName() and 'TF1' not in hist.ClassName()])
            if y_max is None:
                y_max_value = max([hist.GetBinContent(hist.GetMaximumBin()) for hist in drawn_histos if 'TGraph' not in hist.ClassName() and 'TF1' not in hist.ClassName()] +
                                  [max(hist.GetY()) for hist in drawn_histos if 'TGraph' in hist.ClassName() and 'TF1' not in hist.ClassName()])*1.2

            for hist in drawn_histos:
                hist.GetXaxis().SetTitleOffset(1.4)
                hist.GetYaxis().SetRangeUser(y_min_value, y_max_value)
                if y_axis_label:
                    hist.GetYaxis().SetTitle(y_axis_label)
                if x_axis_label:
                    hist.GetXaxis().SetTitle(x_axis_label)
                if x_min is not None and x_max is not None:
                    if 'TGraph' not in hist.ClassName():
                        hist.GetXaxis().SetRangeUser(x_min, x_max)
                    else:
                        hist.GetXaxis().SetLimits(x_min, x_max)

        if self.legend is not None and len(self.histos) > 1:
            self.legend.Draw("same")

        if self.overlay:
            if text:
                rtext = getText(text, 0.15, 0.85)
                rtext.Draw("same")
            self.drawAdditionalText()

        pad_range = list(range(0, 1))
        if not self.overlay:
            pad_range = list(range(1, len(self.histos)+1))
        if do_ratio:
            pad_range = [1]

        self.canvas.Update()
        for pad_id in pad_range:
            self.canvas.cd(pad_id)
            if v_lines:
                for v_line_x in v_lines:
                    aline = ROOT.TLine(v_line_x, ROOT.gPad.GetUymin(), v_line_x,  ROOT.gPad.GetUymax())
                    aline.SetLineStyle(2)
                    aline.Draw("same")
                    stuff.append(aline)
            if h_lines:
                for h_line_y in h_lines:
                    aline = ROOT.TLine(ROOT.gPad.GetUxmin(), h_line_y, ROOT.gPad.GetUxmax(),  h_line_y)
                    aline.SetLineStyle(2)
                    aline.Draw("same")
                    stuff.append(aline)
            if y_log:
                ROOT.gPad.SetLogy()
            if x_log:
                ROOT.gPad.SetLogx()

            ROOT.gPad.Update()

        ROOT.gPad.Draw()

        if do_ratio:
            self.drawRatio(x_min=x_min, x_max=x_max, y_min=y_min_ratio, y_max=y_max_ratio)

        self.canvas.Draw()
        return

    def write(self, name, ext='pdf'):
        self.canvas.SaveAs('{}.{}'.format(name, ext))
        return

    def drawRatio(self, x_min=None, x_max=None, y_min=None, y_max=None):
        #         y_axis_label = '#splitline{{ratio}}{{to {}}}'.format(self.labels[self.ratio_histos[0].id_den])
        y_axis_label = '#splitline{{ratio}}{{scale[0.5]{{to {}}}}}'.format(self.labels[self.ratio_histos[0].id_den])

        self.formatRatioHistos()
        self.canvas.cd(2)
        ROOT.gPad.SetGridy(0)
        for id, ratio in enumerate(self.ratio_histos):
            opt = ''
            if id == 0:
                if 'TGraph' in ratio.histo.ClassName():
                    opt = 'AP'
                ratio.histo.Draw(opt)
            else:
                if 'TGraph' in ratio.histo.ClassName():
                    opt = 'P'
                ratio.histo.Draw(opt+'same')

        # we now set the axis properties
        y_min_value = y_min
        y_max_value = y_max

        drawn_histos = [rat.histo for rat in self.ratio_histos]
        if y_min is None:
            y_min_value = min([hist.GetBinContent(hist.GetMinimumBin()) for hist in drawn_histos if 'TGraph' not in hist.ClassName() and 'TF1' not in hist.ClassName()] +
                              [min(hist.GetY()) for hist in drawn_histos if 'TGraph' in hist.ClassName() and 'TF1' not in hist.ClassName()])*0.8
        if y_max is None:
            y_max_value = max([hist.GetBinContent(hist.GetMaximumBin()) for hist in drawn_histos if 'TGraph' not in hist.ClassName() and 'TF1' not in hist.ClassName()] +
                              [max(hist.GetY()) for hist in drawn_histos if 'TGraph' in hist.ClassName() and 'TF1' not in hist.ClassName()])*1.2

        # print (y_min_value, y_max_value)
        for hist in drawn_histos:
            hist.GetXaxis().SetTitleOffset(5)
            hist.GetYaxis().SetRangeUser(y_min_value, y_max_value)
            if y_axis_label:
                hist.GetYaxis().SetTitle(y_axis_label)
                hist.GetYaxis().SetTitleOffset(2.)
                #             if x_axis_label:
#                 hist.GetXaxis().SetTitle(x_axis_label)
            if x_min is not None and x_max is not None:
                if 'TGraph' not in hist.ClassName():
                    hist.GetXaxis().SetRangeUser(x_min, x_max)
                else:
                    hist.GetXaxis().SetLimits(x_min, x_max)
            hist.GetXaxis().SetTitleSize(20)
            hist.GetYaxis().CenterTitle()
            hist.GetYaxis().SetTitleSize(20)
            hist.GetXaxis().SetLabelSize(20)
            hist.GetYaxis().SetLabelSize(20)
            self.canvas.Update()

        self.canvas.cd(2)
        for h_line_y in [0.9, 1., 1.1]:
            # print (h_line_y)
            print(ROOT.gPad.GetUxmin(), ROOT.gPad.GetUxmax())
            aline = ROOT.TLine(ROOT.gPad.GetUxmin(), h_line_y, ROOT.gPad.GetUxmax(),  h_line_y)
            aline.SetLineStyle(2)
            aline.Draw("same")
            stuff.append(aline)
            self.canvas.Update()

        self.canvas.Draw()


def draw(histograms,
         labels,
         options='',
         norm=False,
         logy=False,
         min_y=None,
         max_y=None,
         min_x=None,
         max_x=None,
         text=None,
         y_axis_label=None,
         x_axis_label=None,
         v_lines=None,
         h_lines=None,
         do_stats=False,
         do_profile=False,
         do_ratio=False,
         do_write=False,
         write_name=None,
         legend_position=None):
    ROOT.gStyle.SetOptStat(False)

    config = rleg_config
    if do_write:
        config = tdr_config
    if do_stats:
        config.do_stats = do_stats
    if legend_position is not None:
        config.legend_position = (legend_position[0],
                                  legend_position[1])
        config.legend_size = (legend_position[2]-legend_position[0],
                              legend_position[3]-legend_position[1])

    dm = DrawMachine(config)
    dm.addHistos(histograms, labels)
    dm.draw(text=text,
            options=options,
            norm=norm,
            y_log=logy,
            y_min=min_y,
            y_max=max_y,
            x_min=min_x,
            x_max=max_x,
            y_axis_label=y_axis_label,
            x_axis_label=x_axis_label,
            v_lines=v_lines,
            h_lines=h_lines,
            do_profile=do_profile,
            # do_ratio=False,
            )
    if do_write:
        dm.write(name=write_name)
    return dm


files = {}
file_keys = {}


class HistoFile():
    def __init__(self, name, label, version=None, type=None, path='../plots/'):
        self.name = name
        self.label = label
        if version:
            version = '_'+version
        else:
            version = ''
        self.histo_filename = os.path.join(path, 'histos_{}{}.root'.format(self.name, version))
        self.histo_file = None
        self.type = type
        self.oldStyle = False

    def __repr__(self):
        return '<{} {}, {}>'.format(self.__class__.__name__, self.histo_filename, self.type)

    def open_file(self):
        if self.histo_file is None:
            self.histo_file = ROOT.TFile(self.histo_filename, 'r')

    def build_file_primitive_index_oldStyle(self):
        # FIXME: this is really hugly
        composite_classes = {('GenParticleHistos', 'h_effNum_'): 'HistoSetEff',
                             ('GenParticleHistos', 'h_effDen_'): 'HistoSetEff',
                             ('TCHistos', 'h_tc_'): 'HistoSetClusters',
                             ('ClusterHistos', 'h_cl2d_'): 'HistoSetClusters',
                             ('Cluster3DHistos', 'h_cl3d_'): 'HistoSetClusters'}
        self.open_file()
        self.histo_file.cd()
        data_list = []
        classtype = 'CalibrationHistos'
        print('--- {}'.format(classtype))
        print('# of plots: {}'.format(len(self.histo_file.GetListOfKeys())))
        # same primitives (tp, tp_sel, gen_sel) applies to several entries
        key_set = set()
        for histo in self.histo_file.GetListOfKeys():
            # print histo.GetName()
            name_parts = histo.GetName().split('_')
            cltype, tp, tp_sel, gen_sel = None, None, None, None
            if len(name_parts) == 4:
                cltype, tp, tp_sel, gen_sel = classtype, name_parts[0], name_parts[1], name_parts[2]
            else:
                # this is a histo in a HistoSet class.. we need to handle this differently
                composite_class = composite_classes[(classtype, '{}_{}_'.format(name_parts[0], name_parts[1]))]
                cltype, tp, tp_sel, gen_sel = composite_class, name_parts[2], name_parts[3], name_parts[4]
            key_set.add((cltype, tp, tp_sel, gen_sel))
        print('# of primitives: {}'.format(len(key_set)))
        for cltype, tp, tp_sel, gen_sel in key_set:
            data_list.append({'classtype': cltype,
                              'tp': tp,
                              'tp_sel': tp_sel,
                              'gen_sel': gen_sel})

        return pd.DataFrame(data_list)

    def build_file_primitive_index(self, debug=True):
        if self.oldStyle:
            print('This is old style')
            return self.build_file_primitive_index_oldStyle()
        # FIXME: this is really hugly
        composite_classes = {('GenParticleHistos', 'h_effNum_'): 'HistoSetEff',
                             ('GenParticleHistos', 'h_effDen_'): 'HistoSetEff',
                             ('TCHistos', 'h_tc_'): 'HistoSetClusters',
                             ('ClusterHistos', 'h_cl2d_'): 'HistoSetClusters',
                             ('Cluster3DHistos', 'h_cl3d_'): 'HistoSetClusters',
                             ('ResoHistos', 'h_reso_'): 'ResoHistos'}

        self.open_file()
        self.histo_file.cd()
        data_list = []
        for key in self.histo_file.GetListOfKeys():
            # first level is classtype
            classtype = key.GetName()
            if(debug):
                print('--- {}'.format(classtype))
            file_dir = self.histo_file.GetDirectory(key.GetName())
            if(debug):
                print('# of plots: {}'.format(len(file_dir.GetListOfKeys())))
            # same primitives (tp, tp_sel, gen_sel) applies to several entries
            key_set = set()
            for histo in file_dir.GetListOfKeys():
                # print(histo.GetName())
                name_parts = histo.GetName().split('_')
                cltype, tp, tp_sel, gen_sel = None, None, None, None
                if len(name_parts) == 3:
                    cltype, tp, tp_sel, gen_sel = classtype, name_parts[0], name_parts[1], None
                elif len(name_parts) == 4:
                    cltype, tp, tp_sel, gen_sel = classtype, name_parts[0], name_parts[1], name_parts[2]
                else:
                    # this is a histo in a HistoSet class.. we need to handle this differently
                    composite_class = composite_classes[(classtype, '{}_{}_'.format(name_parts[0], name_parts[1]))]
                    cltype, tp, tp_sel, gen_sel = composite_class, name_parts[2], name_parts[3], name_parts[4]
                key_set.add((cltype, tp, tp_sel, gen_sel))
            if(debug):
                print('# of primitives: {}'.format(len(key_set)))
            for cltype, tp, tp_sel, gen_sel in key_set:
                data_list.append({'classtype': cltype,
                                  'tp': tp,
                                  'tp_sel': tp_sel,
                                  'gen_sel': gen_sel})

        return pd.DataFrame(data_list)

    def print_file_primitive_index(self):
        primitive_index = self.build_file_primitive_index()
        classtypes = primitive_index.classtype.unique()
        for classtype in classtypes:
            print('- HistoClass: {}'.format(classtype))
            tps = primitive_index[primitive_index.classtype == classtype].tp.unique()
            for tp in tps:
                print('  - TP: {}'.format(tp))
                tp_sels = primitive_index[(primitive_index.classtype == classtype) &
                                          (primitive_index.tp == tp)].tp_sel.unique()
                for tp_sel in tp_sels:
                    gen_sels = primitive_index[(primitive_index.classtype == classtype) &
                                               (primitive_index.tp == tp) &
                                               (primitive_index.tp_sel == tp_sel)].gen_sel.unique()
                    print('    - TP SEL: {} -> GEN SEL: {}'.format(tp_sel, gen_sels))

    def print_primitives(self):
        pp = pprint.PrettyPrinter(indent=4)

        print(self)

        primitive_index = self.build_file_primitive_index(debug=False)
        classtypes = primitive_index.classtype.unique().tolist()
        print('--- HistoClass: ')
        pp.pprint(classtypes)

        tps = primitive_index.tp.unique().tolist()
        tp_select = {}
        for tp in tps:
            tp_select[tp] = primitive_index[primitive_index.tp == tp].tp_sel.unique().tolist()
        # ==== GEN selections ===============================================
        gen_select = {}
        for tp in tps:
            gen_select[tp] = primitive_index[primitive_index.tp == tp].gen_sel.unique().tolist()

        print('--- TPs: ')
        pp.pprint(tps)
        print('--- TP selections:')
        pp.pprint(tp_select)
        print('--- GEN selections:')
        pp.pprint(gen_select)


class HProxy:
    def __init__(self, classtype, tp, tp_sel, gen_sel, root_file):
        self.classtype = classtype
        self.tp = tp
        self.tp_sel = tp_sel
        self.gen_sel = gen_sel
        self.root_file = root_file
        self.instance = None

    def get(self, debug=False):
        if self.instance is None:
            name = '{}_{}_{}'.format(self.tp, self.tp_sel, self.gen_sel)
            if self.gen_sel is None:
                name = '{}_{}'.format(self.tp, self.tp_sel)
            if debug:
                print('-- HProxy:Get: {}'.format(name))
            self.instance = self.classtype(name, self.root_file, debug)
        return self.instance


class HWrapperLazy(object):
    def __init__(self, histo):
        self.histo = histo
        self.data_df = None
        self.filled = False

    def fill_df(self, data):
        self.data_df = data.copy()

    def get(self, debug=False):
        if not self.filled:
            print('Wrapper: {} not filled!'.format(self))
            self.histo.fill(self.data_df)
            self.filled = True
        return self.histo


class HWrapper(object):
    def __init__(self, histo):
        self.histo = histo

    def get(self, debug=False):
        return self.histo


class HPlot:
    def __init__(self, samples, labels_dict):
        self.samples_ = samples
        # reference and complete the label dict
        self.labels_dict = labels_dict
        for sample in samples:
            self.labels_dict[sample.type] = sample.type
        self.labels_dict.update({'PU0': 'PU0', 'PU200': 'PU200'})
        # dataframe used to store the actual data and metadata
        # histos need to be proxies or wrappers (get method to actually retrieve the root histo)
        self.data = pd.DataFrame(columns=['sample', 'pu', 'tp', 'tp_sel', 'gen_sel', 'classtype', 'histo'])

    def create_histo_proxies(self, classtype):
        for sample in self.samples_:
            histo_primtive_index = sample.build_file_primitive_index()
            if histo_primtive_index.empty:
                print('*** ERROR: No histo primitives for sample {}!'.format(sample))
                continue
            class_primitive_index = histo_primtive_index[histo_primtive_index.classtype == str(classtype).split('.')[-1].rstrip('\'>')]
            if class_primitive_index.empty:
                print('*** ERROR: No entry for class: {} in the primtive index!'.format(classtype))
                return

            for index, row in class_primitive_index.iterrows():
                self.data = self.data.append({'sample': sample.type,
                                              'pu': sample.label,
                                              'tp': row.tp,
                                              'tp_sel': row.tp_sel,
                                              'gen_sel': row.gen_sel,
                                              'classtype': classtype,
                                              'histo': HProxy(classtype,
                                                              row.tp,
                                                              row.tp_sel,
                                                              row.gen_sel,
                                                              sample.histo_file)},
                                             ignore_index=True)
            self.data.drop_duplicates(
                subset=['sample', 'pu', 'tp', 'tp_sel', 'gen_sel', 'classtype'],
                inplace=True,
                keep='last')

    def tps(self):
        return self.data.tp.unique().tolist()

    def get_histo(self,
                  classtype,
                  sample=None,
                  pu=None,
                  tp=None,
                  tp_sel=None,
                  gen_sel=None,
                  debug=False):
        histo = None
        labels = []
        text = ''

        query = '(pu == @pu) & (tp == @tp) & (tp_sel == @tp_sel) & (classtype == @classtype)'
        rank_criteria = [('pu', pu), ('tp', tp), ('tp_sel', tp_sel)]
        if gen_sel is not None:
            query += ' & (gen_sel == @gen_sel)'
            rank_criteria.append(('gen_sel', gen_sel))
        else:
            query += ' & (gen_sel.isnull())'
        if sample is not None:
            query += '& (sample == @sample)'
            rank_criteria = [('sample', sample)] + rank_criteria
        # we want to preserve the order as in the input lists
        histo_df = self.data.query(query).copy()

        if histo_df.empty:
            print('No match found for: sample: {} pu: {}, tp: {}, tp_sel: {}, gen_sel: {}, classtype: {}'.format(
                sample, pu, tp, tp_sel, gen_sel, classtype))
            return None, None, None

        rank_list = []
        for (crit_name, crit) in rank_criteria:
            sort_list = dict(zip(crit, range(len(crit))))
            histo_df[crit_name+'_rank'] = histo_df[crit_name].map(sort_list)
            rank_list.append(crit_name+'_rank')

        histo_df.sort_values(rank_list,
                             ascending=[True]*len(rank_list),
                             inplace=True)

        for br in rank_list:
            histo_df.drop(br, axis=1, inplace=True)

        if debug:
            print(histo_df)

        field_counts = histo_df.apply(lambda x: len(x.unique()))
        label_fields = []
        text_fields = []
        # print field_counts
        for field in six.iteritems(field_counts):
            if(field[1] > 1 and field[0] != 'histo'):
                label_fields.append(field[0])
            if(field[1] == 1 and field[0] != 'histo' and field[0] != 'classtype' and field[0] != 'sample'):
                if(gen_sel is None and field[0] == 'gen_sel'):
                    continue
                text_fields.append(field[0])
#         print 'label fields: {}'.format(label_fields)
#         print 'text fields: {}'.format(text_fields)

        for item in histo_df[label_fields].iterrows():
            # print (item)
            labels.append(', '.join([self.labels_dict[tx] for tx in item[1].values if self.labels_dict[tx] != '']))

        # print labels
        text = ', '.join(
            [self.labels_dict[fl] for fl in histo_df[text_fields].iloc[0].values
                if fl in list(self.labels_dict.keys()) and self.labels_dict[fl] != ''])
        histo = [his.get(debug) for his in histo_df['histo'].values]
        return histo, labels, text
