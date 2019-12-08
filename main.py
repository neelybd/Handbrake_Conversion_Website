from tkinter import *
from tkinter import filedialog
import os
import shutil
import ntpath
import subprocess
from selection import *
from flask import *


def select_folder_in(dialog):
    print(dialog)
    folder_in = filedialog.askdirectory()
    if not folder_in:
        input("Program Terminated. Press Enter to continue...")
        exit()

    return folder_in


def y_n_question(question):
    while True:
        # Ask question
        answer = input(question)
        answer_cleaned = answer[0].lower()
        if answer_cleaned == 'y' or answer_cleaned == 'n':
            return answer_cleaned
        else:
            print("Invalid input, please try again.")


# List of all video file formats
video_formats = {'.MP4', '.MKV',
                 '.264', '.3G2', '.3GP', '.3GP2', '.3GPP', '.3GPP2', '.3MM', '.3P2', '.60D', '.787', '.890', '.AAF',
                 '.AEC', '.AECAP', '.AEGRAPHIC', '.AEP', '.AEPX', '.AET', '.AETX', '.AJP', '.ALE', '.AM', '.AMC',
                 '.AMV', '.AMX', '.ANIM', '.ANX', '.AQT', '.ARCUT', '.ARF', '.ASF', '.ASX', '.AV', '.AV3', '.AVB',
                 '.AVC', '.AVCHD', '.AVD', '.AVE', '.AVI', '.AVM', '.AVP', '.AVR', '.AVS', '.AVS', '.AVV', '.AWLIVE',
                 '.AXM', '.AXV', '.BDM', '.BDMV', '.BDT2', '.BDT3', '.BIK', '.BIN', '.BIX', '.BLZ', '.BMC', '.BMK',
                 '.BNP', '.BOX', '.BS4', '.BSF', '.BU', '.BVR', '.BYU', '.CAMPROJ', '.CAMREC', '.CAMV', '.CED', '.CEL',
                 '.CINE', '.CIP', '.CLK', '.CLPI', '.CME', '.CMMP', '.CMMTPL', '.CMPROJ', '.CMREC', '.CMV', '.CPI',
                 '.CPVC', '.CREC', '.CST', '.CVC', '.CX3', '.D2V', '.D3V', '.DAD', '.DASH', '.DAT', '.DAV', '.DB2',
                 '.DCE', '.DCK', '.DCR', '.DCR', '.DDAT', '.DIF', '.DIR', '.DIVX', '.DLX', '.DMB', '.DMSD', '.DMSD3D',
                 '.DMSM', '.DMSM3D', '.DMSS', '.DMX', '.DNC', '.DPA', '.DPG', '.DREAM', '.DSY', '.DV', '.DV-AVI',
                 '.DV4', '.DVDMEDIA', '.DVR', '.DVR-MS', '.DVX', '.DXR', '.DZM', '.DZP', '.DZT', '.EDL', '.EVO', '.EVO',
                 '.EXO', '.EXP', '.EYE', '.EYETV', '.EZT', '.F4F', '.F4M', '.F4P', '.F4V', '.FBR', '.FBR', '.FBZ',
                 '.FCARCH', '.FCP', '.FCPROJECT', '.FFD', '.FFM', '.FLC', '.FLH', '.FLI', '.FLIC', '.FLV', '.FLX',
                 '.FPDX', '.FTC', '.FVT', '.G2M', '.G64', '.G64X', '.GCS', '.GFP', '.GIFV', '.GL', '.GOM', '.GRASP',
                 '.GTS', '.GVI', '.GVP', '.GXF', '.H264', '.HDMOV', '.HDV', '.HEVC', '.HKM', '.IFO', '.IMOVIELIBRARY',
                 '.IMOVIEMOBILE', '.IMOVIEPROJ', '.IMOVIEPROJECT', '.INP', '.INT', '.IRCP', '.IRF', '.ISM', '.ISMC',
                 '.ISMCLIP', '.ISMV', '.IVA', '.IVF', '.IVR', '.IVS', '.IZZ', '.IZZY', '.JDR', '.JMV', '.JNR', '.JSS',
                 '.JTS', '.JTV', '.K3G', '.KDENLIVE', '.KMV', '.KTN', '.LREC', '.LRV', '.LSF', '.LSX', '.LVIX', '.M15',
                 '.M1PG', '.M1V', '.M21', '.M21', '.M2A', '.M2P', '.M2T', '.M2TS', '.M2V', '.M4E', '.M4U', '.M4V',
                 '.M75', '.MANI', '.META', '.MGV', '.MJ2', '.MJP', '.MJPEG', '.MJPG', '.MK3D', '.MMV', '.MNV',
                 '.MOB', '.MOD', '.MODD', '.MOFF', '.MOI', '.MOOV', '.MOV', '.MOVIE', '.MOVIE', '.MP21', '.MP21',
                 '.MP2V', '.MP4.INFOVID', '.MP4V', '.MPE', '.MPEG', '.MPEG1', '.MPEG2', '.MPEG4', '.MPF',
                 '.MPG', '.MPG2', '.MPG4', '.MPGINDEX', '.MPL', '.MPL', '.MPLS', '.MPROJ', '.MPSUB', '.MPV', '.MPV2',
                 '.MQV', '.MSDVD', '.MSE', '.MSH', '.MSWMM', '.MT2S', '.MTS', '.MTV', '.MVB', '.MVC', '.MVD', '.MVE',
                 '.MVEX', '.MVP', '.MVP', '.MVY', '.MXF', '.MXV', '.MYS', '.N3R', '.NCOR', '.NFV', '.NSV', '.NTP',
                 '.NUT', '.NUV', '.NVC', '.OGM', '.OGV', '.OGX', '.ORV', '.OSP', '.OTRKEY', '.PAC', '.PAR', '.PDS',
                 '.PGI', '.PHOTOSHOW', '.PIV', '.PJS', '.PLAYLIST', '.PLPROJ', '.PMF', '.PMV', '.PNS', '.PPJ', '.PREL',
                 '.PRO', '.PRO4DVD', '.PRO5DVD', '.PROQC', '.PRPROJ', '.PRTL', '.PSB', '.PSH', '.PSSD', '.PSV', '.PVA',
                 '.PVR', '.PXV', '.PZ', '.QT', '.QTCH', '.QTINDEX', '.QTL', '.QTM', '.QTZ', '.R3D', '.RCD',
                 '.RCPROJECT', '.RCREC', '.RCUT', '.RDB', '.REC', '.RM', '.RMD', '.RMD', '.RMP', '.RMS', '.RMV',
                 '.RMVB', '.ROQ', '.RP', '.RSX', '.RTS', '.RTS', '.RUM', '.RV', '.RVID', '.RVL', '.SAN', '.SBK', '.SBT',
                 '.SBZ', '.SCC', '.SCM', '.SCM', '.SCN', '.SCREENFLOW', '.SDV', '.SEC', '.SEC', '.SEDPRJ', '.SEQ',
                 '.SER', '.SFD', '.SFERA', '.SFVIDCAP', '.SIV', '.SMI', '.SMI', '.SMIL', '.SMK', '.SML', '.SMV',
                 '.SNAGPROJ', '.SPL', '.SQZ', '.SRT', '.SSF', '.SSM', '.STL', '.STR', '.STX', '.SVI', '.SWF', '.SWI',
                 '.SWT', '.TDA3MT', '.TDT', '.TDX', '.THEATER', '.THP', '.TID', '.TIVO', '.TIX', '.TOD', '.TP', '.TP0',
                 '.TPD', '.TPR', '.TREC', '.TRP', '.TS', '.TSP', '.TSV', '.TTXT', '.TVLAYER', '.TVRECORDING', '.TVS',
                 '.TVSHOW', '.USF', '.USM', '.V264', '.VBC', '.VC1', '.VCPF', '.VCR', '.VCV', '.VDO', '.VDR', '.VDX',
                 '.VEG', '.VEM', '.VEP', '.VF', '.VFT', '.VFW', '.VFZ', '.VGZ', '.VID', '.VIDEO', '.VIEWLET', '.VIV',
                 '.VIVO', '.VIX', '.VLAB', '.VMLF', '.VMLT', '.VOB', '.VP3', '.VP6', '.VP7', '.VPJ', '.VR', '.VRO',
                 '.VS4', '.VSE', '.VSP', '.VTT', '.W32', '.WCP', '.WEBM', '.WFSP', '.WGI', '.WLMP', '.WM', '.WMD',
                 '.WMMP', '.WMV', '.WMX', '.WOT', '.WP3', '.WPL', '.WSVE', '.WTV', '.WVE', '.WVM', '.WVX', '.WXP',
                 '.XEJ', '.XEL', '.XESC', '.XFL', '.XLMV', '.XML', '.XMV', '.XVID', '.Y4M', '.YOG', '.YUV', '.ZEG',
                 '.ZM1', '.ZM2', '.ZM3', '.ZMV'}


