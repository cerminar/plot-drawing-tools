# %load drawingTools.py
import ROOT
import math
import uuid
import pandas as pd

# some useful globals, mainly to deal with ROOT idiosyncrasies
c_idx = 0
p_idx = 0
colors = range(1, 12)
colors = [1, 632-4, 416+1, 600-3, 616+1, 432-3]


marker_styles = [8, 21, 22, 23, 33]
stuff = []
f_idx = 0

ROOT.gStyle.SetOptTitle(False)
ROOT.gStyle.SetPadBottomMargin(0.13)
ROOT.gStyle.SetPadLeftMargin(0.13)
ROOT.gStyle.SetPadRightMargin(0.13)
ROOT.gStyle.SetOptStat(False)

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

class DrawConfig(object):
    def __init__(self):
        self.do_stats = False
        self.marker_size = 0.5
        self.marker_styles = [8, 21, 22, 23, 33]
        self.colors = [1, 632-4, 416+1, 600-3, 616+1, 432-3]
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
        return

tdr_config = DrawConfig()
tdr_config.additional_text.append((0.13,0.91,"#scale[1.5]{CMS} #scale[1.]{Phase-2 Simulation}"))
tdr_config.additional_text.append((0.69,0.91,"14TeV, 200 PU"))

rleg_config = DrawConfig()
rleg_config.canvas_sizes = (800, 600)
rleg_config.canvas_margins = (0.13, 0.3, 0.13, 0.1)
rleg_config.legend_position = (0.7, 0.71)
rleg_config.legend_size = (0.25, 0.14)

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
        return

    def addHistos(self, histograms, labels):
        for hidx,hist in enumerate(histograms):
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
        tex.Draw("same");


    def formatHistos(self):
        for hidx,hist in enumerate(self.histos):
            histo_class = hist.ClassName()
            hist.UseCurrentStyle()

            if 'TGraph' in histo_class:
                hist.SetMarkerSize(self.config.marker_size)
                hist.SetMarkerStyle(self.config.marker_styles[hidx])
                if self.overlay:
                    hist.SetMarkerColor(colors[hidx])
                    hist.SetLineColor(self.config.colors[hidx])

            else:
                hist.SetStats(self.config.do_stats)
                if self.overlay:
                    hist.SetLineColor(self.config.colors[hidx])
        return

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
        for hidx,hist in enumerate(self.histos):
            histo_class = hist.ClassName()
            if 'TGraph' not in histo_class:
                self.legend.AddEntry(hist, self.labels[hidx], 'l')
            else:
                self.legend.AddEntry(hist, self.labels[hidx], 'P')

        return


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
             do_profile=False):

        global p_idx
        global stuff

        self.formatHistos()
        self.createCanvas()
        if self.overlay:
            self.createLegend()

        self.canvas.cd()

        drawn_histos = []
        for hidx, hist in enumerate(self.histos):
            histo_class = hist.ClassName()

            opt = options
            if 'TGraph' in histo_class:
                opt = 'P'+options
            if hidx:
                opt = 'same,'+opt
            else:
                if 'TGraph' in histo_class:
                    opt = opt+'A'

            if not self.overlay:
                self.canvas.cd(hidx+1)
                if text:
                    newtext = '{}: {}'.format(self.labels[hidx], text)
                    rtext = getText(newtext, 0.15, 0.85)
                    rtext.Draw('same')
                    self.drawAdditionalText()

            d_hist = hist
            if norm:
                d_hist = hist.DrawNormalized(opt, 1.)
            else:
                d_hist.Draw(opt)

            if do_profile:
                profname = d_hist.GetName()+'_prof_'+str(p_idx)
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
                y_min_value = min([hist.GetBinContent(hist.GetMinimumBin()) for hist in drawn_histos if 'TGraph' not in hist.ClassName()] +
                                  [min(hist.GetY()) for hist in drawn_histos if 'TGraph' in hist.ClassName()])
            if y_max is None:
                y_max_value = max([hist.GetBinContent(hist.GetMaximumBin()) for hist in drawn_histos if 'TGraph' not in hist.ClassName()] +
                                  [max(hist.GetY()) for hist in drawn_histos if 'TGraph' in hist.ClassName()])*1.2

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

        pad_range = range(0, 1)
        if not self.overlay:
            pad_range = range(1, len(self.histos)+1)

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

        self.canvas.Draw()
        return

    def write(self, name, ext='pdf'):
        self.canvas.SaveAs('{}.{}'.format(name, ext))
        return


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
            do_profile=False,
            # do_ratio=False,
           )
    if do_write:
        dm.write(name=write_name)
    return dm


