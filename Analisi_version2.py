#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import matplotlib as plt
import matplotlib.pyplot as plt
import pandas as pd
from scipy.integrate import simps
from matplotlib.offsetbox import AnchoredText


# In[ ]:


def take_plot_N2(nome_file,x_min, x_max, y_min, y_max):
    
    nome_campione_N2 = pd.read_excel(nome_file+'//'+ nome_file +'_N2@LN2.xlsx', 
                       header = 0, 
                       engine ='openpyxl', 
                       usecols="L:O", 
                       skiprows = range(30), 
                       nrows = 50)
    nome_campione_N2 = nome_campione_N2.rename(columns = {'Quantity Adsorbed (cm³/g STP).1': 'Desorbtion',
                                  'Quantity Adsorbed (cm³/g STP)': 'Adsorbtion'})
    colonne_N2 = nome_campione_N2.columns

    subplot_N2 = nome_campione_N2.plot(
        x = colonne_N2[0], 
        y = colonne_N2[1], 
        kind = 'line', 
        lw=2, 
        colormap='gnuplot', 
        marker='.', 
        markersize = 20,
       
        
    
    )
    nome_campione_N2.plot(
        x = colonne_N2[2], 
        y = colonne_N2[3], 
        kind = 'line', 
        lw=2,
        ax = subplot_N2,
        colormap = 'gist_rainbow', 
        marker='.', 
        xlim = (x_min,x_max),
        ylim = (y_min,y_max),
        markersize = 20,
        figsize = (20, 11),
        fontsize = 20
    )
    plt.legend(loc ='lower right', fontsize = 20 )
    plt.xlabel(colonne_N2[0], fontsize = 20)
    plt.ylabel('Quantity Adsorbed (cm³/g STP)', fontsize = 20)
    plt.title(nome_file, fontsize = 20)
    
    
    
    tempN = AnchoredText('N2@LN2', prop = dict(size=20), frameon = True, loc = 'upper left')
    tempN.patch.set_boxstyle('round, pad=0.,rounding_size=0.2')
    subplot_N2.add_artist(tempN)
    
    plt.grid(True,linewidth=0.5, linestyle='-')
    
    plt.savefig(nome_file+'//'+'Grafici'+'//'+nome_file + '_N2.jpeg', transparent = False)
    
    nome_campione_N2.to_csv(nome_file+'//'+nome_file +'_SAIEUS.txt', columns=[colonne_N2[0], colonne_N2[1]], header = False, sep = '\t', index = False)
    nome_campione_N2.to_csv(nome_file+'//'+nome_file +'_SAIEUS.txt', columns=[colonne_N2[2], colonne_N2[3]], header = False, mode = 'a', sep = '\t', index = False)
    
    dataframe = nome_campione_N2[ [colonne_N2[0], colonne_N2[1]] ].copy()
    dataframe = dataframe.rename(columns = {colonne_N2[1]: nome_file+'_N2'})
    
    return dataframe 
    
    


# In[ ]:


