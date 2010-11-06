Gimp Spot Colour Separation  v 0.2.2  Copyright Robby Cerantola 2010-2011

The program is distributed under the terms of the GNU General Public License.

This is a Gimp Python-Fu plug-in aimed to ease the creation of spot colour separation starting from a RGB image.
The image can be multiple coloured artwork and even a photograph.
It is thinked for screen printers (like the author) who needs positive films for making screens for direct printing.

It is tested with Gimp 2.4 and 2.6 under Linux and Windows but should work on other platforms too.

How to install:
be sure that Python, PyCairo, PyGtk, PyGObject are installed first and than install Gimp
Unpak the source files, copy the brush files SmallCrossHair.gbr  CrossHair12.gbr  BigSquare.vbr to the Gimp brushes directory (usually under user-directory/.gimp-2.6/brushes/ ) and the python plug-in spot-separation.py into the Gimp plug-in directory (usually under user-directory/.gimp-2.6/plug-in/ )
Start Gimp, and when you will load an image, in the menu bar will apear a new item named <Spot>.

How to use:

The very first step is to flatten the image to get rid off every existing layer, selections and channels.
Then you have to create a custom palette by selecting every colour you need in your final print plus the black and white colours. The maximum number of colours is 14 (because there are not automatic printing machines with more tha 14 colours in my knowledge)
There is an option under the Spot menu <Prepare palette> that makes some work for you. At the moment it is in a very early stage, it makes only a palette named the same as the image with the black and white colours picked: you still need to put the rest of the colours by yourself in the new created palette. If you dont know how, you need to read carefully the Gimp manual first and then come back.
You can now run the main routine by selecting from Spot menu the <Spot separation> item. A Python-Fu gui will appear you need to select the Colour Palette : it has to be the palette you prepared before.
The software will than reduce the number of colours to those in your custom palette, creating a separate layer for each colour.


There are also some options, here a brief description:

    Type of dithering:
        
        none: no dithering at all
        Floyd-Steynberg:
        Floyd-Steynberg reduced: produce an image with less colour tones
        Fixed: use fixed typographic dithering
    
    Transparency dithering: 
    
        simulate or not transparencies by dithering.
    
    
    Multiple files: 
        
        not selected > you get a single multilayer file in color saved in the working directory as separated-filename.psd . Useful for preview pourpose, or to be imported with other softwares, CorelDraw (TM) for example.
        
        selected > you get as many files as many colours in your custom palette, ready to be printed on your photo unit, laser or inkjet printer, the goal of the entire plug-in.
         They are black and white tiff files saved in the working directory.
    
    Underlayer:                 (if you don't know what it is for , you are not a screen printer)
                none             do not create any underlayer 
                same dimensions  create an underlayer the same dimension of the sum of all the layers
                bigger           create an underlayer 1 pixel around bigger than the sum of layers
                smaller          same as above but 1 pixel around smaller
    
    
    Delete background:
        
        tryes to guess wich layer is the background layer not needed in the screen printing process (the fabric colour for example) and erase it (sometime deletes the wrong layer, you are warned). It is important when you chose the colours in the custom palette to include any fabric or background colour present in the image ! 
        
    Blocks and marks:
    
        adds some coloured blocks at the bottom of the image to help preparing the right colours pastes for the screen printing process.
        Adds also 2 crosshair for registering pourpose and some other informations on how the separation was done. 

    Pixel enlargement factor  :       VERY IMPORTANT FOR SCREEN PRINTERS
         integer value  1: the resolution of the final layers will be the same of the initial image
                        2 or n , the resolution of the final layers will be 1/2 or 1/n of the initial one.
                                As result, the phisical dimension of the image remains unchanged, while the dot (pixel) dimension will increase, easing the fabrication of the screens , and increasing the covering of the final print. 
                                Do not exagerate with this value or the final print will result very pixeled (Maybe you really  want this effect !!)

    Separate using:
                        layers -> the default way using layers to separate colours
                        channels -> EXPERIMENTAL!! use channels to separate colours, not usable yet !! 

    Working directory: 
         self explanatory.

TODO
    Undo
    Automate colours picking
    Automate previewing process
    Paginate the resulting layers to a single bigger page to be printed on large format inkjet film printers 
    Mirror the layers for transfer printing


THIS SOFTWARE IS PROVIDED "AS IS" AND ANY EXPRESSED OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Feeds back are welcome, send an e-mail to robbycerantola at gmail dot com

06/11/2010





 