files = {}
file_keys = {}


class RootFile:
    def __init__(self, file_name):
        global file
        self.file_name = file_name
        if self.file_name not in files.keys():
            print 'get file: {}'.format(self.file_name)
            files[self.file_name] = ROOT.TFile(self.file_name)
        self._file = files[self.file_name]
        self._file_keys = None

    def cd(self):
        self._file.cd()

    def GetListOfKeys(self):
        global file_keys
        if self.file_name not in file_keys.keys():
            print 'get list'
            file_keys[self.file_name] = self._file.GetListOfKeys()
        self._file_keys = file_keys[self.file_name]
        return self._file_keys


class Sample():
    def __init__(self, name, label, version=None, type=None):
        self.name = name
        self.label = label
        if version:
            version = '_'+version
        else:
            version = ''
        self.histo_filename = '../plots1/histos_{}{}.root'.format(self.name, version)
        self.histo_file = None
        self.type = type

    def __repr__(self):
        return '<{} {}, {}>'.format(self.__class__.__name__, self.histo_filename, self.type)

    def open_file(self):
        self.histo_file = ROOT.TFile(self.histo_filename, 'r')

# sample_names = ['ele_flat2to100_PU0',
#                 'ele_flat2to100_PU200',
#                 'photonPt35_PU0',
#                 'photonPt35_PU200']


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
                print '-- HProxy:Get: {}'.format(name)
            self.instance = self.classtype(name, self.root_file, debug)
        return self.instance


class HPlot:
    def __init__(self, samples, tp_sets, tp_selections, gen_selections):
        self.tp_sets = tp_sets
        # self.tp_selections = tp_selections
        # self.gen_selections = gen_selections
        self.pus = []
        self.labels_dict = {}

        for sample in samples:
            self.pus.append(sample.label)
            self.labels_dict[sample.type] = sample.type

        self.data = pd.DataFrame(columns=['sample', 'pu', 'tp', 'tp_sel', 'gen_sel', 'classtype', 'histo'])

        self.labels_dict.update(tp_sets)
        self.labels_dict.update(tp_selections)
        self.labels_dict.update(gen_selections)
        self.labels_dict.update({'PU0': 'PU0', 'PU200': 'PU200'})

    def cache_histo(self,
                    classtype,
                    samples,
                    pus,
                    tps,
                    tp_sels,
                    gen_sels,
                    debug=False):
        if gen_sels is None:
            gen_sels = [None]

        for sample in samples:
            if debug:
                print sample
            for tp in tps:
                for tp_sel in tp_sels:
                    for gen_sel in gen_sels:
                        if debug:
                            print sample, tp, tp_sel, gen_sel
                        self.data = self.data.append({'sample': sample.type,
                                                      'pu': sample.label,
                                                      'tp': tp,
                                                      'tp_sel': tp_sel,
                                                      'gen_sel': gen_sel,
                                                      'classtype': classtype,
                                                      'histo': HProxy(classtype, tp, tp_sel, gen_sel, sample.histo_file)},
                                                     ignore_index=True)

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
        if gen_sel is not None:
            query += ' & (gen_sel == @gen_sel)'
        else:
            query += ' & (gen_sel.isnull())'
        if sample is not None:
            query += '& (sample == @sample)'

        histo_df = self.data.query(query)

        if histo_df.empty:
            print 'No match found for: pu: {}, tp: {}, tp_sel: {}, gen_sel: {}, classtype: {}'.format(pu, tp, tp_sel, gen_sel, classtype)
            return None, None, None
        if debug:
            print histo_df

        field_counts = histo_df.apply(lambda x: len(x.unique()))
        label_fields = []
        text_fields = []
        # print field_counts
        for field in field_counts.iteritems():
            if(field[1] > 1 and field[0] != 'histo'):
                label_fields.append(field[0])
            if(field[1] == 1 and field[0] != 'histo' and field[0] != 'classtype' and field[0] != 'sample'):
                if(gen_sel is None and field[0] == 'gen_sel'):
                    continue
                text_fields.append(field[0])
#         print 'label fields: {}'.format(label_fields)
#         print 'text fields: {}'.format(text_fields)

        for item in histo_df[label_fields].iterrows():
            labels.append(', '.join([self.labels_dict[tx] for tx in item[1].values if self.labels_dict[tx] != '']))

        # print labels
        text = ', '.join([self.labels_dict[fl] for fl in histo_df[text_fields].iloc[0].values if self.labels_dict[fl] != ''])
        histo = [his.get(debug) for his in histo_df['histo'].values]
        return histo, labels, text
