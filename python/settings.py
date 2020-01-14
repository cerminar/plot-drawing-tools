# %load python/settings.py

# === samples =====================================================
import pprint
import python.plotters_config as plotters



samples = []

# samples += samples_nugunrates
# samples += samples_nugunrates_V8
samples += samples_ele_V9

for smp in samples:
    smp.open_file()


sample = 'ele-V9'

# === TP ==========================================================
tps = [
       'EG',
        'EGBRL',
#        'TkEle',
       'TkEleEL',
#        'TkEleBRL',
       'TkEleELBRL',
#        'TkEleALL',
       'TkEleELALL'
]

# === Load the Histo Primitives ====================================
histo_primitives = samples[0].build_file_primitive_index()


# print histo_primitives.data.unique()
# === TP selections ================================================
tp_select = {}

for tp in tps:
    tp_select[tp] = histo_primitives[histo_primitives.tp == tp].tp_sel.unique().tolist()

# ==== GEN selections ===============================================
gen_select ={}
for tp in tps:
    gen_select[tp] = histo_primitives[histo_primitives.tp == tp].gen_sel.unique().tolist()


import pprint
pp = pprint.PrettyPrinter(indent=4)
print '--- TPs: '
pp.pprint(tps)
print '--- TP selections:'
pp.pprint(tp_select)
print '--- GEN selections:'
pp.pprint(gen_select)
