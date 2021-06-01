# Module pour l'activité de détection de contours
# (C) www.python-lycee.com


from ipywidgets import interact
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
from io import BytesIO
import requests

def Application_Filtre_image(Nom_Filtre,url):
    
    #ouverture de l'image originale
    im_originale = Image.open(BytesIO(requests.get(url).content))
    
    # récupération des dimensions de l'image originale
    L,H = im_originale.size
    
    # création d'une image vierge, de même format et même dimension que l'image initiale
    im_modifiee = Image.new( mode=im_originale.mode , size=(L,H) )
    
    # ouverture de l'accès aux pixels des deux images 
    pix_origine = im_originale.load()
    pix_modifie = im_modifiee.load()
    
    # on parcourt tous les pixels des images (sauf les bords)
    for x in range(1,L-1):
        for y in range(1,H-1):
            intensite_origine  = pix_origine[x,y][0] #récupération de la composante R du pixel original considérée comme intensité
            # Calcul de la nouvelle intensité avec le filtre (ordre NW,N,NE,W,C,E,SW,S,SE)
            intensite_modifiee = Nom_Filtre(    
                pix_origine[x-1,y-1][0],
                pix_origine[x,y-1][0],
                pix_origine[x+1,y-1][0],
                pix_origine[x-1,y][0],
                pix_origine[x,y][0],
                pix_origine[x+1,y][0], 
                pix_origine[x-1,y+1][0],
                pix_origine[x,y+1][0],
                pix_origine[x+1,y+1][0] 
                ) 
           
            pix_modifie[x,y] = (intensite_modifiee,)*3 #écriture des composantes R,G,B du pixel modifié
    
    # on renvoie l'image originale et l'image modifiée
    return im_originale,im_modifiee     

def Visualisation_Filtre(Nom_Filtre):
    
    # Application du filtre sur les images de test
    
    im_originale1,im_modifiee1 = Application_Filtre_image(Nom_Filtre,url='https://raw.githubusercontent.com/PythonLycee/PyLyc/master/img/city.bmp')
    im_originale2,im_modifiee2 = Application_Filtre_image(Nom_Filtre,url='https://raw.githubusercontent.com/PythonLycee/PyLyc/master/img/Chantier.bmp')

    fig = plt.figure(1, figsize=(15, 12))
    
    plt.subplot(2,2,1)
    plt.imshow(im_originale1)   
    plt.text(0,-10,'Image originale')
    plt.axis('off')
    
    plt.subplot(2,2,2)
    plt.imshow(im_modifiee1)
    plt.text(0,-10,'Détection des contours')
    plt.axis('off')
    
    plt.subplot(2,2,3)
    plt.imshow(im_originale2)   
    plt.text(0,-10,'Image originale')
    plt.axis('off')
    
    plt.subplot(2,2,4)
    plt.imshow(im_modifiee2)
    plt.text(0,-10,'Détection des contours')
    plt.axis('off')
    
    Coordonnees_image_origine={
        'NW':(0,2) , 'N':(1,2) , 'NE':(2,2) ,
        'W' :(0,1) , 'C':(1,1) ,  'E':(2,1) ,
        'SW':(0,0) , 'S':(1,0) , 'SE':(2,0) 
        }
    Coordonnees_image_arrivee={
        'NW':(4,2) , 'N':(5,2) , 'NE':(6,2) ,
        'W' :(4,1) , 'C':(5,1) ,  'E':(6,1) ,
        'SW':(4,0) , 'S':(5,0) , 'SE':(6,0)         
        }
        
    def Tableau_bord(NW,N,NE,W,C,E,SW,S,SE):
        
        
        # correspondances de couleur 
        Niveaux_gris={
                        'NW': NW/255 , 'N': N/255 , 'NE':NE/255 ,
                        'W' :  W/255 , 'C': C/255 ,  'E': E/255 ,
                        'SW': SW/255 , 'S': S/255 , 'SE':SE/255      
                     }
            
        #création de la figure
        fig,ax = plt.subplots()
        ax.axis('equal')                # repère orthonormé
        plt.plot([0,7],[0,3],alpha=0)   # ligne diagonale invisible pour la détection automatique de la taille souhaitée
        plt.axis('off')                 # axes masqués
        
        #création des carrés représentant les pixels pour chaque cardinalité
        for pos in ['NW','N','NE','W','C','E','SW','S','SE']:
            
            #pixel d'origine
            ax.add_patch(
                patches.Rectangle(
                    Coordonnees_image_origine[pos],
                    1,
                    1,
                    edgecolor='orange',    
                    facecolor=(Niveaux_gris[pos],)*3,
                    fill=True
                    )
                )
            
            plt.text(*Coordonnees_image_origine[pos],"    "+pos+"\n\n",color=(0 if Niveaux_gris[pos]>0.5 else 1,)*3 )
            
            
            
            #pixel d'arrivée
            
            lum = Nom_Filtre(NW,N,NE,W,C,E,SW,S,SE) #calcul de la luminosite
            
            ax.add_patch(
                patches.Rectangle(
                    Coordonnees_image_arrivee[pos],
                    1,
                    1,
                    edgecolor='orange',    
                    facecolor='white' if pos!='C' else (lum/255,)*3,
                    fill= pos=='C',
                    hatch='/' if pos!='C' else None
                    )
                )            
            if pos=='C':
                plt.text(*Coordonnees_image_arrivee[pos],"   "+str(lum)+"\n\n",color= (0 if lum>127 else 1,)*3)
            else:
                plt.text(*Coordonnees_image_arrivee[pos],"      ?\n\n",color= (0.2,)*3)
            

                
        plt.text(0.5,-0.35,"pixels d'origine")
        plt.text(4.5,-0.35,"pixel de détection")
        
        
        plt.show()
        
        
    

    interact(
        Tableau_bord,
        NW = (0,255,1), N = (0,255,1) , NE = (0,255,1),
        W  = (0,255,1), C = (0,255,1) , E  = (0,255,1),
        SW = (0,255,1), S = (0,255,1) , SE = (0,255,1))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