print("Program: Handbrake Conversion")
print("Release: 0.0.1")
print("Date: 2019-11-10")
print("Author: Brian Neely")
print()
print()
print("This program read the files within a specified folder, converts it based on several factors, and writes "
      "it to a specified location.")
print()
print()

# Find primary input folder
primary_folder = select_folder_in("Primary Folder - Folder where files will be replaced.")

# Get list of all files in folder
print("Getting list of available files...")
primary_files_rel = list()
for (dirpath, dirnames, filenames) in os.walk(primary_folder):
    if len(filenames) != 0:
        for i in filenames:
            # Test if file format is a video format
            file = os.path.join(os.path.relpath(dirpath, primary_folder), i)
            for j in video_formats:
                if file[-len(j):] == str.lower(j):
                    primary_files_rel.append(os.path.join(primary_folder, file))
                    break
print("Found " + str(len(primary_files_rel)) + " files!")

# Handbrake Location
runstr = """"HandBrakeCLI.exe" --preset-import-file "{0}" -Z ""{1}"" -i "{2}" -o "{3}" """

# File Out Extension
file_out_extension = ".mkv"

# Preset Folder
preset_folder = "Presets"

# Select Preset
preset_with_extension = list_selection(os.listdir(preset_folder), "Select Preset for conversion.", "Preset")

# Preset Path
preset_path = ntpath.join(preset_folder, preset_with_extension)

# Preset without Extension
preset, json = os.path.splitext(preset_with_extension)

# File Out Path
file_out_folder = "Out"

# File In
file_in = primary_files_rel[0]

# Get file path without extension
file_out_path, old_extension = os.path.splitext(file_in)

# File Name
file_name = ntpath.basename(file_out_path)

# File Out Path and Name
file_out = ntpath.join(file_out_folder, file_name + file_out_extension)

# Run Handbrake
returncode = subprocess.call(runstr.format(preset_path, preset, file_in, file_out))