def take_plot_H2(nome_file, dataframe, x_min, x_max, y_min,y_max):
    nome_campione_H2 = pd.read_excel(nome_file+'//'+nome_file +'_H2@LN2(gmol).xlsx', 
                                     header = 0, 
                                     engine ='openpyxl', 
                                     usecols="L:O", 
                                     skiprows = range(30), 
                                     nrows = 33)
    nome_campione_H2 = nome_campione_H2.rename(columns = {'Quantity Adsorbed (mmol/g)': 'Adsorbtion', 
                                                          'Quantity Adsorbed (mmol/g).1': 'Desorbtion'})
    colonne_H2 = nome_campione_H2.columns
    nome_campione_H2[colonne_H2[1]] = nome_campione_H2[colonne_H2[1]]*2/10 #2/10 per trasformare wt%
    nome_campione_H2[colonne_H2[3]] = nome_campione_H2[colonne_H2[3]]*2/10
    subplot_H2 = nome_campione_H2.plot(
        x = colonne_H2[0], 
        y = colonne_H2[1], 
        kind = 'line', 
        lw=2, 
        colormap='gnuplot', 
        marker='.', 
        markersize = 20)
    nome_campione_H2.plot(
        x = colonne_H2[2], 
        y = colonne_H2[3], 
        kind = 'line', 
        lw=2,
        ax = subplot_H2,
        colormap = 'gist_rainbow', 
        marker='.', 
        markersize = 20,
        xlim = (x_min,x_max),
        ylim = (y_min,y_max),
        figsize = (20, 11),
        fontsize = 20    )
    plt.legend(loc ='lower right', fontsize = 20 )
    plt.xlabel(colonne_H2[0], fontsize = 20)
    plt.ylabel('Quantity Adsorbed (Wt%)', fontsize = 20)
    plt.title(nome_file, fontsize = 20)
    tempH = AnchoredText('H2@LN2', prop = dict(size=20), frameon = True, loc = 'upper left')
    tempH.patch.set_boxstyle('round, pad=0.,rounding_size=0.2')
    subplot_H2.add_artist(tempH)        
    plt.grid(True,linewidth=0.5, linestyle='-')
    plt.savefig(nome_file+'//'+'Grafici'+'//'+nome_file + '_H2.jpeg', transparent = False)
     #array_idrogeno = nome_campione_H2[ [colonne_H2[0], colonne_H2[1]] ].to_numpy()
    dataframe_H2 = nome_campione_H2[ [colonne_H2[0], colonne_H2[1]] ].copy()
    dataframe_H2 = dataframe_H2.rename(columns = {colonne_H2[1]: nome_file+'_H2'})
 
    dataframe = dataframe.merge(dataframe_H2, left_index=True, right_index=True)
    
    return dataframe
    


# In[ ]:


def istogramma(porus_campione,colonne_pori, nome_file):
    #classifichiamo il diametro dei pori in nanometri
    macropori = 50 # maggiori di 50 nanometri
    mesopori = 2 # compresi fra 2 e 50 nanometri
    micropori = 0.7 # sono i pori compresi tra 0,7 e 2 nanometri
    ultramicropori = 0 # sono i pori minori di 0,7 nanometri
    
    ultra = porus_campione.loc[ porus_campione[colonne_pori[0]] <= 0.7, [colonne_pori[0],colonne_pori[1], colonne_pori[2]] ]
    micro = porus_campione.loc[ (porus_campione[colonne_pori[0]] > 0.7) & (porus_campione[colonne_pori[0]] <= 2) , [colonne_pori[0],colonne_pori[1], colonne_pori[2]] ]
    meso = porus_campione.loc[ (porus_campione[colonne_pori[0]] > 2) & (porus_campione[colonne_pori[0]] <= 50) , [colonne_pori[0],colonne_pori[1], colonne_pori[2]] ]
    macro = porus_campione.loc[ porus_campione[colonne_pori[0]] > 50 , [colonne_pori[0],colonne_pori[1], colonne_pori[2]] ]
    
    ultra_np = ultra.to_numpy()
    micro_np = micro.to_numpy()
    meso_np = meso.to_numpy()
    macro_np = macro.to_numpy()

    area_ultra = simps(ultra_np[:,1], ultra_np[:,0])
    area_micro = simps(micro_np[:,1], micro_np[:,0])
    area_meso = simps(meso_np[:,1], meso_np[:,0])
    area_macro = np.trapz(macro_np[:,1], macro_np[:,0])
    tot = area_macro+area_micro+area_meso+area_ultra
    #print('Volume cumulativo=',area_macro+area_micro+area_meso+area_ultra, 'cc/g')

    istogramma = pd.DataFrame([ ['<0.7 (nm)','ultra-\n microporous', area_ultra], ['0.7-2 (nm)','super-\n microporous', area_micro], ['2-50 (nm)','mesoporous', area_meso], ['-','total', tot] ], 
                          columns = ['Range pore width', 'denomination', 'cumulative volume (cm³/g)'] )
    istogramma = istogramma.set_index('Range pore width')
    print(istogramma)

    istogramma.plot(x = 'denomination' ,
                    y = 'cumulative volume (cm³/g)', 
                    kind = 'bar',
                    legend = False,
                    figsize = (12, 5),
                    ylim = (0, tot+tot/5),
                    fontsize = 15       )
    plt.grid(True, linewidth=0.5, linestyle='-')
    plt.ylabel('Cumulative volume (cm³/g)',fontsize = 15, fontweight ='bold')
    plt.xlabel('Porosity', fontsize = 15, fontweight ='bold')
    plt.title(nome_file, fontsize = 20)
    
    
    plt.xticks(rotation='horizontal')
    plt.savefig(nome_file+'//'+'Grafici'+'//'+nome_file + '_ist.jpeg', transparent = False) 
    #plt.yscale('log')  
    istogramma = istogramma.rename(columns = {'cumulative volume (cm³/g)': nome_file})
    return istogramma   


