#!/usr/bin/env python
"""
    Created August 2008
    TablePlotter Class
    Copyright (C) Damien Farrell
 
    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 2
    of the License, or (at your option) any later version.
 
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
 
    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

import sys, os
from Tkinter import *
try:
    import numpy
except:
    print 'you need numpy to do statistics'
try:
    import matplotlib
    matplotlib.use('TkAgg')
    from matplotlib.font_manager import FontProperties
    import pylab
except:
    print 'You need matplotlib to use this feature..'    

class pylabPlotter(object):
    """An interface to matplotlib for general plotting and stats, using tk backend"""
    
    colors = ['#0000A0','#FF0000','#437C17','#AFC7C7','#E9AB17','#7F525D','#F6358A']
    linestyles = ['p','-','--']
    shapes = ['p','-','--',':','.' ,'o','^','<','s','+','x','D','1','4','h'] 
    legend_positions = ['best', 'upper left','upper center','upper right',
                         'center left','center','center right'
                         'lower left','lower center','lower right']    

    graphtypes = ['XY', 'hist', 'bar']
    
    def __init__(self):
        #Setup variables
        self.shape = 'p'
        self.grid = 1 
        self.xscale = 0
        self.yscale = 0
        self.showlegend = 0
        self.legendloc = 'best'
        self.legendlines = []
        self.legendnames = []
        self.graphtype = 'XY'
        self.datacolors = self.colors
        #self.seriesnames = []
        self.setupPlotVars()        
        return

    def plotXY(self, x, y, title='', xlabel=None, ylabel=None, shape=None,
                            clr=None):
        """Do x-y plot of 2 lists"""
        if shape == None:
            shape = self.shape
        if clr == None:
            clr = 'b'
        if self.xscale == 1:
            if self.yscale == 1:
                plotfig = pylab.loglog(x, y, shape, color=clr)
            else:    
                plotfig = pylab.semilogx(x, y, shape, color=clr)    
        elif self.yscale == 1:
            plotfig = pylab.semilogy(x, y, shape, color=clr) 
        else:                    
            plotfig = pylab.plot(x, y, shape, color=clr)      
       
        if self.grid == 1:
            print 'self.grid',self.grid
            pylab.grid(True)
        
        return plotfig

       
    def doHistogram(self, recs, bins=10, title='', xlabel=None, ylabel=None):
        """Do a pylab histogram of a dict with 1 or more lists"""
        dim=int(ceil(len(recs)/2.0))
        i=1
        for r in recs:
            if len(recs[r])==0:
                continue
            pylab.subplot(2,dim,i)
            i=i+1
            histogram = pylab.hist(recs[r],bins=bins)                         
            pylab.title(r)
            pylab.xlabel(xlabel)
            pylab.ylabel(ylabel)        
        return histogram
        
        
    def setData(self, data):
        """Set the current plot data, useful for re-plotting without re-calling 
           explicit functions from the parent"""
         
        self.currdata = data  
        return
    
    def hasData(self):
        """Is there some plot data?""" 
        if hasattr(self, 'currdata') and len(self.currdata) > 0:
            return True
        else:    
            return False

    def setDataSeries(self, names=None):
        """Set the series names, for use in legend"""
        self.dataseriesvars=[]        
        for i in range(1,len(names)):
           s=StringVar()
           s.set(names[i])
           self.dataseriesvars.append(s)
        return
    
    def plotCurrent(self, data=None, format=None):
        """Re-do the plot with the current options and data"""        
        self.applyOptions()
        self.clear()  
        
        if data == None:
            try:
                data = self.currdata
            except:
                print 'no data to plot'
                return
        else:
            self.setData(data)
        
        print 'self.currdata', self.currdata
        
        title = self.plottitle.get()
        xlabel = self.plotxlabel.get()       
        ylabel = self.plotylabel.get()  
        seriesnames = []
        legendlines = []
        for d in self.dataseriesvars:
            seriesnames.append(d.get())
        if format == None:
            #do an X-Y plot, with the first list as X xals 
            if self.graphtype == 'XY':
                import copy
                pdata = copy.deepcopy(data)
                x = pdata[0]
                pdata.remove(x)
                i=0
                for y in pdata:
                    c = self.colors[i]
                    fig = self.plotXY(x, y, clr=c)
                    legendlines.append(fig)
                    i+=1
            
            elif self.graphtype == 'hist':
                self.doHistogram(data, title=title, xlabel=xlabel, ylabel=ylabel)
        elif format == 'ekindata':
            #we have to treat the ekin data properly..
            
            xdata, ydata, fitxdata, fitydata = data
            for d in xdata:                     
                #datalines.append(plt.plot(self.xdata[d],self.ydata[d],shapes[i],color=clr))  
                self.plotXY(xdata[d], ydata[d])
                if fitxdata.has_key(d): 
                    self.plotXY(fitxdata[d],fitydata[d],shape='-')
                    
        pylab.title(title)
        pylab.xlabel(xlabel)
        pylab.ylabel(ylabel)        

        #create legend data
        
        
        if self.showlegend == 1:
            pylab.legend(legendlines,seriesnames,shadow=True,
                         numpoints=1,loc=self.legendloc)
            
        self.show()         
        return        
    
    def clear(self):
        """clear plot"""
        pylab.clf()
        self.legendlines = []
        self.legendnames = []
        return        

    def show(self):
        pylab.show()
        return    

    def showGeneralStats(self):
        #cc = numpy.corrcoef(numpy.array([x,y]))  
        #print 'correlation coeff.:', cc[1,0]           
        return        

    def setOptions(self, shape=None, grid=None, xscale=None, yscale=None,
                    showlegend=None, legendloc=None, graphtype=None):
        """Set the options before plotting"""
        if shape != None:
            self.shape = shape
        if grid != None:
            self.grid = grid
        if xscale != None:
            self.xscale = xscale
        if yscale != None:
            self.yscale = yscale
        if showlegend != None:
            self.showlegend = showlegend
        if legendloc != None:
            self.legendloc = legendloc
        if self.graphtype !=None:
            self.graphtype = graphtype
        return

    def setupPlotVars(self):
        """Plot Vars """
        self.pltgrid = IntVar()
        self.pltlegend = IntVar()
        self.pltsymbol = StringVar()
        self.pltsymbol.set('p')
        self.legendlocvar = StringVar()
        self.legendlocvar.set('best')
        self.xscalevar = IntVar()
        self.yscalevar = IntVar()
        self.xscalevar.set(0)
        self.yscalevar.set(0)
        self.graphtypevar = StringVar()
        self.graphtypevar.set('XY')
        #plot specific
        self.plottitle = StringVar()
        self.plottitle.set('')
        self.plotxlabel = StringVar()
        self.plotxlabel.set('')
        self.plotylabel = StringVar()
        self.plotylabel.set('')
        self.dataseriesvars=[]
        return


    def applyOptions(self):
        """Apply the gui option vars to the plotter options"""
        self.setOptions(shape=self.pltsymbol.get(), grid=self.pltgrid.get(),
               xscale=self.xscalevar.get(), yscale=self.yscalevar.get(),
               showlegend = self.pltlegend.get(),
               legendloc = self.legendlocvar.get(),
               graphtype = self.graphtypevar.get())
        return
            

    def plotSetup(self, data=None):
        """Plot options dialog""" 
        if data != None:
            self.setData(data)
        self.plotprefswin=Toplevel()
        self.plotprefswin.geometry('+300+450')
        self.plotprefswin.title('Plot Preferences')
        row=0
        frame1=LabelFrame(self.plotprefswin, text='General')
        frame1.grid(row=row,column=0,sticky='news',padx=2,pady=2) 
        def close_prefsdialog():
            self.plotprefswin.destroy()    

        def choosecolor(x):
            """Choose color for data series"""
            d=x[0]
            c=x[1] 
            print 'passed', 'd',d, 'c',c
            import tkColorChooser 
            colour,colour_string = tkColorChooser.askcolor(c,parent=self.pylabopts_win)  
            if colour != None:
                self.datacolors[d] = str(colour_string) 
                cbuttons[d].configure(bg=colour_string)

            return
    
        Checkbutton(frame1, text="Grid lines", variable=self.pltgrid,
                    onvalue=1, offvalue=0).grid(row=0,column=0, columnspan=2, sticky='news')
        Checkbutton(frame1, text="Legend", variable=self.pltlegend,
                    onvalue=1, offvalue=0).grid(row=1,column=0, columnspan=2, sticky='news')
      
        Label(frame1,text='Symbol:').grid(row=2,column=0,padx=2,pady=2)
        symbolbutton = Menubutton(frame1,textvariable=self.pltsymbol,
					                relief=GROOVE, width=16, bg='lightblue')          
        symbol_menu = Menu(symbolbutton, tearoff=0)
        symbolbutton['menu'] = symbol_menu        
        for text in self.shapes:
            symbol_menu.add_radiobutton(label=text,
                                            variable=self.pltsymbol,
                                            value=text,
                                            indicatoron=1)  
        symbolbutton.grid(row=2,column=1, sticky='news',padx=2,pady=2)
        row=row+1
        

        Label(frame1,text='Legend pos:').grid(row=3,column=0,padx=2,pady=2)
        legendposbutton = Menubutton(frame1,textvariable=self.legendlocvar,
					                relief=GROOVE, width=16, bg='lightblue')          
        legendpos_menu = Menu(legendposbutton, tearoff=0)
        legendposbutton['menu'] = legendpos_menu 
        i=0
        for p in self.legend_positions:
            print p
            legendpos_menu.add_radiobutton(label=p,
                                        variable=self.legendlocvar,
                                        value=p,
                                        indicatoron=1)  
            i+=1
        legendposbutton.grid(row=3,column=1, sticky='news',padx=2,pady=2)
          
        row=0
        scalesframe = LabelFrame(self.plotprefswin, text="Axes Scales")
        scales={0:'norm',1:'log'}
        for i in range(0,2):
            Radiobutton(scalesframe,text='x-'+scales[i],variable=self.xscalevar,
                            value=i).grid(row=0,column=i,pady=2)
            Radiobutton(scalesframe,text='y-'+scales[i],variable=self.yscalevar,
                            value=i).grid(row=1,column=i,pady=2)
        
        scalesframe.grid(row=row,column=1,sticky='news',padx=2,pady=2)
        
        row=row+1        
        frame=LabelFrame(self.plotprefswin, text='Graph type')
        frame.grid(row=row,column=0,columnspan=2,sticky='news',padx=2,pady=2) 
        for i in range(len(self.graphtypes)):
            Radiobutton(frame,text=self.graphtypes[i],variable=self.graphtypevar,
                            value=i).grid(row=0,column=i,pady=2)        
        row=row+1
        labelsframe = LabelFrame(self.plotprefswin,text='Labels')
        labelsframe.grid(row=row,column=0,columnspan=2,sticky='news',padx=2,pady=2)
        Label(labelsframe,text='Title:').grid(row=0,column=0,padx=2,pady=2)
        Entry(labelsframe,textvariable=self.plottitle,bg='white',relief=GROOVE).grid(row=0,column=1,padx=2,pady=2)
        Label(labelsframe,text='X-axis label:').grid(row=1,column=0,padx=2,pady=2)
        Entry(labelsframe,textvariable=self.plotxlabel,bg='white',relief=GROOVE).grid(row=1,column=1,padx=2,pady=2)
        Label(labelsframe,text='Y-axis label:').grid(row=2,column=0,padx=2,pady=2)
        Entry(labelsframe,textvariable=self.plotylabel,bg='white',relief=GROOVE).grid(row=2,column=1,padx=2,pady=2)

        row=row+1
        
        seriesframe = LabelFrame(self.plotprefswin, text="Data Series Labels")  
        seriesframe.grid(row=row,column=0,columnspan=2,sticky='news',padx=2,pady=2)
        #self.dataseriesvars=[]
        if len(self.dataseriesvars) == 0:
            self.setDataSeries(range(len(self.currdata)))
        c=1                       
        for s in self.dataseriesvars:                               
            Label(seriesframe,text='Series '+str(c)).grid(row=c,column=0,padx=2,pady=2)
            Entry(seriesframe,textvariable=s,bg='white',
                                      relief=GROOVE).grid(row=c,column=1,padx=2,pady=2)
            c+=1

        row=row+1
        cbuttons = {}
        frame = LabelFrame(self.plotprefswin, text="Dataset Colors")        
        for d in range(len(self.dataseriesvars)): 
            c = self.datacolors[d]  
            action = lambda x =(d,c): self.choosecolor(x)
            cbuttons[d]=Button(frame,text=d,bg=c,command=action)
            cbuttons[d].pack(fill=X,padx=2,pady=2)                 
        frame.grid(row=row,column=0,columnspan=2,sticky='news',padx=2,pady=2)
        
        row=row+1
        frame=Frame(self.plotprefswin)
        frame.grid(row=row,column=0,columnspan=2,sticky='news',padx=2,pady=2)   
        b = Button(frame, text="Replot", command=self.plotCurrent, relief=GROOVE, bg='#99ccff')
        b.pack(side=LEFT,fill=X,padx=2,pady=2)
        b = Button(frame, text="Apply", command=self.applyOptions, relief=GROOVE, bg='#99ccff')
        b.pack(side=LEFT,fill=X,padx=2,pady=2)  
        c=Button(frame,text='Close', command=close_prefsdialog, relief=GROOVE, bg='#99ccff')
        c.pack(side=LEFT,fill=X,padx=2,pady=2)
        
        self.plotprefswin.focus_set()
        self.plotprefswin.grab_set()        
        
        return
        