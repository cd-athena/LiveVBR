# Import necessary libraries
import sys
import subprocess
import os
import argparse
import pandas as pd
import math
import pickle

# Main function
def main():
    """
    The main entry point of the program.
    """
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description='Process video with a specified resolution.')

    # Add arguments
    parser.add_argument('--video', help='Path to the input video file')
    parser.add_argument('--inputres', help='Resolution of the output video in the format WIDTHxHEIGHT')
    parser.add_argument('--minbr', help='Minimum bitrate value')
    parser.add_argument('--maxbr', help='Maximum bitrate value')
    parser.add_argument('--jnd', help='JND value- 2,4 or 6')
    
    # Parse the arguments
    args = parser.parse_args()

    # Access the parsed arguments
    input_video = args.video
    input_resolution = args.inputres
    MIN_BR = int(args.minbr)
    MAX_BR = int(args.maxbr)
    JND = int(args.jnd)

    # Get the current directory
    current_directory = os.getcwd()
    
    ## Run VCA
    # Define the command and arguments
    command = os.path.join(current_directory, 'build', 'vc15-x86_64', 'source', 'apps', 'vca', 'vca.exe')
    csv_file = os.path.join(current_directory,'test.csv')

    # Construct the command-line arguments
    args = [
        command,
        '--input', input_video,
        '--input-res', input_resolution,
        '--input-fps', '30',
        '--complexity-csv', csv_file
    ]
    
    # Run the command using subprocess
    subprocess.run(args, shell=True)
    
    ## Generate average features
    # Read E,h,L values of the full video
    df = pd.read_csv('test.csv')
    E_val = df[' E'].mean()
    h_val = df[' h'].mean()
    L_val = df[' L'].mean()
    
    ## Loading prediction models
    vmaf_pred_360 = pickle.load(open('./vmaf-pred/vmaf_pred_360', 'rb'))
    vmaf_pred_432 = pickle.load(open('./vmaf-pred/vmaf_pred_432', 'rb'))
    vmaf_pred_540 = pickle.load(open('./vmaf-pred/vmaf_pred_540', 'rb'))
    vmaf_pred_720 = pickle.load(open('./vmaf-pred/vmaf_pred_720', 'rb'))
    vmaf_pred_1080 = pickle.load(open('./vmaf-pred/vmaf_pred_1080', 'rb'))
    vmaf_pred_1440 = pickle.load(open('./vmaf-pred/vmaf_pred_1440', 'rb'))
    vmaf_pred_2160 = pickle.load(open('./vmaf-pred/vmaf_pred_2160', 'rb'))
    
    vmaf_models = {'360': vmaf_pred_360, '432': vmaf_pred_432, '540': vmaf_pred_540, '720': vmaf_pred_720, 
               '1080': vmaf_pred_1080, '1440': vmaf_pred_1440, '2160': vmaf_pred_2160}
               
    br_pred_360 = pickle.load(open('./bitrate-pred/br_pred_360', 'rb'))
    br_pred_432 = pickle.load(open('./bitrate-pred/br_pred_432', 'rb'))
    br_pred_540 = pickle.load(open('./bitrate-pred/br_pred_540', 'rb'))
    br_pred_720 = pickle.load(open('./bitrate-pred/br_pred_720', 'rb'))
    br_pred_1080 = pickle.load(open('./bitrate-pred/br_pred_1080', 'rb'))
    br_pred_1440 = pickle.load(open('./bitrate-pred/br_pred_1440', 'rb'))
    br_pred_2160 = pickle.load(open('./bitrate-pred/br_pred_2160', 'rb'))
    
    br_models = {'360': br_pred_360, '432': br_pred_432, '540': br_pred_540, '720': br_pred_720, 
               '1080': br_pred_1080, '1440': br_pred_1440, '2160': br_pred_2160}
               
    crf_pred_360 = pickle.load(open('./crf-pred/crf_pred_360', 'rb'))
    crf_pred_432 = pickle.load(open('./crf-pred/crf_pred_432', 'rb'))
    crf_pred_540 = pickle.load(open('./crf-pred/crf_pred_540', 'rb'))
    crf_pred_720 = pickle.load(open('./crf-pred/crf_pred_720', 'rb'))
    crf_pred_1080 = pickle.load(open('./crf-pred/crf_pred_1080', 'rb'))
    crf_pred_1440 = pickle.load(open('./crf-pred/crf_pred_1440', 'rb'))
    crf_pred_2160 = pickle.load(open('./crf-pred/crf_pred_2160', 'rb'))
    
    crf_models = {'360': crf_pred_360, '432': crf_pred_432, '540': crf_pred_540, '720': crf_pred_720, 
               '1080': crf_pred_1080, '1440': crf_pred_1440, '2160': crf_pred_2160}
    
    # Functions to determine the maximum VMAF possible with the combination of the best resolution, CRF for a given target bitrate
    def model_vmaf_value(resolution, target_br, test_vector):
          cur_vmaf = vmaf_models[resolution].predict([test_vector])[0]
          cur_crf = int(crf_models[resolution].predict([test_vector])[0])
          return cur_vmaf, cur_crf

    def get_best_vmaf_model(target_br, test_vector):
          resolutions = ['360', '432', '540', '720', '1080', '1440', '2160']
          max_vmaf = 0
          best_res = ''
          best_crf = 0

          for res in resolutions:
            cur_vmaf, cur_crf = model_vmaf_value(res, target_br, test_vector)
            if float(cur_vmaf) > float(max_vmaf):
              max_vmaf = cur_vmaf
              best_res = res
              best_crf = cur_crf    
          return target_br, best_res, cur_crf, max_vmaf
          
    # Functions to determine the bitrate value with the combination of the best resolution, CRF for a given VMAF
    def model_bitrate_value(resolution, max_vmaf, test_vector):
          cur_br = math.exp(br_models[resolution].predict([test_vector])[0])
          test_vector = test_vector[:-1] + [math.log(cur_br)]
          cur_crf = int(crf_models[resolution].predict([test_vector])[0])
          return cur_br, cur_crf

    def get_best_bitrate_model(target_vmaf, test_vector, prev_best_res, prev_crf):
          if target_vmaf > 96:
            target_vmaf = 96
          resolutions = ['360', '432', '540', '720', '1080', '1440', '2160']
          min_br = 1000000
          cur_crf = 0
          best_res = ''
          remove_list = []
          for cur_res in resolutions:
            if cur_res != prev_best_res:
              remove_list.append(cur_res)
            if cur_res == prev_best_res:
              break
          for cur_res in remove_list:
              resolutions.remove(cur_res)
          for res in resolutions:
            cur_br, cur_crf = model_bitrate_value(res, target_vmaf, test_vector)
            if float(cur_br) < float(min_br):
              min_br = cur_br
              best_res = res
          test_vector = [E_val, h_val, L_val, math.log(min_br)]
          if cur_crf >= prev_crf and best_res == prev_best_res:
            if best_res != '2160':
              try:
                best_res = resolutions[resolutions.index(best_res) + 1]
                cur_br, cur_crf = model_bitrate_value(res, target_vmaf, test_vector)
              except:
                best_res = '2160'
                cur_br, cur_crf = model_bitrate_value(res, target_vmaf, test_vector)
                if cur_crf >= prev_crf:
                  cur_crf -= 1
            elif best_res == '2160':
                cur_crf -= 1
          if cur_crf >= prev_crf:
            cur_crf = prev_crf - 1
          if best_res == '2160' and (prev_crf - cur_crf)>=6:
            cur_crf = prev_crf - 3
            if min_br > MAX_BR:
              min_br = MAX_BR - 1
          return min_br, best_res, cur_crf
    
    # Setting the minimum bitrate
    br_minimum = MIN_BR
    
    # First run
    test_vector = [E_val, h_val, L_val, math.log(br_minimum)]
    br_minimum, best_res, cur_crf, max_vmaf = get_best_vmaf_model(br_minimum, test_vector)
    
    # File to write the config settings according to the generated ladder
    fh = open('.\jnd_ladder_config.txt', 'w')
    j = 0 # Counter for index
    
    # Check if the VMAF value is 100 - JND or more
    if max_vmaf >= (100 - JND):
      max_vmaf = 100 - JND
      test_vector = [E_val, h_val, L_val, max_vmaf]
      br_minimum, best_res, cur_crf = get_best_bitrate_model(max_vmaf, test_vector, best_res, cur_crf)
      # If maximum bitrate is not reached, write the current row of the ladder 
      if br_minimum <= MAX_BR:
        fh.writelines('[id_' + str(j+1) + ':0:nil] --input ' + str(best_res) +'pSource.y4m --crf ' + str(cur_crf) +' --vbv-maxrate ' + str(round(br_minimum,2)) + ' --vbv-bufsize 48000 --strict-cbr -o hevc/out_' + str(j+1) +'.hevc --csv out_' + str(j+1) +'.csv --preset ultrafast' + '\n')
        j += 1
    else:
        fh.writelines('[id_' + str(j+1) + ':0:nil] --input ' + str(best_res) +'pSource.y4m --crf ' + str(cur_crf) +' --vbv-maxrate ' + str(round(br_minimum,2)) + ' --vbv-bufsize 48000 --strict-cbr -o hevc/out_' + str(j+1) +'.hevc --csv out_' + str(j+1) +'.csv --preset ultrafast' + '\n')
        j += 1
        # Loop until the VMAF value reaches 100 - JND or more
        while max_vmaf <= (100 - JND):
          max_vmaf = float(max_vmaf) + 6
          # Clip the VMAF value
          if max_vmaf > (100 - JND):
            max_vmaf = 100 - JND + 0.01 # Added 0.01 to avoid infinite loop while clipping
          test_vector = [E_val, h_val, L_val, max_vmaf]
          br_minimum, best_res, cur_crf = get_best_bitrate_model(max_vmaf, test_vector, best_res, cur_crf)
          if br_minimum > MAX_BR: # Break if the maximum bitrate is reached
            break
          fh.writelines('[id_' + str(j+1) + ':0:nil] --input ' + str(best_res) +'pSource.y4m --crf ' + str(cur_crf) +' --vbv-maxrate ' + str(round(br_minimum,2)) + ' --vbv-bufsize 48000 --strict-cbr -o hevc/out_' + str(j+1) +'.hevc --csv out_' + str(j+1) +'.csv --preset ultrafast' + '\n')
          j += 1
          

# Execute the main function
if __name__ == "__main__":
    main()