# In[ ]:


def porus_sample(nome_file, intervallo):
    porus_campione = pd.read_csv(nome_file+'//'+nome_file +'_porus.csv', 
                            sep = ';', 
                            header = 0,
                            usecols = [7,8,9,10,11,14,15,16],
                            decimal = ',')    
    porus_campione = porus_campione.rename(columns = {'w': 'Pore width (nm)','dV/dw': 'Pore Size Distribution (cm³/g/nm)', 'V cum': ' Cumulative Volume (cm³/g)'})
    colonne_pori = porus_campione.columns
    porus_campione[colonne_pori[0]] = porus_campione[colonne_pori[0]]/10
    porus_campione[colonne_pori[1]] = porus_campione[colonne_pori[1]]*10
    
    
    y_max_psd = np.amax( porus_campione[colonne_pori[1]].to_numpy() )
    y_max_vol = np.amax( porus_campione[colonne_pori[2]].to_numpy() )
    
    
    
    #print(porus_campione)
    subplot = porus_campione.plot(x = colonne_pori[0], 
                        y = colonne_pori[1], 
                        kind = 'line', 
                        lw = 2,
                        color = 'r', 
                        ylim = (0,y_max_psd+y_max_psd*0.2),
                        fontsize = 20 , 
                        ##marker='.', 
                        #markersize = 20, 
                        legend = False
                       )
    subplot_o = subplot.twinx()
    
    porus_campione.plot(x = colonne_pori[0], 
                        y = colonne_pori[2],
                        kind = 'line', 
                        lw = 2,
                        color = 'b', 
                        
                        ax = subplot_o, 
                        xlim = (0.35, intervallo),
                        ylim = (0,y_max_vol+y_max_vol*0.1),
                        xticks = porus_campione.index*2,                
                        figsize = (20, 11),
                        legend = False,
                        fontsize = 20    )
    subplot.set_ylabel(colonne_pori[1], fontsize = 20, color = 'r')
    subplot.set_xlabel(colonne_pori[0], fontsize = 20)
    plt.xscale('log')
    plt.xlabel(colonne_pori[0], fontsize = 20)
    plt.ylabel(colonne_pori[2], fontsize = 20, color = 'b')
    plt.title(nome_file, fontsize = 20)
    subplot.grid(True, linewidth=0.5, linestyle='-')  
    plt.savefig(nome_file+'//'+'Grafici'+'//'+nome_file + '_porus.jpeg', transparent = False)
    
    df_ist = istogramma(porus_campione, colonne_pori, nome_file)
    return df_ist


# In[ ]:


def sovrapponi(*array, idrogeno, nome_grafico, x_min, x_max, y_min,y_max): #nome grafico deve essere una stringa
    if bool(idrogeno) == False:
        for x in array:
            ax = plt.gca()
            nome_old = x.columns[1]
            nome_new = nome_old[0 : len(nome_old) - 3]
            x = x.rename( columns = { nome_old : nome_new})
            x.plot(x = x.columns[0] ,
                   y = x.columns[1], 
                   kind = 'line',
                   lw=2, 
                   marker='.', 
                   ax = ax,
                   markersize = 20,
                   xlim = (x_min,x_max),
                   ylim = (y_min,y_max),
                   figsize = (20, 11),
                   fontsize = 20   )
        plt.title("N$_2$@LN$_2$",fontsize = 20)
        plt.xlabel("Relative pressure ($p/p^0$)",fontsize=20)
        plt.ylabel("Quantity Adsorbed (cm³/g STP)",fontsize = 20)
        plt.grid(True, linewidth=0.5, linestyle='-')
        plt.legend(loc = 'upper left', fontsize = 15,) #bbox_to_anchor=(1,0.8))
        plt.savefig('Sovrapposizioni//' + nome_grafico +'_N2.jpeg', transparent = False)
        #plt.show()
        
            
    else:
        for x in array:
            ax = plt.gca()
            nome_old = x.columns[3]
            nome_new = nome_old[0 : len(nome_old) - 3]
            x = x.rename( columns = { nome_old : nome_new})
            x.plot(x = x.columns[2] ,
                   y = x.columns[3], 
                   kind = 'line',
                   lw = 2, 
                   marker='.', 
                   xlim = (x_min,x_max),
                   ylim = (y_min,y_max),
                   ax = ax,
                   markersize = 20,
                   
                   figsize = (20, 11),
                   fontsize = 20   )
        plt.title("H$_2$@LN$_2$", fontsize = 20)
        plt.xlabel("Relative pressure ($p/p^0$)",fontsize=20)
        plt.ylabel("Quantity Adsorbed (Wt%)",fontsize = 20)
        plt.grid(True, linewidth=0.5, linestyle='-')
        plt.legend(loc = 'upper left', fontsize = 15)
        plt.savefig('Sovrapposizioni//' + nome_grafico + '_H2.jpeg', transparent = False)
        #plt.show()
        


