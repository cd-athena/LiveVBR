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

# Import necessary libraries
import sys
import subprocess
import os
import argparse
import pandas as pd
import math
import pickle
import ladder_generation

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
    parser.add_argument('--codec', help='Codec name- x265, x264, av1')
    parser.add_argument('--output', help='Output file name with file extension e.g. result.csv')
    
    # Parse the arguments
    args = parser.parse_args()

    # Access the parsed arguments
    input_video = args.video
    input_resolution = args.inputres
    MIN_BR = int(args.minbr)
    MAX_BR = int(args.maxbr)
    JND = int(args.jnd)
    codec = args.codec
    output_filename = args.output

    l_gen = ladder_generation.LadderGenerator(input_video, input_resolution, codec, MIN_BR, MAX_BR, JND, output_filename)
    l_gen.run_vca() # Run VCA on the input video to generate E,h,L features 
    l_gen.generate_features() # Compute the average of E,h,L features for the entire video
    l_gen.load_models() # Load the prediction models as per the corresponding codec
    l_gen.generate_ladder() # Generate the ladder
    l_gen.cleanup_files() # Delete unnecessary  intermediate output files

# Execute the main function
if __name__ == "__main__":
    main()