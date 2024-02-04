import os

# heliolinc run commands
# hl_make_tracklets = './heliolinc2/src/make_tracklets -dets ./true_raw_input.csv -pairdets ./output.csv -colformat ./heliolinc2/tests/colformat_LSST_01.txt -pairs LSST_pairs_01.csv -earth ./heliolinc2-main/tests/Earth1day2020s_02a.txt -obscode ./heliolinc2-main/tests/ObsCodes.txt'
# hl_generate = './heliolinc2/src/heliolinc -dets ./output.csv -pairs ./LSST_pairs_01.csv -mjd 60608.63 -obspos ./heliolinc2/tests/Earth1day2020s_02a.txt -heliodist ./heliolinc2-main/tests/accelmat_mb08a_sp04.txt -out LSST_hl_all.csv -outsum LSST_hl_summary.csv'
# gen_lflist = 'echo "LSST_hl_all.csv LSST_hl_summary.csv" > LSST_lflist01'
# hl_link_refine = './heliolinc2/src/link_refine -pairdet ./output.csv -lflist LSST_lflist01 -outfile LSST_linkref_all01.csv -outsum LSST_linkref_summary01.csv'
# hl_link_refine_multisite = './heliolinc2/src/link_refine_multisite -pairdet ./output.csv -lflist LSST_lflist01 -outfile LSST_linkref_all01.csv -outsum LSST_linkref_summary01.csv'

navigate = './heliolinc2/tests'
hl_generate = '../src/heliolinc_danby -imgs outim_test01.txt -pairdets pairdet_test01.csv -tracklets tracklets_test01.csv -trk2det trk2det_test01.csv -mjd 60607.74 -obspos Earth1day2020s_02a.csv -heliodist radhyp_test01.txt -outsum sum_test01.csv -clust2det clust2det_test01.csv'
gen_lflist = 'printf "sum_test01.csv clust2det_test01.csv\n" > clusterlist_test01'
hl_link_refine = '../src/link_refine_Herget_univar -imgs outim_test01.txt -pairdets pairdet_test01.csv -lflist clusterlist_test01 -mjd 60607.74 -outsum LRHsum_test01.csv -clust2det LRHclust2det_test01.csv'

def run_heliolinc(uid):
  # navigate to heliolinc directory
  print("Current directory before navigation:", os.getcwd())
  os.chdir(navigate)
  print("Current directory after navigation:", os.getcwd())
  # make tracklets
  hl_make_tracklets = f'../src/make_tracklets_new -dets heliolinc-comprehensive/heliolinc-backend/temp_files/{uid}_input.csv -outim outim_test01.txt -pairdets pairdet_test01.csv -tracklets tracklets_test01.csv -trk2det trk2det_test01.csv -colformat colformat_LSST_01.txt -imrad 2.0 -maxtime 2.0 -maxGCR 1.5 -maxvel 1.5 -minarc 1.0 -earth Earth1day2020s_02a.csv -obscode ObsCodesNew.txt'
  print(hl_make_tracklets)
  os.system(hl_make_tracklets)
  print("TRACKLETS MADE")
  # run heliolinc
  os.system(hl_generate)
  print("LINKS GENERATED")
  # generate link refine file
  os.system(gen_lflist)
  print("LINK REFINE SET CREATED")
  # link refine
  os.system(hl_link_refine)
  print("LINKS REFINED")