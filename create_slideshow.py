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
    elgain=float(a[20])
    try:
        horgain=float(a[6])
    except:
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
                bgstr="data-background-video=\"%s\" data-background-video-loop data-background-video-muted data-autoslide=\"5000\" "%(m)
            else:
                #                continue
                #data-background-size=\"contain\"
                bgstr="data-background-image=\"%s\" data-autoslide=\"1000\""%(m)
#            
                #           
            #
            #
            transitions=["zoom","fade","slide","convex","concave","zoom"]
            transition=transitions[int(n.floor(n.random.rand(1)*len(transitions))[0])]
            #data-transition=\"zoom\"
            transition="fade"
            o.write("<section data-transition=\"%s\" data-transition-speed=\"fast\" %s ><div data-id=\"box\" style=\"height: 1080px; width:1920px;\"><h1 style=\"margin-top: 0px\">%s</h1><p>%s</p><p style=\"position: fixed; bottom: 0px; left: 0px\">%s</p><p style=\"position: fixed; bottom: 0px; right: 0px\">Horizontal: %1.1f km Vertical: %1.0f m</br>Total horizontal %1.1f km vertical: %1.2f km</p></div></section>\n"%(transition,bgstr,name,desc,datestr,horgain,elgain,total_hor,total_vert/1e3))

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