# In[ ]:


def total_ist(*df_porus, y_max):
    
    i = 0
    barWidth = 0.45
    
    for x in df_porus:
        if i == 0:
            dataframe = x.copy()
        else:
            dataframe_2 = x.copy()
            dataframe = pd.merge(dataframe, dataframe_2, how="right", on = ['denomination'])
        i = i + 1
    
    x_ticks = dataframe[['denomination']].to_numpy()
    #print(x_ticks)
   
    dataframe.plot(kind="bar",
                   figsize=(20,11),
                   width = barWidth,
                   fontsize = 20,
                  ylim = (0,y_max))
    plt.grid(True, linewidth=0.5, linestyle='-')
   
    plt.xlabel('Porosity', fontweight ='bold', fontsize = 20)
    plt.ylabel('Cumulative Volume (cm³/g)', fontweight ='bold', fontsize = 20)
    plt.xticks( [ r for r in range(len(x_ticks)) ], ['ultra-microporous', 'super-microporous', 'mesoporous', 'total'], rotation='horizontal')
    plt.legend(loc = 'upper left', fontsize = 15)
    plt.savefig('Sovrapposizioni//'+'istogramma.jpeg', transparent = False)
    
    
    


# In[ ]:


def plot_pyrolisis(nome_pir, xmin, xmax, freq):
    log_pirolisi = pd.read_csv('log_pirolysis//'+ nome_pir +'.csv', 
                            sep = '\t', 
                            header = None,
                            usecols = [1,2,3,4],
                            decimal = ',')
    log_pirolisi = log_pirolisi.rename(columns = { 1: 'Time (Min)', 2 : 'Temp_Teor (°C)', 3: 'Temp (°C)', 4: '$\Delta T$'})
    colonne_log = log_pirolisi.columns
    log_pirolisi[colonne_log[0]] = log_pirolisi[colonne_log[0]]/60
    log_pirolisi = log_pirolisi.loc[ (log_pirolisi[colonne_log[0]] > xmin) & (log_pirolisi[colonne_log[0]] <= xmax) , [colonne_log[0],colonne_log[1], colonne_log[2], colonne_log[3]] ]

    
    
    #print(log_pirolisi)
    
    subplot = log_pirolisi.plot(x = colonne_log[0], 
                        y = colonne_log[1], 
                        kind = 'line', 
                        lw = 2,
                        color = 'r', 
                        )
    
    log_pirolisi.plot(x = colonne_log[0], 
                        y = colonne_log[2],
                        marker = '.', 
                        color = 'b', 
                        ax = subplot, 
                        xlim = (xmin, xmax),
                        figsize = (20, 11),
                        legend = True,
                        fontsize = 20    )
    
    subplot.set_ylabel(colonne_log[1], fontsize = 20)
    subplot.set_xlabel(colonne_log[0], fontsize = 20)
    plt.xlabel(colonne_log[0], fontsize = 20)
    plt.ylabel(colonne_log[2], fontsize = 20)
    plt.xticks(np.arange(xmin, xmax, freq))
    plt.legend(fontsize = 20, loc = 'best')
    subplot.grid(True, linewidth=0.5, linestyle='-')  
    plt.savefig( 'log_pirolysis//'+ nome_pir + '.jpeg', transparent = False)
    
    


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




