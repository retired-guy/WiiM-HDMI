#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import os
from datetime import datetime
import json
import requests
import xmltodict
import upnpclient
from tkinter import *
from PIL import ImageTk,Image,ImageFont,ImageDraw
from random import randrange
from threading import Thread

####################################################################
#### Change the ip address to that of your WiiM Mini
dev = upnpclient.Device("http://192.168.68.112:49152/description.xml")
####################################################################

ws = Tk()
ws.title('WiiM Office')
ws.attributes("-fullscreen",True)
ws.config(bg='#000000')

screenwidth = ws.winfo_screenwidth()
screenheight = ws.winfo_screenheight()
fontsize = screenheight // 20
fontname = "Helvetica"

bgcolor = "#451f0c"
ON = 1
OFF = 0

time_lbl = Label(
    ws,
    text=time.strftime( "%d/%m/%Y %A %H:%M"),
    anchor="w",
    font=(fontname,fontsize),
    padx=10,
    pady=5,
    bg=bgcolor,
    fg='#ffffff'
    )

time_lbl.grid(row=4,column=0,sticky="nwes")

progress_lbl = Label(
    ws,
    text="",
    anchor="e",
    font=(fontname,fontsize),
    padx=10,
    pady=5,
    bg=bgcolor,
    fg='#ffffff'
    )

progress_lbl.grid(row=4,column=1,sticky="nwes")

title_lbl = Label(
    ws,
    text="",
    anchor="w",
    padx=10,
    pady=5,
    font=(fontname,fontsize),
    bg=bgcolor,
    fg='#ffffff'
    )

title_lbl.grid(row=0,column=0,columnspan=2,sticky="ew",padx=0,pady=0)

artist_lbl = Label(
    ws,
    text="",
    anchor="nw",
    wraplength=screenwidth // 2,
    justify="left",
    padx=10,
    pady=10,
    font=(fontname,fontsize),
    bg='#000000',
    fg='#ffffff'
    )

artist_lbl.grid(row=1,column=1,sticky="news")

album_lbl = Label(
    ws,
    text="",
    anchor="nw",
    wraplength=screenwidth // 2,
    justify="left",
    padx=10,
    pady=10,
    font=(fontname,fontsize),
    bg='#000000',
    fg='#ffffff'
    )

album_lbl.grid(row=2,column=1,sticky="news")


meta_lbl = Label(
    ws,
    text="",
    anchor="sw",
    padx=10,
    pady=10,
    font=(fontname,fontsize),
    bg='#000000',
    fg='#ffffff'
    )

meta_lbl.grid(row=3,column=1,sticky="news")

art_lbl = Label(
    ws,
    image=None
    )

art_lbl.grid(row=1,column=0,rowspan=3,sticky=W+N,padx=0,pady=0)

ws.columnconfigure(1, weight=2)

def screen(flag):
    if flag == ON:
        os.system("xset dpms force on")
    else:
        os.system("xset dpms force standby")

def get_nowplaying():

    w = ws.winfo_width()
    h = ws.winfo_height()
    lh = title_lbl.winfo_height()
    old_title = ""
    cleared = False

    while True:
        time.sleep(1)
        try:

            time_text=time.strftime("%a, %d %b %Y    %H:%M")
            obj = dev.AVTransport.GetInfoEx(InstanceID='0')
            transportstate = obj['CurrentTransportState']
            
            if transportstate != 'PLAYING':
                if not cleared:
                    if transportstate not in ['PLAYING','TRANSITIONING']:
                        screen(OFF)
                        cleared = True
                    
                continue

            if cleared:
                if transportstate == 'PLAYING':
                    screen(ON)
                    cleared = False


            time_lbl.config(text=time_text)
            try:
                duration = obj['TrackDuration'][3:]
                reltime = obj['RelTime'][3:]
                progress = f"{reltime}/{duration}"
            except:
                progress = "" 

            progress_lbl.config(text=progress)

            meta = obj['TrackMetaData']
            data = xmltodict.parse(meta)["DIDL-Lite"]["item"]
            title = data['dc:title'][:50]
            if title != old_title:
                    
                try:
                    artist = data['upnp:artist'][:100]
                except:
                    artist = ""

                try:
                    quality = int(data['song:quality'])
                except:
                    quality = 0

                try:
                    actualQuality = data['song:actualQuality']
                    mediatype = "FLAC"
                except:
                    actualQuality = ""

                try:
                    rate = int(data['song:rate_hz'])/1000.0
                except:
                    rate = 0

                try:
                    depth = int(data['song:format_s'])
                    if actualQuality == "HD":
                      depth = 16
                    if depth > 24:
                      depth = 24
                except:
                    depth = 0


                try:
                    title = data['dc:title'][:50]
                except:
                    title = ""

                try:
                    album = data['upnp:album'][:100]
                except:
                    album = ""

                if album == "":
                    try:
                      album = data['dc:subtitle'][:100]
                    except:
                      pass

                try:
                    mediatype = data['upnp:mediatype'].upper()
                except:
                    if quality > 1 or len(actualQuality) > 0 :
                      mediatype = "FLAC"
                    else:
                      mediatype = ""

                try:
                    br= int(data['song:bitrate']) 
                    bitrate = f"{br} kbps"
                except Exception as e:
                    print(e)
                    bitrate = ""

                try:
                  arttmp = data["upnp:albumArtURI"]
                  if isinstance(arttmp, dict):
                    arturl = arttmp["#text"]
                  else:
                    arturl = arttmp
                except:
                    arturl = ""
                    

                old_title = title
                metatext = f"{depth} bits / {rate} kHz {bitrate}"
                title_lbl.config(text=title) 
                artist_lbl.config(text=artist)
                album_lbl.config(text=album)
                meta_lbl.config(text=metatext)
                
                try:
                    image = Image.open(requests.get(arturl,stream=True).raw)
                    image = image.resize((screenheight-(lh*2),screenheight-(lh*2)))
                    img = ImageTk.PhotoImage(image)
                    art_lbl.config(image=img)
                except Exception as e:
                    print(e)
                    pass
                
        except Exception as e:
            print(e)

        ws.update()



thread = Thread(target=get_nowplaying)
thread.daemon = True             
thread.start()


ws.mainloop()

