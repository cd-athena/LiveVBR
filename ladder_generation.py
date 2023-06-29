'''
 *****************************************************************************
 * Copyright (C) 2023 Christian Doppler Laboratory ATHENA
 *
 * Authors: Vignesh V Menon <vignesh.menon@aau.at>
 *          Prajit T Rajendran <prajit.thazhurazhikath-rajendran@universite-paris-saclay.fr>
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.
 *****************************************************************************
'''

# Importing necessary libraries
import pandas as pd
import math
import pickle
import os
import subprocess
import sys

# Creating a class to handle ladder generation
class LadderGenerator:
    # Constructor
    def __init__(self, input_video, input_resolution, codec, MIN_BR, MAX_BR, JND, output_name):
        # Get the current directory
        self.current_directory = os.getcwd()
        self.input_video = input_video
        self.input_resolution = input_resolution
        self.codec = codec
        self.MIN_BR = MIN_BR
        self.MAX_BR = MAX_BR
        self.JND = JND
        self.output_name = output_name
    
    # Function to run VCA on input video and generate necessary features
    def run_vca(self):
        # Define the command and arguments
        command = os.path.join(self.current_directory, 'VCA', 'source', 'apps', 'vca', 'vca.exe')
        csv_file = os.path.join(self.current_directory,'test.csv')

        # Construct the command-line arguments
        args = [
            command,
            '--input', self.input_video,
            '--input-res', self.input_resolution,
            '--input-fps', '30',
            '--complexity-csv', csv_file
        ]

        # Run the command using subprocess
        subprocess.run(args, shell=True)
        
    # Generate average features
    def generate_features(self):
        # Read E,h,L values of the full video
        df = pd.read_csv(os.path.join(self.current_directory,'test.csv'))
        self.E_val = df[' E'].mean()
        self.h_val = df[' h'].mean()
        self.L_val = df[' L'].mean()
        
    # Load corresponding prediction models
    def load_models(self):
        # Set path to model
        if self.codec == 'x265':
            model_path = './models/x265/'
        else:
            print('Codec not supported')
            sys.exit()
            
        # Loading prediction models
        vmaf_pred_360 = pickle.load(open(os.path.join(model_path,'vmaf-pred','vmaf_pred_360'), 'rb'))
        vmaf_pred_432 = pickle.load(open(os.path.join(model_path,'vmaf-pred','vmaf_pred_432'), 'rb'))
        vmaf_pred_540 = pickle.load(open(os.path.join(model_path,'vmaf-pred','vmaf_pred_540'), 'rb'))
        vmaf_pred_720 = pickle.load(open(os.path.join(model_path,'vmaf-pred','vmaf_pred_720'), 'rb'))
        vmaf_pred_1080 = pickle.load(open(os.path.join(model_path,'vmaf-pred','vmaf_pred_1080'), 'rb'))
        vmaf_pred_1440 = pickle.load(open(os.path.join(model_path,'vmaf-pred','vmaf_pred_1440'), 'rb'))
        vmaf_pred_2160 = pickle.load(open(os.path.join(model_path,'vmaf-pred','vmaf_pred_2160'), 'rb'))
        
        self.vmaf_models = {'360': vmaf_pred_360, '432': vmaf_pred_432, '540': vmaf_pred_540, '720': vmaf_pred_720, 
                   '1080': vmaf_pred_1080, '1440': vmaf_pred_1440, '2160': vmaf_pred_2160}
                   
        br_pred_360 = pickle.load(open(os.path.join(model_path,'bitrate-pred','br_pred_360'), 'rb'))
        br_pred_432 = pickle.load(open(os.path.join(model_path,'bitrate-pred','br_pred_432'), 'rb'))
        br_pred_540 = pickle.load(open(os.path.join(model_path,'bitrate-pred','br_pred_540'), 'rb'))
        br_pred_720 = pickle.load(open(os.path.join(model_path,'bitrate-pred','br_pred_720'), 'rb'))
        br_pred_1080 = pickle.load(open(os.path.join(model_path,'bitrate-pred','br_pred_1080'), 'rb'))
        br_pred_1440 = pickle.load(open(os.path.join(model_path,'bitrate-pred','br_pred_1440'), 'rb'))
        br_pred_2160 = pickle.load(open(os.path.join(model_path,'bitrate-pred','br_pred_2160'), 'rb'))
        
        self.br_models = {'360': br_pred_360, '432': br_pred_432, '540': br_pred_540, '720': br_pred_720, 
                   '1080': br_pred_1080, '1440': br_pred_1440, '2160': br_pred_2160}
                   
        crf_pred_360 = pickle.load(open(os.path.join(model_path,'crf-pred','crf_pred_360'), 'rb'))
        crf_pred_432 = pickle.load(open(os.path.join(model_path,'crf-pred','crf_pred_432'), 'rb'))
        crf_pred_540 = pickle.load(open(os.path.join(model_path,'crf-pred','crf_pred_540'), 'rb'))
        crf_pred_720 = pickle.load(open(os.path.join(model_path,'crf-pred','crf_pred_720'), 'rb'))
        crf_pred_1080 = pickle.load(open(os.path.join(model_path,'crf-pred','crf_pred_1080'), 'rb'))
        crf_pred_1440 = pickle.load(open(os.path.join(model_path,'crf-pred','crf_pred_1440'), 'rb'))
        crf_pred_2160 = pickle.load(open(os.path.join(model_path,'crf-pred','crf_pred_2160'), 'rb'))
        
        self.crf_models = {'360': crf_pred_360, '432': crf_pred_432, '540': crf_pred_540, '720': crf_pred_720, 
                   '1080': crf_pred_1080, '1440': crf_pred_1440, '2160': crf_pred_2160}
                   
    # Functions to determine the maximum VMAF possible with the combination of the best resolution, CRF for a given target bitrate
    def model_vmaf_value(self, resolution, target_br, test_vector):
          cur_vmaf = self.vmaf_models[resolution].predict([test_vector])[0]
          cur_crf = int(self.crf_models[resolution].predict([test_vector])[0])
          return cur_vmaf, cur_crf

    def get_best_vmaf_model(self, target_br, test_vector):
          resolutions = ['360', '432', '540', '720', '1080', '1440', '2160']
          max_vmaf = 0
          best_res = ''
          best_crf = 0

          for res in resolutions:
            cur_vmaf, cur_crf = self.model_vmaf_value(res, target_br, test_vector)
            if float(cur_vmaf) > float(max_vmaf):
              max_vmaf = cur_vmaf
              best_res = res
              best_crf = cur_crf    
          return target_br, best_res, cur_crf, max_vmaf
          
    # Functions to determine the bitrate value with the combination of the best resolution, CRF for a given VMAF
    def model_bitrate_value(self, resolution, max_vmaf, test_vector):
          cur_br = math.exp(self.br_models[resolution].predict([test_vector])[0])
          test_vector = test_vector[:-1] + [math.log(cur_br)]
          cur_crf = int(self.crf_models[resolution].predict([test_vector])[0])
          return cur_br, cur_crf

    def get_best_bitrate_model(self, target_vmaf, test_vector, prev_best_res, prev_crf):
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
            cur_br, cur_crf = self.model_bitrate_value(res, target_vmaf, test_vector)
            if float(cur_br) < float(min_br):
              min_br = cur_br
              best_res = res
          test_vector = [self.E_val, self.h_val, self.L_val, math.log(min_br)]
          if cur_crf >= prev_crf and best_res == prev_best_res:
            if best_res != '2160':
              try:
                best_res = resolutions[resolutions.index(best_res) + 1]
                cur_br, cur_crf = self.model_bitrate_value(res, target_vmaf, test_vector)
              except:
                best_res = '2160'
                cur_br, cur_crf = self.model_bitrate_value(res, target_vmaf, test_vector)
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
          
    # Function to generate the ladder
    def generate_ladder(self):
        # Setting the minimum bitrate
        br_minimum = self.MIN_BR
        
        # First run
        test_vector = [self.E_val, self.h_val, self.L_val, math.log(br_minimum)]
        br_minimum, best_res, cur_crf, max_vmaf = self.get_best_vmaf_model(br_minimum, test_vector)
        
        # File to write the config settings according to the generated ladder
        fh = open('.\jnd_ladder_config.txt', 'w')
        dict_ladder = {
                    'Codec': [],
                    'ID' : [],
                    'Bitrate' : [],
                    'CRF' : [],
                    }

        j = 0 # Counter for index
        
        # Check if the VMAF value is 100 - JND or more
        if max_vmaf >= (100 - self.JND):
          max_vmaf = 100 - self.JND
          test_vector = [self.E_val, self.h_val, self.L_val, max_vmaf]
          br_minimum, best_res, cur_crf = self.get_best_bitrate_model(max_vmaf, test_vector, best_res, cur_crf)
          # If maximum bitrate is not reached, write the current row of the ladder 
          if br_minimum <= self.MAX_BR:
            fh.writelines('[id_' + str(j+1) + ':0:nil] --input ' + str(best_res) +'pSource.y4m --crf ' + str(cur_crf) +' --vbv-maxrate ' + str(round(br_minimum,2)) + ' --vbv-bufsize 48000 --strict-cbr -o hevc/out_' + str(j+1) +'.hevc --csv out_' + str(j+1) +'.csv --preset ultrafast' + '\n')
            dict_ladder['Codec'].append(self.codec)
            dict_ladder['ID'].append(j+1)
            dict_ladder['Bitrate'].append(round(br_minimum,2))
            dict_ladder['CRF'].append(cur_crf)
            j += 1
        else:
            fh.writelines('[id_' + str(j+1) + ':0:nil] --input ' + str(best_res) +'pSource.y4m --crf ' + str(cur_crf) +' --vbv-maxrate ' + str(round(br_minimum,2)) + ' --vbv-bufsize 48000 --strict-cbr -o hevc/out_' + str(j+1) +'.hevc --csv out_' + str(j+1) +'.csv --preset ultrafast' + '\n')
            dict_ladder['Codec'].append(self.codec)
            dict_ladder['ID'].append(j+1)
            dict_ladder['Bitrate'].append(round(br_minimum,2))
            dict_ladder['CRF'].append(cur_crf)
            j += 1
            # Loop until the VMAF value reaches 100 - JND or more
            while max_vmaf <= (100 - self.JND):
              max_vmaf = float(max_vmaf) + 6
              # Clip the VMAF value
              if max_vmaf > (100 - self.JND):
                max_vmaf = 100 - self.JND + 0.01 # Added 0.01 to avoid infinite loop while clipping
              test_vector = [self.E_val, self.h_val, self.L_val, max_vmaf]
              br_minimum, best_res, cur_crf = self.get_best_bitrate_model(max_vmaf, test_vector, best_res, cur_crf)
              if br_minimum > self.MAX_BR: # Break if the maximum bitrate is reached
                break
              fh.writelines('[id_' + str(j+1) + ':0:nil] --input ' + str(best_res) +'pSource.y4m --crf ' + str(cur_crf) +' --vbv-maxrate ' + str(round(br_minimum,2)) + ' --vbv-bufsize 48000 --strict-cbr -o hevc/out_' + str(j+1) +'.hevc --csv out_' + str(j+1) +'.csv --preset ultrafast' + '\n')
              dict_ladder['Codec'].append(self.codec)
              dict_ladder['ID'].append(j+1)
              dict_ladder['Bitrate'].append(round(br_minimum,2))
              dict_ladder['CRF'].append(cur_crf)
              j += 1
              
        # Creating a Dataframe object
        df = pd.DataFrame(dict_ladder)
        
        # Generating a .csv file output
        df.to_csv(os.path.join(self.current_directory,self.output_name), index=False)
              
    # Delete unnecessary intermediate output
    def cleanup_files(self):
        csv_file = os.path.join(self.current_directory,'test.csv')
        if os.path.exists(csv_file):
            os.remove(csv_file)
    
    

