import uuid
import ROOT
from drawingTools import draw
stuff = []

def gausstailfit_wc(name, project_hist, bin_limits):
    global cache
    if cache is not None and not cache[(cache.h_name == name) & (cache.bin_limits == bin_limits)].empty:
        print 'READ cached fit results h_name: {}, bin_limits: {}'.format(name, bin_limits)
        print cache[(cache.h_name == name) & (cache.bin_limits == bin_limits)].results
        return cache[(cache.h_name == name) & (cache.bin_limits == bin_limits)].results.values[0]

    max_bin = project_hist.GetMaximumBin()
    max_value = project_hist.GetBinCenter(max_bin)
    rms_value = project_hist.GetRMS()
    max_y = project_hist.GetMaximum()
#     print max_bin, max_value, rms_value

    def gausstail(x, p):
        #         // [Constant] * ROOT::Math::crystalball_function(x, [Alpha], [N], [Sigma], [Mean])
        return p[0] * ROOT.Math.crystalball_function(x[0], p[3], p[4], p[2], p[1])

    fitf = ROOT.TF1('gausstail', gausstail, -1.5, 1.5, 5)
    fitf.SetParNames('norm', 'mean', 'sigma', 'alpha', 'n')
#     fitf.FixParameter(0, 1.)
    fitf.SetParLimits(1, max_value-0.04, max_value+0.04)

    fitf.SetParameters(max_y, max_value, rms_value, 1, 1)
    draw([project_hist], labels=['fit'], text=name)
    stuff.append(fitf)
    project_hist.Draw("same")
#     c.Draw()
    print '   name: {}, y_max = {}, max_value = {}, RMS = {}'.format(name, max_y, max_value, rms_value)
    result = project_hist.Fit('gausstail', 'QERLS+')
    result.Print()
    print '   norm = {}, reso_mean = {}, reso_sigma = {}, alpha = {}, n = {}'.format(result.GetParams()[0], result.GetParams()[1], result.GetParams()[2], result.GetParams()[3], result.GetParams()[4])
#     func = project_hist.GetFunction("gaus")
    # print '   NDF = {}, chi2 = {}, prob = {}'.format(fitf.GetNDF(), fitf.GetChisquare(), fitf.GetProb())

    if cache is not None:
        cache = cache.append({'h_name': name,
                              'bin_limits': bin_limits,
                              'results': result}, ignore_index=True)
#         print cache

    return result


def computeEResolution(h2d_orig,
                       bins_limits=[(3, 6), (7, 12), (13, 23), (24, 34), (35, 49), (50, 100)],
                       cache=None):
    global stuff
    h2d = h2d_orig.Clone()
    h2d.GetYaxis().SetRangeUser(-100, 100)
    x, y, ex_l, ex_h, ey_l, ey_h = [], [], [], [], [], []
    print '-----------------------'
    for x_bin_low, x_bin_high in bins_limits:
        y_proj = h2d.ProjectionY(uuid.uuid4().hex[:6]+'_y', x_bin_low, x_bin_high)
        stuff.append(y_proj)
        x_low = h2d.GetXaxis().GetBinLowEdge(x_bin_low)
        x_high = h2d.GetXaxis().GetBinUpEdge(x_bin_high)
        print 'x_low: {} x_high: {}'.format(x_low, x_high)
#         fit_result = gausstailfit(h2d_orig.GetName(), y_proj)
        fit_result = gausstailfit_wc(h2d_orig.GetName(), y_proj, (x_bin_low, x_bin_high))
        h2d.SetAxisRange(x_low, x_high)
        x_mean = h2d.GetMean()
#         print 'mean: {}'.format(x_mean)
    #     x_value = h2d.GetXaxis().GetBinCenter(x_bin)
    #     x_err_min = x_value - h2d.GetXaxis().GetBinLowEdge(x_bin)
    #     x_err_plus = h2d.GetXaxis().GetBinUpEdge(x_bin) - x_value

        x.append(x_mean)
        ex_l.append(0)
        ex_h.append(0)
        y.append(fit_result.GetParams()[2])

#         y.append(fit_result.GetParams()[2]/x_mean)
        ey_l.append(0)
        ey_h.append(0)
    return x, y, ex_l, ex_h, ey_l, ey_h


def computeEResolutionMean(h2d_orig,
                           bins_limits=[(3, 6), (7, 12), (13, 23), (24, 34), (35, 49), (50, 100)],
                           cache=None):
    h2d = h2d_orig.Clone()
    h2d.GetYaxis().SetRangeUser(-100, 100)
    x, y, ex_l, ex_h, ey_l, ey_h = [], [], [], [], [], []
    print '-----------------------'
    for x_bin_low, x_bin_high in bins_limits:
        y_proj = h2d.ProjectionY(uuid.uuid4().hex[:6]+'_y', x_bin_low, x_bin_high)
        stuff.append(y_proj)
        x_low = h2d.GetXaxis().GetBinLowEdge(x_bin_low)
        x_high = h2d.GetXaxis().GetBinUpEdge(x_bin_high)
        print 'x_low: {} x_high: {}'.format(x_low, x_high)
#         fit_result = gausstailfit(h2d_orig.GetName(), y_proj)
        fit_result = gausstailfit_wc(h2d_orig.GetName(), y_proj, (x_bin_low, x_bin_high))

        h2d.SetAxisRange(x_low, x_high)
        x_mean = h2d.GetMean()
#         print 'mean: {}'.format(x_mean)
    #     x_value = h2d.GetXaxis().GetBinCenter(x_bin)
    #     x_err_min = x_value - h2d.GetXaxis().GetBinLowEdge(x_bin)
    #     x_err_plus = h2d.GetXaxis().GetBinUpEdge(x_bin) - x_value

        x.append(x_mean)
        ex_l.append(0)
        ex_h.append(0)

        y.append(fit_result.GetParams()[1])
        ey_l.append(0)
        ey_h.append(0)
    return x, y, ex_l, ex_h, ey_l, ey_h
