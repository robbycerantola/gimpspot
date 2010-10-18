#!/usr/bin/env python
#This is a Gimp plug-in for makeing spot color separation (suitable for screen printing)
#starting from a photo in sRGB format.
#It will reduce first the numbers of the colors accordingly to the custom palette prepared first by the user.
#The color palette has to have the indexed color 0 -> black  color 1 ->white color 2 -> the eventually background
# colour present in the original foto (if it is different from black or white) and than all the colours you think 
#you need to make a good aproximation of the original photo
#
#spot-sparation.py V0.1 by Robby Cerantola for Seritex Arad Romania (c)2010-2011
# robbycerantola@gmail.com
#This is a GNU GPL open source software.
#
# Maximum number of colours -> 10 
# OPTIONS description:
#
#Marks & Bars: put registration marks, color squares to better identify every colour  on the bottom of the separated
#layers plus some text information about filename, colour name (accordingly with names stored in the current palette),
#resolution pixel enlargement factor
#Multiple files : save in the current directory as many black&white files as the colors in the final image,
#usefull to be imported in RIP software for printing or CorelDraw(TM);if not selected it will be saved only one multilayer
#PSD file.  

#Pixel enlargement factor: reduces resolution but not final printing dimension in mm  to get a bigger dot, 
#usefull to get a better silkscreen. Usually a 2 factor is enought, bigger factor come with a bigger loose of details, 
#important is also the starting resolution of the original image. 
#
#TODO Automatic underlayer: (fondino) Makes an extra underlayer for all the separated layers for screen printing a white base to be over printed. 
#TODO Automate palette 
#TODO Delete background from final layers

import math
from gimpfu import *
import os


debug=1        #output some debug information on console
maxnumcol=10   #max number of final colours
maxenlarge=4   #max pixel factor enlargement

def export_layers(img, drw, path, flatten=False,nname=""):
    """Exports layers to separate monochrome tif files by colour name"""
    dupe = img.duplicate()
    for layer in dupe.layers:
        layer.visible = 0
    for layer in dupe.layers:
        layer.visible = 1
        name = nname+"_"+layer.name + ".tif"
        fullpath = os.path.join(path, name);
        tmp = dupe.duplicate()
        if (flatten):  #in CorelDraw we need it Black/white to be coloured afterwards
            tmp.flatten()
            pdb.gimp_image_convert_rgb(tmp)
            pdb.gimp_convert_indexed(tmp,0,3,2,0,0,"fake")
        pdb.gimp_file_save(tmp, tmp.layers[0], fullpath, name)
        dupe.remove_layer(layer)

def export_channels(img, drw, path, flatten=False,nname=""):
    """Exports channels to separate monochrome tif files by colour name"""
    dupe = img.duplicate()
    for layer in dupe.layers:
        layer.visible = 0
    for layer in dupe.layers:
        layer.visible = 1
        name = nname+"_"+layer.name + ".tif"
        fullpath = os.path.join(path, name);
        tmp = dupe.duplicate()
        if (flatten):  #in CorelDraw we need it Black/white to be coloured afterwards
            tmp.flatten()
            pdb.gimp_image_convert_rgb(tmp)
            pdb.gimp_convert_indexed(tmp,0,3,2,0,0,"fake")
        pdb.gimp_file_save(tmp, tmp.layers[0], fullpath, name)
        dupe.remove_layer(layer)

def spot_palette(timg,tdrawable,mode=0,option=False):
    """Prepare palette for spot separation"""
    palette=timg.name
    palette,ext=os.path.splitext(palette)
    palette=pdb.gimp_palette_new(palette)
    if debug:print"Created new palette:%s" % palette
    pdb.gimp_palette_add_entry(palette,"black",(0,0,0))
    pdb.gimp_palette_add_entry(palette,"white",(255,255,255))
    pdb.gimp_palettes_popup("palette_callback","Choose_next_colours",palette)
    
def palette_callback(img,drawable):
    return


