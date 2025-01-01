#!/usr/bin/env python3

import numpy as n
import matplotlib.pyplot as plt
import glob
import csv
import sys
import os
year=-1
if len(sys.argv) > 1:
    year=int(sys.argv[1])
    
o=open("stravashow.html","w")

header="""
<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
 
        <title>reveal.js</title>
 
        <link rel="stylesheet" href="dist/reset.css">
        <link rel="stylesheet" href="dist/reveal.css">
        <link rel="stylesheet" href="dist/theme/black.css">
 
    </head>
    <body>
        <div class="reveal">
          <div class="slides">
                <section data-transition="zoom" data-transition-speed="fast"><h1>Strava</h1></section>
"""
o.write(header)


total_vert=0
total_hor=0
inf=open("activities.csv","r")
inf.readline()
activities = csv.reader(inf, delimiter=',')
for a in activities:
    print(a)
    datestr=a[1]
    amon, aday, ayear, ahour, ampm=datestr.split(" ")
    print(year)
    this_year=int(ayear[0:4])
    if year != -1:
        if this_year != year:
            print("skipping")
            continue
    name=a[2]
    desc=a[4]
    try:
        elgain=float(a[20])
        horgain=float(a[6])
    except:
        print("no elgain or horgain")
        elgain=0
        horgain=0
    print(elgain)
    total_vert+=elgain
    total_hor+=horgain    
#    desc=a[4]
    media=a[len(a)-1].split("|")
    if len(media)>0:
        for m in media:
            print(m)
            if len(m) == 0:
                continue
            if os.path.exists(m) != True:
                print("missing media file %s"%(m))
                continue
            bgstr=""
            if m[-4:] == ".mp4":
                import shlex
                from subprocess import Popen, PIPE
#args = shlex.split('sudo /usr/bin/atq')
                cmdlist=shlex.split("ffprobe -v error -select_streams v:0 -show_entries stream=duration -of default=noprint_wrappers=1:nokey=1 %s"%(m))
           
                prc = Popen(cmdlist, stdout=PIPE, stderr=PIPE)
                output, stderr = prc.communicate()
                video_dur=float(output.strip())
                print("dur",video_dur)
                bgstr="data-background-video=\"%s\" data-background-video-loop data-background-video data-autoslide=\"%d\" "%(m,int(n.floor(video_dur*1000)))
            else:
                #                continue
                #data-background-size=\"contain\"
                bgstr="data-background-image=\"%s\" data-autoslide=\"2000\""%(m)
#            
                #           
            #
            #
            transitions=["zoom","fade","slide","convex","concave","zoom"]
            transition=transitions[int(n.floor(n.random.rand(1)*len(transitions))[0])]
            #data-transition=\"zoom\"
            transition="fade"
            o.write("<section data-transition=\"%s\" data-transition-speed=\"fast\" %s ><div data-id=\"box\" style=\"height: 1080px; width:1920px;\"><h1 style=\"margin-top: 0px; text-shadow: -1px 0 1px black, 0 1px 1px black, 1px 0 1px black, 0 -1px 1px black\">%s</h1><p style=\"text-shadow: -1px 0 1px black, 0 1px 1px black, 1px 0 1px black, 0 -1px 1px black\">%s</p><p style=\"position: fixed; bottom: 0px; left: 0px; text-shadow: -1px 0 1px black, 0 1px 1px black, 1px 0 1px black, 0 -1px 1px black\">%s</p><p style=\"position: fixed; bottom: 0px; right: 0px; text-shadow: -1px 0 1px black, 0 1px 1px black, 1px 0 1px black, 0 -1px 1px black\">Hor / vert: %1.1f km / %1.0f m Season total: %1.1f km / %1.2f km</p></div></section>\n"%(transition,bgstr,name,desc,datestr,horgain,elgain,total_hor,total_vert/1e3))

footer="""
            </div>
        </div>
 
        <script src="dist/reveal.js"></script>      
        <script>
            // More info about initialization & config:
            // - https://revealjs.com/initialization/
            // - https://revealjs.com/config/
            Reveal.initialize({
                hash: true,
autoSlideStoppable: false,
                 controls: false,
                 autoSlide: 1000,
                 loop: true,
                 width: 1920,
                 height: 1080
 
            });
        </script>
    </body>
</html>

"""
    
o.write(footer)
o.close()
