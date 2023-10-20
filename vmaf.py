import os
import json

#lista_de_videos = [['video.mp4','mezanino.mxf']]
lista_de_videos = [['tk014214-v6-trecho-mxf-2023-04-04_17-08-47_h264_288_240000.mp4','TK014214_v6_trecho.mxf'],
['tk014214-v6-trecho-mxf-2023-04-04_17-08-47_h264_360_374137.mp4','TK014214_v6_trecho.mxf'],
['tk014214-v6-trecho-mxf-2023-04-04_17-08-47_h264_576_710860.mp4','TK014214_v6_trecho.mxf'],
['tk014214-v6-trecho-mxf-2023-04-04_17-08-47_h264_1080_3905402.mp4','TK014214_v6_trecho.mxf'],
['tk014214-v6-trecho-mxf-2023-04-04_17-08-47_h264_900_1350634.mp4','TK014214_v6_trecho.mxf'],
['tk014214-v6-trecho-mxf-2023-04-04_17-08-47_h264_900_2566204.mp4','TK014214_v6_trecho.mxf'],
['tk014214-v6-trecho-mxf-2023-04-04_17-08-47_h264_1080_5943474.mp4','TK014214_v6_trecho.mxf']]

def ffprobe_json(video):
    comando = "ffprobe -v quiet -print_format json -show_format -show_streams {fname} > {fname}.json".format(fname=video)
    os.system(comando)
    return

def video_upscale(video,altura,largura,codec):
    if altura==2160:
        up="4k"
    elif altura==1080:
        up="hd"
    comando = "ffmpeg -i {fname} -vf scale={vlargura}x{valtura} -c:v {codec_lib} {fname}_{valtura}.mp4".format(fname=video,vlargura=largura,valtura=altura,codec_lib=codec)
    os.system(comando)
    return

def vmaf(video,mezanino,modelo):
    comando = '''ffmpeg -i {videoin} -i {original} -lavfi libvmaf="model_path='C\:\\\\FFmpeg\\\\bin\\\\{model}':log_path=vmaf_{videoin}.json" -f null - '''.format(videoin=video,original=mezanino,model=modelo)
    os.system(comando)
    return

def main(video,mezanino):
    model=""
    codec_lib = ""

    ffprobe_json(video)
    ffprobe_json(mezanino)

    with open(mezanino+".json") as f:
        datam = f.read()
    parsed_json_mezanino = json.loads(datam)
    mezanino_width = parsed_json_mezanino['streams'][0]['width']
    mezanino_height = parsed_json_mezanino['streams'][0]['height']
        
    if mezanino_height == 2160:
        model="vmaf_4k_v0.6.1.json"
    elif mezanino_height == 1080:
        model="vmaf_v0.6.1.json"

    with open(video+".json") as file:
        datav = file.read()
    parsed_json_video = json.loads(datav)
    video_width = parsed_json_video['streams'][0]['width']
    video_height = parsed_json_video['streams'][0]['height']
    video_formato = parsed_json_video['streams'][0]['codec_name']
    if video_formato == 'hevc':
        codec_lib = "libx265"
    elif video_formato == 'h264':
        codec_lib = "libx264"


    if video_height == mezanino_height:
       vmaf(video,mezanino,model)
    else:
       video_upscale(video,mezanino_height,mezanino_width,codec_lib)
       vmaf(video+"_{h}.mp4".format(h=mezanino_height),mezanino,model)
    return



for v in lista_de_videos:
    main(v[0],v[1])