def spot_separation(timg, tdrawable,palette="Default",dither=2,transparency=False,marks=False,multiple=False,delback=False,underlayer=False,enlargement=1,chla=0):
    """ spot color separation """
    
    if pdb.gimp_drawable_is_indexed(tdrawable)== True:  #it has to be a RGB image!!
        return 
    #timg.disable_undo()
    #pdb.gimp_image_undo_disable(timg)
    #pdb.gimp_image_undo_freeze(timg)
    width = tdrawable.width
    height = tdrawable.height
    nrcol=pdb.gimp_palette_get_info(palette)
    if enlargement>maxenlarge :
        enlargement=maxenlarge
    if enlargement>1:    #makes a "bigger" pixel
        xres,yres=pdb.gimp_image_get_resolution(timg)
        width=int(width/enlargement)
        height=int(height/enlargement)
        pdb.gimp_image_set_resolution(timg,int(xres/enlargement),int(yres/enlargement))
        tdrawable=pdb.gimp_drawable_transform_scale(tdrawable,0,0,width,height,0,0,0,3,0)
    
	#making room for palette and marks  
    
    nwdrawable=timg.flatten() # flatten all existing layers
    pdb.gimp_context_set_background(pdb.gimp_palette_entry_get_color(palette,2)) # background is the first color in the palette
    pdb.gimp_image_resize(timg,width,height+130,0,0)
    
    pdb.gimp_layer_resize(nwdrawable,width,height+130,0,0)
    
    original_active = timg.active_layer
        
    bartext="Selection of %s colours..." %nrcol
    pdb.gimp_progress_set_text(bartext)	
    
    numlayers,layerids=pdb.gimp_image_get_layers(timg)
    masterlayer=layerids[numlayers-1]
    
    if debug:print "Layer ID is ",masterlayer,layerids    

    if nrcol < maxnumcol: 	
        gimp.progress_init("Separating...")
        pdb.gimp_convert_indexed(timg,dither,4,nrcol,0,0,palette)		
        
        #pdb.gimp_context_set_brush("Circle (19)")
        pdb.gimp_context_set_brush("BigSquare")
        
        #draw some squares coloured in palette colours
        if marks==True:
            xpos=100
            ypos=height+50
            delta=int((width-200)/nrcol)
            if delta > 100:
                delta=100
            for idxcol in range(1,nrcol):
                xpos=xpos+delta
                color=pdb.gimp_palette_entry_get_color(palette,idxcol)	
		
                pdb.gimp_context_set_foreground(color)	
            
                pdb.gimp_paintbrush(nwdrawable,0,2,[xpos,ypos,xpos,ypos],0,0)
                
            
            
                
        pdb.gimp_context_set_foreground(pdb.gimp_palette_entry_get_color(palette,0)) # set black foreground mo make selection black
        pdb.gimp_context_set_background(pdb.gimp_palette_entry_get_color(palette,1))# set white background 
        for idxcol in range(0,nrcol):		
            
            fraction=idxcol*(1.0/nrcol)
            gimp.progress_update(fraction)
            
            timg.active_layer = original_active
            color=pdb.gimp_palette_entry_get_color(palette,idxcol)
            if debug:print timg.active_layer          
            pdb.gimp_by_color_select(nwdrawable,color,0,0,0,0,0,0)           
            
            if chla==1: #create channels instead of layers (experimental)
                if debug:print "Creating new Channel"
                pdb.gimp_selection_invert(timg)
                ch=pdb.gimp_selection_save(timg)
                pdb.gimp_channel_set_opacity(ch,100)
                pdb.gimp_drawable_set_name(ch,pdb.gimp_palette_entry_get_name(palette,idxcol))
            
            else:    # create layers instead of channels
                pdb.gimp_edit_copy(nwdrawable)    #copy&paste way 1/2
                floating=pdb.gimp_edit_paste(nwdrawable,0)       #2/2      
                if multiple==True:
                    pdb.gimp_edit_fill(floating,0)  #fill the current selection with black 
                pdb.gimp_layer_resize_to_image_size(floating) # resize curent layer to the image size
                #floating=pdb.gimp_selection_float(nwdrawable,0,0)       #alternative way 1/1    
                pdb.gimp_floating_sel_to_layer(floating)
            
                #set layer name accordingly the palette colour name (or index)
                layernewname=pdb.gimp_palette_entry_get_name(palette,idxcol)
                if layernewname =="Immagine" or layernewname=="Untitled" :
                    layernewname="Col #"+str(idxcol)
                floating.name=layernewname      
                       
            
        
        if chla==1: # elaborate as channels 
            pass
        
        else:    # elaborate as layers
            #delete old layer when finished
            #pdb.gimp_layer_delete(original_active)
            timg.remove_layer(timg.layers[nrcol])
            
            #for each layer draw crosshair
            if marks==True:
                color=pdb.gimp_palette_entry_get_color(palette,0)	
    		
                pdb.gimp_context_set_foreground(color)	
                pdb.gimp_context_set_brush("CrossHair")
                xpos=50
                
                for curentlayer in timg.layers:
                    #timg.active_layer=curentlayer
                    #draw crosshair
                    
                    
                    pdb.gimp_paintbrush(curentlayer,0,2,[xpos,ypos,xpos,ypos],0,0)
                    pdb.gimp_paintbrush(curentlayer,0,2,[xpos+width-100,ypos,xpos+width-100,ypos],0,0)
                    
                    #draw also some information
                
                for n in range(nrcol):
                    if debug:print"Info", n
                    info=timg.name+" "+timg.layers[n].name+" dot X"+str(enlargement)+" " +str(pdb.gimp_image_get_resolution(timg))+" ppi" 
                    
                    fl=pdb.gimp_text_fontname(timg,timg.layers[n],xpos+100,ypos+50,info,-1,False,20,0,"Sans") 
                                   
                    pdb.gimp_floating_sel_to_layer(fl)
                    
                        
                    for k in range(n):
                        pdb.gimp_image_lower_layer(timg,fl)
                                            
                    pdb.gimp_image_merge_down(timg,fl,0) #merge layers
                
                
                
                
                
            name,ext =os.path.splitext(timg.name)        
            #save multiple black&white files to be separately printed with printer or ripper
            if multiple==True: 
    	        path=os.getcwd()
    	        export_layers(timg,nwdrawable,path,True,name)
    	        
    	        #TODO close current file without saving
    	        
    	        #TODO open every file
    	        
    	    #save one unic multicolor/multilayer file to be worked with CorelDraw for exemple     
            else:    
    	        #back to RGB space because I cannot manage to make PSD indexed file
    	        # to keep trace of layers (maybe it is not possible)!!
    	        
    	        pdb.gimp_image_convert_rgb(timg)
    	        
    	        
    	        filename="separated-"+name+".psd"
    	       
    	        fullpath=os.path.join(os.getcwd(),filename)
    	        if debug:print"Saving ",fullpath            
    	        pdb.gimp_file_save(timg, timg.layers[0], fullpath, filename)
	        
	        
    else:
		if debug:print "Too many colors: can't deal with!!"
		#error : too many colors to do spot separation with
    #timg.enable_undo()
    #pdb.gimp_image_undo_enable(timg)
    #pdb.gimp_image_undo_thaw(timg)

