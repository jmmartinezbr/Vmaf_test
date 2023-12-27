import os
import json

#lista_de_videos = [['video.mp4','mezanino.mxf']]
#insert video list in lista_de_videos

lista_de_videos = [["video.mp4","mezanine.mxf"]]

def ffprobe_json(video):
    comando = "ffprobe -v quiet -print_format json -show_format -show_streams {fname} > {fname}.json".format(fname=video)
    os.system(comando)
    return

def vmaf(video,mezanino,vlargura,valtura,modelo): #Function that aplies vmaf test autoscaling videos below mezanino's resolution
    comando = '''ffmpeg -i {videoin} -i {original} -lavfi "[0:v]scale={vlargura}x{valtura}[main];[main][1:v]libvmaf=model='path={model}':log_path=vamf_{videoin}.json " -f null -'''.format(videoin=video,original=mezanino,model=modelo,vlargura=vlargura,valtura=valtura)
    os.system(comando)
    return

def main(video,mezanino):
    model=""

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

    vmaf(video,mezanino,mezanino_width,mezanino_height,model)

    return


for v in lista_de_videos:
    main(v[0],v[1])
