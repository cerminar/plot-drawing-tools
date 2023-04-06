# %load validation_egeff.py
### This is the baseline set of plots for validation purposes

smps_pho = ['pho-12p5', 'pho-compID']
smps_ele = ['ele-12p5', 'ele-compID']



# eff vs eta

configs = [
    (smps_pho, ['TkEmEB', 'TkEmEE'], ['all'],      ['GENPt15', 'GENEePt15'],  'hEffVsEta_TkEm_IDLooseP_GENPt15'),
    (smps_pho, ['TkEmEB', 'TkEmEE'], ['all'],      ['GENPt30', 'GENEePt30'],  'hEffVsEta_TkEm_IDLooseP_GENPt30'),
    (smps_pho, ['TkEmEB', 'TkEmEE'], ['IDTightP'], ['GENPt30', 'GENEePt30'],  'hEffVsEta_TkEm_IDTightP_GENPt30'),

    (smps_ele, ['TkEleEB', 'TkEleEE'], ['all'],      ['GENPt15', 'GENEePt15'],  'hEffVsEta_TkEle_IDLooseE_GENPt15'),
    (smps_ele, ['TkEleEB', 'TkEleEE'], ['all'],      ['GENPt30', 'GENEePt30'],  'hEffVsEta_TkEle_IDLooseE_GENPt30'),
    (smps_ele, ['TkEleEB', 'TkEleEE'], ['IDTightE'], ['GENPt15', 'GENEePt15'],  'hEffVsEta_TkEle_IDTightE_GENPt15'),
    (smps_ele, ['TkEleEB', 'TkEleEE'], ['IDTightE'], ['GENPt30', 'GENEePt30'],  'hEffVsEta_TkEle_IDTightE_GENPt30'),

    (smps_pho, ['TkEmL2',], ['all'],      ['GENPt15', 'GENEePt15'],  'hEffVsEta_TkEmL2_IDLooseP_GENPt15'),
    (smps_pho, ['TkEmL2',], ['all'],      ['GENPt30', 'GENEePt30'],  'hEffVsEta_TkEmL2_IDLooseP_GENPt30'),
    (smps_pho, ['TkEmL2',], ['IDTightP'], ['GENPt30', 'GENEePt30'],  'hEffVsEta_TkEmL2_IDTightP_GENPt30'),

    (smps_ele, ['TkEleL2',], ['all'],      ['GENPt15', 'GENEePt15'],  'hEffVsEta_TkEleL2_IDLooseE_GENPt15'),
    (smps_ele, ['TkEleL2',], ['all'],      ['GENPt30', 'GENEePt30'],  'hEffVsEta_TkEleL2_IDLooseE_GENPt30'),
    (smps_ele, ['TkEleL2',], ['IDTightE'], ['GENPt15', 'GENEePt15'],  'hEffVsEta_TkEleL2_IDTightE_GENPt15'),
    (smps_ele, ['TkEleL2',], ['IDTightE'], ['GENPt30', 'GENEePt30'],  'hEffVsEta_TkEleL2_IDTightE_GENPt30'),

]


for smps, objs, objs_sel, gen_sel, h_name in configs:
    print(f'obj: {objs}, sel: {objs_sel}, histo: {h_name}')

    dm = DrawMachine(newconfig)
    dm.config.legend_position = (0.1,0.15)

    hsets, labels, text = hplot.get_histo(
        histos.HistoSetEff, 
        smps, 
        ['PU200'], 
        objs, 
        objs_sel, gen_sel, debug=False)

    dm.addHistos([his.h_eff.h_abseta.CreateGraph() for his in hsets], labels=labels)

    dm.addRatioHisto(0,1)

    dm.draw(text=text, 
            x_min=0., x_max=3.2, 
            y_min=0.5, y_max=1.1, v_lines=[1.52, 1.7, 2.4],
           do_ratio=False,
           y_min_ratio=0.9,
           y_max_ratio=1.1)
    # dm.write(name='eg_TDRvsSummer20_matchig_eff')

    dm.toWeb(name=h_name, page_creator=wc)

#



# eff vs pT

configs = [
    (smps_pho, ['TkEmEB'], ['all'],      ['GENEtaF'],    'hEffVsPt_TkEmEB_IDLooseP_GENEtaF'),
    (smps_pho, ['TkEmEB'], ['IDTightP'], ['GENEtaF'],    'hEffVsPt_TkEmEB_IDTightP_GENEtaF'),
    (smps_pho, ['TkEmEE'], ['all'],      ['GENEeEtaBC'], 'hEffVsPt_TkEmEE_IDLooseP_GENEtaBC'),
    (smps_pho, ['TkEmEE'], ['IDTightP'], ['GENEeEtaBC'], 'hEffVsPt_TkEmEE_IDTightP_GENEtaBC'),

    (smps_ele, ['TkEleEB'], ['all'],      ['GENEtaF'],    'hEffVsPt_TkEleEB_IDLooseE_GENEtaF'),
    (smps_ele, ['TkEleEB'], ['IDTightE'], ['GENEtaF'],    'hEffVsPt_TkEleEB_IDTightE_GENEtaF'),
    (smps_ele, ['TkEleEE'], ['all'],      ['GENEeEtaBC'], 'hEffVsPt_TkEleEE_IDLooseE_GENEtaBC'),
    (smps_ele, ['TkEleEE'], ['IDTightE'], ['GENEeEtaBC'], 'hEffVsPt_TkEleEE_IDTightE_GENEtaBC'),

    
]


for smps, objs, objs_sel, gen_sel, h_name in configs:
    print(f'obj: {objs}, sel: {objs_sel}, histo: {h_name}')

    dm = DrawMachine(newconfig)
    dm.config.legend_position = (0.3,0.15)

    hsets, labels, text = hplot.get_histo(
        histos.HistoSetEff, 
        smps, 
        ['PU200'], 
        objs, 
        objs_sel, 
        gen_sel, debug=False)
    # for hset in hsets:
    #     hset.computeEff(rebin=2)
    dm.addHistos([his.h_eff.h_pt.CreateGraph() for his in hsets], labels=labels)

    dm.addRatioHisto(1,0)
    dm.addRatioHisto(2,0)
    # dm.addRatioHisto(3,0)
    # dm.addRatioHisto(4,0)


    dm.draw(text=text, 
            x_min=0, x_max=100, 
            y_min=0.0, y_max=1.1, 
            h_lines=[1.0, 0.9],
           do_ratio=True,
           y_min_ratio=0.8,
           y_max_ratio=1.2)
    # dm.write(name='eg_TDRvsSummer20_matchig_eff')

    dm.toWeb(name=h_name, page_creator=wc)


#wc.publish()