register(
        "Prepare-palette",
        "Prepare custom palette for spot colour separation. Palette name will be the same as image name.",
        "You have to make a custom palette where the first colours have to be black and white, then pick the background colour, then the other you need",
        "Robby Cerantola",
        "Robby Cerantola",
        "2010-2011",
        "<Image>/Spot/_Prepare palette...",
        "RGB*, GRAY*",
        [
                
                (PF_RADIO,"mode","Mode:",0,
                (("Manual",0),
                ("Mode 1",1),
                ("Mode 2",2),
                ("Mode 3",3))),
                (PF_BOOL,   "option", "Option 1", False),
                
                
                
                
        ],
        [],
        spot_palette)       



    
register(
        "Spot-separation",
        "Make a spot color separation using a custom palette",
        "You have to make a custom palette where the first colours have to be black and white, then pick the background colour, then the other you need",
        "Robby Cerantola",
        "Robby Cerantola",
        "2010-2011",
        "<Image>/Spot/_Spot-Separation...",
        "RGB*, GRAY*",
        [
                (PF_PALETTE, "palette", "Palette name:", "Default"),
                (PF_RADIO,"dither","Type of dithering:",2,
                (("None",0),
                ("Floyd-Steinberg",1),
                ("Floyd-Steinberg reduced",2),
                ("Fixed",3))),
                (PF_BOOL,   "transparency", "Dither _Transparency:", False),
                (PF_BOOL,   "marks", "_Marks & bars:", False),
                (PF_BOOL,   "multiple", "Multiple files:", False),
                (PF_BOOL,   "delback","Delete background color:",False),
                (PF_BOOL,   "underlayer", "Automatic underlayer:",False),
                (PF_INT,   "enlargement","Pixel enlargement factor",1),
                (PF_RADIO, "chla","Selection with ",0,
                (("Layers",0),
                ("Channels(experimental)",1)))
                
                
                
        ],
        [],
        spot_separation)
        
register(
        "Palette_callback",
        "Do nothing after being selected a palette",
        "Return from external routine:do nothing",
        "Robby Cerantola",
        "Robby Cerantola",
        "2010-2011",
        "",
        "RGB*, GRAY*",
        [
                
                
                
                
        ],
        [],
        palette_callback)    
        
        

main()


