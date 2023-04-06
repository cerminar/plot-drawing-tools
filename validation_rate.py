### This is the baseline set of plots for validation purposes

smps = ['12p5', 'compID']

# 
configs = [
    (['TkEmEE'],  ['IDTightPEtaABC'],       'hRate_TkEmEE_IDTightP_EtaABC'),
    (['TkEmEE'],  ['IDTightPIso0p1EtaABC'], 'hRate_TkEmEE_IDTightPIso0p1_EtaABC'),
    (['TkEmEE'],  ['EtaABC'],               'hRate_TkEmEE_IDLooseP_EtaABC'),
    (['TkEmEB'],  ['EtaF'],                 'hRate_TkEmEB_IDLooseP_EtaF'),

    (['TkEleEE'], ['IDTightEEtaABC'],       'hRate_TkEleEE_IDTightE_EtaABC'),
    (['TkEleEE'], ['EtaABC'],               'hRate_TkEleEE_IDLooseE_EtaABC'),
    (['TkEleEB'], ['EtaF'],                 'hRate_TkEleEB_IDLooseE_EtaF'),
    (['TkEleEB'], ['IDTightEEtaF'],         'hRate_TkEleEB_IDTightE_EtaF'),
    (['TkEleEB'], ['IDTightEIso0p1EtaF'],   'hRate_TkEleEB_IDTightEIso0p1_EtaF'),

    (['TkEmL2'],  ['EtaABC'],               'hRate_TkEmL2_IDLooseP_EtaABC'),
    (['TkEmL2'],  ['IDTightPEtaABC'],       'hRate_TkEmL2_IDTightP_EtaABC'),
    (['TkEmL2'],  ['EtaF'],                 'hRate_TkEmEB_IDLooseP_EtaF'),

    (['TkEleL2'], ['IDTightEEtaABC'],       'hRate_TkEleL2_IDTightE_EtaABC'),
    (['TkEleL2'], ['EtaABC'],               'hRate_TkEleL2_IDLooseE_EtaABC'),
    (['TkEleL2'], ['EtaF'],                 'hRate_TkEleL2_IDLooseE_EtaF'),
    (['TkEleL2'], ['IDTightEEtaF'],         'hRate_TkEleL2_IDTightE_EtaF'),

    (['TkEleL2'], ['IDTightEEtaFABC'],       'hRate_TkEleL2_IDTightE_EtaFABC'),
    (['TkEleL2'], ['EtaFABC'],               'hRate_TkEleL2_IDLooseE_EtaFABC'),

]


for objs, objs_sel, h_name in configs:
    print(f'obj: {objs}, sel: {objs_sel}, histo: {h_name}')

    dm = DrawMachine(newconfig)
    dm.config.legend_position = (0.4, 0.4)

    hsets, labels, text = hplot.get_histo(histos.RateHistos, smps, 'PU200', objs, objs_sel, None)
    dm.addHistos([his.h_pt for his in hsets], labels=labels)

    dm.addRatioHisto(1,0)
    dm.addRatioHisto(2,0)

    dm.draw(
        text=text,
        y_min=0.1, y_max=40000,
        x_min=0, x_max=60,
        y_min_ratio=0.5, y_max_ratio=2.0,
        y_log=True, 
        x_axis_label='online p_{T} thresh. [GeV]',
        h_lines=[20,100,1000],
    do_ratio=True)
    dm.toWeb(name=h_name, page_creator=wc)

#


#wc.publish()