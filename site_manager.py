# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 17:22:59 2016

@author: Brian
"""

import os
import subprocess
import shutil

site_name = "bmer.github.io"
THIS_D = os.path.dirname(os.path.realpath(__file__))

if os.path.basename(THIS_D) != site_name:
    raise StandardError("site_manager should only be run under the directory {}!".format(site_name))

CWD = os.getcwd()
make4ht_support_dir = os.path.join(THIS_D, "make4ht_support")
tex_sources_dir = os.path.join(THIS_D, "tex_sources")

if not os.path.isdir(make4ht_support_dir):
    raise StandardError("No make4ht_support directory detected!")

config_file_path = os.path.join(make4ht_support_dir, "config.cfg")
if not os.path.isfile(config_file_path):
    raise StandardError("No config.cfg file detected!")
    
build_script_path = os.path.join(make4ht_support_dir, "build_script.mk4")
if not os.path.isfile(build_script_path):
    raise StandardError("No build_script.mk4 file detected!")
    
if not os.path.isdir(tex_sources_dir):
    raise StandardError("No tex_sources directory detected!")
    
tex_filepaths = [os.path.join(tex_sources_dir, filepath) for filepath in os.listdir(tex_sources_dir) if filepath.endswith(".tex")]

print "====================================="
print "Found tex_filepaths: "
for tex_filepath in tex_filepaths:
    print tex_filepath
print "====================================="

tex_filenames = [os.path.basename(tex_filepath)[:-4] for tex_filepath in tex_filepaths]

content_dir = os.path.join(THIS_D, "content")
if not os.path.isdir(content_dir):
    os.mkdir(content_dir)

config_file_path_forwardslashes = config_file_path.replace('\\', '/')
build_script_path_forwardslashes = build_script_path.replace('\\', '/')
for tex_filepath, tex_filename in zip(tex_filepaths, tex_filenames):
    output_dir = os.path.join(content_dir, tex_filename)
    
    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)
    os.mkdir(output_dir)
    
    subprocess.call(["make4ht", tex_filepath.replace('\\', '/'), "-c", config_file_path_forwardslashes, "-e", build_script_path_forwardslashes, "-d", output_dir.replace('\\', '/')])

print "====================================="
print "Finding unwanted files..."
unwanted_file_paths = [os.path.join(THIS_D, filepath) for filepath in os.listdir(THIS_D) if filepath.endswith((".log", ".4ct", ".4tc", ".aux", ".css", ".dvi", ".idv", ".lg", ".tmp", ".xref", ".png"))] + [os.path.join(THIS_D, "{}.html".format(tex_filename)) for tex_filename in tex_filenames]

print "Executing clean up..."
for unwanted_file_path in unwanted_file_paths:
    os.remove(unwanted_file_path)
    
print "Done."
    
