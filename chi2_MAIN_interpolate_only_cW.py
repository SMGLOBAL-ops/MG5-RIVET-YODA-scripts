#!/usr/bin/python
# encoding=utf8
import sys
import yoda
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import spline

def yoda_chisq(hist1, hist2):
    # function to calculate chisquare for all hists between two yoda files
    # first argument is the SM yoda file, second is the non-SM yoda file

    # read in yoda files
    h1 = yoda.read(hist1)
    h2 = yoda.read(hist2)

    # remove non histograms (ones that don't start with /ATLAS)
    for item in h1.keys():
        if "/ATLAS" not in str(item):
            non_hist = h1.pop(item)
        elif "/RAW/ATLAS" in str(item):
                         non_hist2 = h1.pop(item)
        elif "/CoMom_ZZ" in str(item):
             non_hist = h1.pop(item)
            # print("Removing {item}".format(item=non_hist))

    for item in h2.keys():
        if "/ATLAS" not in str(item):
            non_hist = h2.pop(item)
        elif "/RAW/ATLAS" in str(item):
          non_hist2 = h2.pop(item)
        elif "/CoMom_ZZ" in str(item):
                   non_hist = h2.pop(item)
            # print("Removing {item}".format(item=non_hist))

    chisquare_all = {}
    # loop over all histograms
    for hist in h1.keys():
        # get name of histogram
        hist_name = str(h1[hist]).split('/')[-1].split("'")[0]
        # check if histogram name matches between yoda files
        if hist_name != str(h2[hist]).split('/')[-1].split("'")[0]:
            sys.stderr.write("***\n")
            sys.stderr.write("Error: Yodas are probably from different analyses\n")
            sys.stderr.write("***\n")
            return
        # print("Processing histogram " + hist_name + "...")

        # get bins of histogram
        hb1 = h1[hist].bins()
        hb2 = h2[hist].bins()

        # loop over bins, adding to the chisquare sum each iteration
        chisquare_all[hist_name] = 0
        for i in range(0, len(hb1)):
            error = hb1[i].sumW() ** 0.5  # error is sqrt(N) for bins in yoda1
            # if error is 0, add 0 to chisquare
            if error == 0:
                continue
            # add to the chisquare value for the current histogram
            chisquare_all[hist_name] += (hb1[i].sumW() - hb2[i].sumW()) ** 2 / error ** 2


    return chisquare_all
    
    
ewk_qcd_file = "SMEFT_SMlimit.yoda"

poi_values = ["-0.35", "-0.25", "-0.15", "-0.1", "-0.05", "1.000000e-99", "0.15", "0.25", "0.35"]

results = []
for poi in poi_values:
    poi_file="cW_{param}.yoda".format(param=poi)
    chi2=yoda_chisq(ewk_qcd_file, poi_file)
    results.append(chi2)

print(poi_values)
print(results)

poi_numerical_values =  [-0.35, -0.25, -0.15, -0.1, -0.05, 0.0, 0.15, 0.25, 0.35]

# error_keys = []
error_values = []

x_print_list = []

for key, value in results[0].items():
    
    if key not in ["pT_jet2", "mass_dijet", "deltay_dijet", "m4l_inclusive_dijet", "yproduct", "pt_jet_ratio", "Zep_Z1", "Zep_Z2", "Zep_Z1_vbs", "Zep_Z2_vbs", "zstar4l", "ystar4l", "mass_dijet_vbs", "m4l_inclusive_vbs", "ptZ1_vbs", "ptZ2_vbs", "pt4l_vbs", "costhetastar1_vbs", "costhetastar2_vbs"]:
        continue

    print(key)
#     error_keys.append(key)
    
    temp_list = []
    for item in results:
        temp_list.append(item[key])
        
#     sorted_dict = OrderedDict(
#     sorted((key, list(sorted(vals, reverse=True)))
#
#     for key, vals in d.items()))
#         print(sorted_dict)


  #  temp_list_2 = []
  #  minimum = min(temp_list)
  #  for item in temp_list:
   #     temp_list_2.append(item - minimum)
   
    plt.title('$\chi^2$ minimisation %s' % key)
    plt.ylabel('$\chi^2$ ')
    plt.xlabel('cW parameter value')

    y_line = [4] * 300

  #  plt.plot(poi_numerical_values, temp_list)
 #  plt.plot(poi_numerical_values, y_line)
    
    x = np.array(poi_numerical_values)
    y = np.array(temp_list)

    x_smooth = np.linspace(x.min(), x.max(),300)
    y_smooth = spline(x,y, x_smooth)

    plt.plot(x_smooth, y_line)
    plt.plot(x_smooth, y_smooth)
    
    x = poi_numerical_values
    y = temp_list
    for i, j in zip(x, y):
        rounded = '%.2f' % j
        label = '('+str(i)+', '+rounded+')'
        plt.text(i, j+1.5, label, fontsize=4)
       
    
#     idx = np.argwhere(np.isclose(y_line, y_smooth, atol=0.1)).reshape(-1)
    idx = np.argwhere(np.diff(np.sign(y_smooth - y_line))).flatten()
 #   print(idx)
 
    # Plotting points of intersection
    plt.plot(x_smooth[max(idx)], y_smooth[max(idx)], 'ro')
    plt.plot(x_smooth[min(idx)], y_smooth[min(idx)], 'ro')
    
    
    # Calculating and printing error
    max_idx = abs(x_smooth[max(idx)])
    min_idx = abs(x_smooth[min(idx)])
    if max_idx > min_idx:
        idx_error = max_idx - min_idx
    else:
        idx_error = min_idx - max_idx
    idx_error = idx_error/2
   # idx_label = "Error = " + str(idx_error)
    error_values.append((key, idx_error))
        
  #  plt.text(-2.0, -1.5, idx_label, fontsize=6)
#     print(idx_label)
    
    plt.savefig('Chi2_plots/chi2_%s.pdf' % key)
    plt.clf()
    
    x_intersect_points = x_smooth[idx]
    x_print_item = 0.25
    x_print_index = poi_numerical_values.index(x_print_item)
    x_print_list.append((key, temp_list[x_print_index], x_intersect_points, idx_error))


    
x_print_list_sorted = sorted(x_print_list, key=lambda x: x[1], reverse=True)
print("\n\nOrdered Values for chosen parameter value:")
for item in x_print_list_sorted:
#     print(item[0], item[1])
#     print(item[0] + ' intersects:')
#     print(item[2])
    print(item[0], 'Value at 0.25:', item[1], 'Error:', item[2])
    
print("\n\nPaste these into an excel document and do a line of best fit maybe?")
for item in x_print_list_sorted:
    print(item[2])
    
# smallest_error_index = error_values.index(min(error_values))
# print("Smallest Error:")
# print(error_keys[smallest_error_index], error_values[smallest_error_index])

sorted_error_values = sorted(error_values, key=lambda x: x[1])
print("\n\nError Values:")
for item in sorted_error_values:
    print(item)

    

# plt.plot(poi_numerical_values, param_plot)
# plt.title('$\chi^2$ minimisation pt4l_onshell')
# plt.ylabel('$\chi^2$ ')
# plt.xlabel('cW parameter value')
# plt.savefig('Chi2_looptest/chi2_pt4l_onshell.pdf')


#x = np.array([poi_numerical_values])
#y = np.array([param_plot])

#x_smooth = np.linespace(x.min(), x.max(),300)
#y_smooth = spline(x,y, x_smooth)

#plt.plot(x_smooth, y_smooth)

#plt.show()






 #yoda_chisq("EWK_QCD_cW_1.00000e-99_paramvalue-scaled.yoda","EWK_QCD_cW_--_paramvalue-scaled.yoda")

 #yoda_chisq("EWK_QCD_cW_1.00000e-99_paramvalue-scaled.yoda","EWK_QCD_cW_-0.75_paramvalue-scaled.yoda")

 #yoda_chisq("EWK_QCD_cW_1.00000e-99_paramvalue-scaled.yoda","EWK_QCD_cW_-0.50_paramvalue-scaled.yoda")

 #yoda_chisq("EWK_QCD_cW_1.00000e-99_paramvalue-scaled.yoda","EWK_QCD_cW_-0.25_paramvalue-scaled.yoda")

 #yoda_chisq("EWK_QCD_cW_1.00000e-99_paramvalue-scaled.yoda","EWK_QCD_cW_0.25_paramvalue-scaled.yoda")

 #yoda_chisq("EWK_QCD_cW_1.00000e-99_paramvalue-scaled.yoda","EWK_QCD_cW_0.50_paramvalue-scaled.yoda")

 #yoda_chisq("EWK_QCD_cW_1.00000e-99_paramvalue-scaled.yoda","EWK_QCD_cW_0.75_paramvalue-scaled.yoda")

 #yoda_chisq("EWK_QCD_cW_1.00000e-99_paramvalue-scaled.yoda","EWK_QCD_cW_1.0_paramvalue-scaled.yoda")


