
from sympy import *                                         # import du module sympy
from random import randint,choice                           # import des fonctions générant l'aléatoire
import IPython ; from IPython.display import display, HTML  # pour la génération des écritures en html (dont latex)
from time import sleep                                      # pour la gestion des délais


# SYMBOLE GLOBAL POUR LA VARIABLE DES FONCTIONS
x=symbols('x')



    
    
    











def par(expr,gauche=True):
    """
    génère une parenthèse latex si l'expression démarre par - OU si elle contient un + OU un - à l'intérieur
    ( si gauche=True
    ) si gauche= False
    """
    return ("\\left( " if gauche else "\\right) ") if (expr[0]=="-" or "+" in expr[1:] or "-" in expr[1:]) else ""

def sig(expr):
    """
    génère un + si l'expression ne démarre pas par -
    """
    return "" if expr[0]=="-" else "+"

def rempl(expr):
    """
    remplace log par ln dans une chaine
    remplace les puissances à coeff 1/2 par des racines carrées
    """
    expr=expr.replace("log","ln")
    for k in range(20):
            expr=expr.replace("x^{\\frac{"+str(k)+"}{2}}",("x^{"+str(k//2)+"}" if k//2!=1 else "x")+" \\sqrt{x} ")
            expr=expr.replace("x^{"+str(k)+".5}","x^{"+str(k)+"} \\sqrt{x} ")
    return expr

def koeff(Rationnel=True,Nonnul=True):
    """
    fonction qui génère un coefficient 
    si Rationnel vaut True -> coeff rationnel
                      False -> coeff entier
                      None -> coeff 1 ou -1
    Non nul si Nonnul)
    """
    if Rationnel==None : return choice([-1,1])
    k=1
    while k in [-1,1]:
        k = choice([-1,1])*(Rational(randint(1 if Nonnul else 0,10),randint(1,10)) if Rationnel else randint(1 if Nonnul else 0,10))
    return k
    


# LES FONCTIONS QUI GENERENT UN EXERCICE (càd UNE FONCTION A DERIVER)
# RECOIVENT EN ARGUMENT UNE LISTE DE LISTES DE FONCTIONS
# (UNIFORMISATION POUR L'APPEL)







def derivee_produit_par_scalaire(l=['x'],Rationnel=True):
    """
    génère une fonction produit d'un coefficient et d'une fonction 
    renvoie :
    le titre de l'exercice
    la consigne (str)
    la solution
    la liste des détails de calcul (liste de str)
    la liste des feedback (juste, faux 1er essai, faux 2e essai) chacun de type liste de str
    la liste des lignes d'aide (liste de str)
    """
    Coeff = koeff(Rationnel) # génération d'un coefficient non nul
    f_usuelle = eval(choice(l[0])) # génération d'une fonction usuelle
    
    f = Coeff*f_usuelle 
    
    correction=["f(x)="+latex(f)]
    
    etape = "f(x)="+latex(Coeff)+"\\times "+latex(f_usuelle)
    if etape!=correction[-1]: correction.append(etape)
    
    correction.append(" \\text{ a pour dérivée : }")
    
    f_usuelle_der = simplify(diff(f_usuelle,x))
    etape = "f'(x)="+latex(Coeff)+"\\times "+par(latex(f_usuelle_der))+latex(f_usuelle_der)+par(latex(f_usuelle_der),False)
    correction.append(etape) 
    
    etape = "f'(x)="+latex(Coeff*f_usuelle_der)
    if etape!=correction[-1]: correction.append(etape)
    
    sol = diff(f,x)
    etape = "f'(x)="+latex(sol)
    if etape!=correction[-1]: correction.append(etape)
    
    sol=factor(sol)
    etape = "f'(x)="+latex(sol)
    if etape!=correction[-1]: correction.append(etape)
    
    sol=simplify(sol)
    etape = "f'(x)="+latex(sol)
    if etape!=correction[-1]: correction.append(etape)    
    
    consigne = "<latex> \[ \\text{Donner une expression de la dérivée de } f \\text{ définie par } f(x)= "+latex(f)+"  \\text{.} \] </latex>"
    
    L_feedback = [  [" \\color{#239B56}{\\text{Réponse correcte.}}",
                     " \\color{#239B56}{\\text{La réponse attendue était } f'(x)="+latex(sol)+"\\text{.}}"
                    ],
                    [" \\color{#D35400}{\\text{Réponse fausse.}}",
                     " \\color{#D35400}{\\text{Une aide est disponible pour le 2}^{\\text{ème}} \\text{ essai.}}"
                    ],
                    [" \\color{#E71212}{\\text{Réponse fausse.}}",
                     " \\color{#E71212}{\\text{La réponse attendue était } f'(x)="+latex(sol)+"\\text{. Voir correction ci-dessus.}}"
                    ]
                    ]
                        

    L_aide = ["\\text{ La formule à appliquer est :} ",
                "\\; \\left( k \\times u \\right)' = k \\times u' \\;",
                "\\text{ où } k \\text{ constante et } u \\text{ fonction dérivable sur un intervalle I. }  "
              ]
    
    return consigne,sol,correction,L_feedback,L_aide


    
def derivee_somme(l=['x'],Rationnel=True):
    """
    génère une fonction somme
    renvoie :
    le titre de l'exercice
    la consigne (str)
    la solution
    la liste des détails de calcul (liste de str)
    la liste des feedback (juste, faux 1er essai, faux 2e essai) chacun de type liste de str
    la liste des lignes d'aide (liste de str)
    """
    Coeff1 = koeff(Rationnel) # génération d'un non nul    
    f_usuelle1 = eval(choice(l[0])) # génération d'une fonction usuelle
    
    Coeff2 = koeff(Rationnel) # génération d'un coefficient non nul
    
    f_usuelle2 = f_usuelle1
    while f_usuelle2==f_usuelle1: # génération d'une AUTRE fonction usuelle
        f_usuelle2 = eval(choice(l[1]))     
    
    f = Coeff1*f_usuelle1+Coeff2*f_usuelle2 
    
    correction=["f(x)="+latex(f)]
    
    etape="f(x)="+latex(Coeff1)+"\\times "+latex(f_usuelle1)+sig(latex(Coeff2))+latex(Coeff2)+"\\times "+latex(f_usuelle2)
    if etape!=correction[-1]: correction.append(etape)
    
    correction.append(" \\text{ a pour dérivée : }")
    
    f_usuelle1_der = simplify(diff(f_usuelle1,x))
    f_usuelle2_der = simplify(diff(f_usuelle2,x))
    
    etape="f'(x)="+latex(Coeff1)+"\\times "+par(latex(f_usuelle1_der))+latex(f_usuelle1_der)+par(latex(f_usuelle1_der),False)+sig(latex(Coeff2))+latex(Coeff2)+"\\times "+par(latex(f_usuelle2_der))+latex(f_usuelle2_der)+par(latex(f_usuelle2_der),False)
    if etape!=correction[-1]: correction.append(etape)
    
    #etape="f'(x)="+latex(Coeff1*f_usuelle1_der)+"+"+("\\left( " if latex(Coeff2*f_usuelle2_der)[0]=="-" else "")+latex(Coeff2*f_usuelle2_der)+("\\right) " if latex(Coeff2*f_usuelle2_der)[0]=="-" else "")
    #if etape!=correction[-1]: correction.append(etape)
    
    etape="f'(x)="+latex(simplify(Coeff1*f_usuelle1_der+Coeff2*f_usuelle2_der))
    if etape!=correction[-1]: correction.append(etape)
    
    sol=simplify(diff(f,x))
    etape="f'(x)="+latex(sol)
    if etape!=correction[-1]: correction.append(etape)
    
    sol=factor(sol)
    etape="f'(x)="+latex(sol)
    if etape!=correction[-1]: correction.append(etape)    
    
    consigne = "<latex> \[ \\text{Donner une expression de la dérivée de } f \\text{ définie par } f(x)= "+latex(f)+"  \\text{.} \] </latex>"
    
    L_feedback = [  [" \\color{#239B56}{\\text{Réponse correcte.}}",
                     " \\color{#239B56}{\\text{La réponse attendue était } f'(x)="+latex(sol)+"\\text{.}}"
                    ],
                    [" \\color{#D35400}{\\text{Réponse fausse.}}",
                     " \\color{#D35400}{\\text{Une aide est disponible pour le 2}^{\\text{ème}} \\text{ essai.}}"
                    ],
                    [" \\color{#E71212}{\\text{Réponse fausse.}}",
                     " \\color{#E71212}{\\text{La réponse attendue était } f'(x)="+latex(sol)+"\\text{. Voir correction ci-dessus.}}"
                    ]
                    ]
                        

    L_aide = ["\\text{ La formule à appliquer est :} ",
                "\\; \\left( u + v \\right)' =  u' + v' \\;",
                "\\text{ où } u \\text{ et } v \\text{ fonctions dérivables sur un intervalle I. }  "
             ]
    
    return consigne,sol,correction,L_feedback,L_aide



    
    
    
    
    
    
    
def derivee_produit(l=['x'],Rationnel=True):
    """
    génère une fonction produit 
    renvoie :
    le titre de l'exercice
    la consigne (str)
    la solution
    la liste des détails de calcul (liste de str)
    la liste des feedback (juste, faux 1er essai, faux 2e essai) chacun de type liste de str
    la liste des lignes d'aide (liste de str)
    """
    
    Coeff1 = koeff(Rationnel) # génération d'un coefficient non nul   
    # le coeff est rattaché à la fonction 1 
    
    f_usuelle1 = eval(choice(l[0])) # génération d'une fonction usuelle
        
    f_usuelle2 = f_usuelle1
    while f_usuelle2==f_usuelle1: # génération d'une AUTRE fonction usuelle
        f_usuelle2 = eval(choice(l[1]))  
     
    f = (Coeff1*f_usuelle1)*f_usuelle2 
        
    correction=["f(x)="+par(latex(simplify(Coeff1*f_usuelle1)))+latex(simplify(Coeff1*f_usuelle1))+par(latex(simplify(Coeff1*f_usuelle1)),False)+" \\times "+par(latex(f_usuelle2))+latex(f_usuelle2)+par(latex(f_usuelle2),False) ]
        
    correction.append(" \\text{ a pour dérivée : }")
    
    f_usuelle1_der = simplify(diff(f_usuelle1,x))
    f_usuelle2_der = simplify(diff(f_usuelle2,x))
    
    etape="f'(x)="+par(latex(simplify(Coeff1*f_usuelle1_der)))+latex(simplify(Coeff1*f_usuelle1_der))+par(latex(simplify(Coeff1*f_usuelle1_der)),False)+" \\times "+par(latex(f_usuelle2))+latex(f_usuelle2)+par(latex(f_usuelle2),False)+"+"+par(latex(simplify(Coeff1*f_usuelle1)))+latex(simplify(Coeff1*f_usuelle1))+par(latex(simplify(Coeff1*f_usuelle1)),False)+" \\times "+par(latex(f_usuelle2_der))+latex(f_usuelle2_der)+par(latex(f_usuelle2_der),False)
    if etape!=correction[-1]: correction.append(etape)
    
    etape="f'(x)="+par(latex(simplify(Coeff1*f_usuelle1_der*f_usuelle2)))+latex(simplify(Coeff1*f_usuelle1_der*f_usuelle2))+par(latex(simplify(Coeff1*f_usuelle1_der*f_usuelle2)),False)+"+"+par(latex(simplify(Coeff1*f_usuelle1*f_usuelle2_der)))+latex(simplify(Coeff1*f_usuelle1*f_usuelle2_der))+par(latex(simplify(Coeff1*f_usuelle1*f_usuelle2_der)),False)
    if etape!=correction[-1]: correction.append(etape)
    
    etape="f'(x)="+latex(simplify(Coeff1*f_usuelle1_der*f_usuelle2+Coeff1*f_usuelle1*f_usuelle2_der))
    if etape!=correction[-1]: correction.append(etape)
    
    sol=simplify(diff(f,x))
    etape="f'(x)="+latex(sol)
    if etape!=correction[-1]: correction.append(etape)                     
                         
    sol=factor(sol)
    etape="f'(x)="+latex(sol)
    if etape!=correction[-1]: correction.append(etape)    
    
    consigne = "<latex> \[ \\text{Donner une expression de la dérivée de } f \\text{ définie par } f(x)= "+par(latex(simplify(Coeff1*f_usuelle1)))+latex(simplify(Coeff1*f_usuelle1))+par(latex(simplify(Coeff1*f_usuelle1)),False)+" \\times "+par(latex(f_usuelle2))+latex(f_usuelle2)+par(latex(f_usuelle2),False)+"  \\text{.} \] </latex>"
    
    L_feedback = [  [" \\color{#239B56}{\\text{Réponse correcte.}}",
                     " \\color{#239B56}{\\text{La réponse attendue était } f'(x)="+latex(sol)+"\\text{.}}"
                    ],
                    [" \\color{#D35400}{\\text{Réponse fausse.}}",
                     " \\color{#D35400}{\\text{Une aide est disponible pour le 2}^{\\text{ème}} \\text{ essai.}}"
                    ],
                    [" \\color{#E71212}{\\text{Réponse fausse.}}",
                     " \\color{#E71212}{\\text{La réponse attendue était } f'(x)="+latex(sol)+"\\text{. Voir correction ci-dessus.}}"
                    ]
                    ]
                        

    L_aide = ["\\text{ La formule à appliquer est :} ",
                "\\; \\left( u \\times v \\right)' =  u' \\times v + u \\times v' \\;",
                "\\text{ où } u \\text{ et } v \\text{ fonctions dérivables sur un intervalle I. }  "
             ]
    
    return consigne,sol,correction,L_feedback,L_aide


def derivee_quotient(l=['x'],Rationnel=True):
    """
    génère une fonction quotient
    renvoie :
    le titre de l'exercice
    la consigne (str)
    la solution
    la liste des détails de calcul (liste de str)
    la liste des feedback (juste, faux 1er essai, faux 2e essai) chacun de type liste de str
    la liste des lignes d'aide (liste de str)
    """
    
    Coeff1 = koeff(Rationnel) # génération d'un coefficient non nul   
    # le coeff est rattaché à la fonction 1 
    
    f_usuelle1 = eval(choice(l[0])) # génération d'une fonction usuelle
        
    f_usuelle2 = f_usuelle1
    while f_usuelle2==f_usuelle1: # génération d'une AUTRE fonction usuelle
        f_usuelle2 = eval(choice(l[1]))  
     
    f = (Coeff1*f_usuelle1)/f_usuelle2 
        
    correction=["f(x)= "+latex(Coeff1)+"\\times \\frac{"+latex(f_usuelle1)+"}{"+latex(f_usuelle2)+"}"]
        
    correction.append(" \\text{ a pour dérivée : }")
    
    f_usuelle1_der = simplify(diff(f_usuelle1,x))
    f_usuelle2_der = simplify(diff(f_usuelle2,x))
    
    etape="f'(x)= "+latex(Coeff1)+"\\times \\frac{"+par(latex(f_usuelle1_der))+latex(f_usuelle1_der)+par(latex(f_usuelle1_der),False)+" \\times "+par(latex(f_usuelle2))+latex(f_usuelle2)+par(latex(f_usuelle2),False)+"-"+par(latex(f_usuelle1))+latex(f_usuelle1)+par(latex(f_usuelle1),False)+" \\times "+par(latex(f_usuelle2_der))+latex(f_usuelle2_der)+par(latex(f_usuelle2_der),False)+"}{ \\left( "+ latex(f_usuelle2)  +" \\right) ^2 }"
    if etape!=correction[-1]: correction.append(etape)
    
    etape="f'(x)= "+latex(Coeff1)+"\\times \\frac{"+par(latex(simplify(f_usuelle1_der*f_usuelle2)))+latex(simplify(f_usuelle1_der*f_usuelle2))+par(latex(simplify(f_usuelle1_der*f_usuelle2)),False)+"-"+par(latex(simplify(f_usuelle1*f_usuelle2_der)))+latex(simplify(f_usuelle1*f_usuelle2_der))+par(latex(simplify(f_usuelle1*f_usuelle2_der)),False)+"}{ \\left( "+ latex(f_usuelle2)  +" \\right) ^2 }"
    if etape!=correction[-1]: correction.append(etape)
    
    etape="f'(x)= "+latex(Coeff1)+"\\times \\frac{"+latex(simplify(f_usuelle1_der*f_usuelle2-f_usuelle1*f_usuelle2_der))+"}{ \\left( "+ latex(f_usuelle2)  +" \\right) ^2 }"
    if etape!=correction[-1]: correction.append(etape)
    
    sol=simplify(diff(f,x))
    #etape="f'(x)="+latex(sol)
    #if etape!=correction[-1]: correction.append(etape)                     
                         
    sol=factor(sol)
    etape="f'(x)="+latex(sol)
    if etape!=correction[-1]: correction.append(etape)    
    
    consigne = "<latex> \[ \\text{Donner une expression de la dérivée de } f \\text{ définie par } f(x)= "+latex(Coeff1)+"\\times \\frac{"+latex(simplify(f_usuelle1))+"}{"+latex(f_usuelle2)+"} \\text{.} \] </latex>"
    
    L_feedback = [  [" \\color{#239B56}{\\text{Réponse correcte.}}",
                     " \\color{#239B56}{\\text{La réponse attendue était } f'(x)="+latex(sol)+"\\text{.}}"
                    ],
                    [" \\color{#D35400}{\\text{Réponse fausse.}}",
                     " \\color{#D35400}{\\text{Une aide est disponible pour le 2}^{\\text{ème}} \\text{ essai.}}"
                    ],
                    [" \\color{#E71212}{\\text{Réponse fausse.}}",
                     " \\color{#E71212}{\\text{La réponse attendue était } f'(x)="+latex(sol)+"\\text{. Voir correction ci-dessus.}}"
                    ]
                    ]
                        

    L_aide = ["\\text{ La formule à appliquer est :} ",
                "\\; \\left( \\frac{u}{v} \\right)' =  \\frac{u' \\times v - u \\times v'}{v^2} \\;",
                "\\text{ où } u \\text{ et } v \\text{ fonctions dérivables sur un intervalle I où } v \\text{ ne s'annule pas. }"
             ]
    
    return consigne,sol,correction,L_feedback,L_aide















def html_presentation(titre_exercice="",decompte_reponses=[0,0,0],insert_html='',align='center',width=800,height=70,backcolor='#FAE5D3',padding=0.5,margin=0.1):
    """
    création de la boîte du titre 
    """   
    insert_html += '<div id="presentation" style="float: '+align+'; width: '+str(width)+'px; height: '+str(height)+'px; background-color: '+backcolor+'; padding:'+str(padding)+'em; ;margin: '+str(margin)+'em;">'
    
    # score
    
    insert_html += """
    
    <table style="float: right;">
    <tr style="padding=0.1em; background-color:#EDBB99; ">
        <td style="text-align:left; font-size: 14px; text-align:center;"><strong>Score :</strong></td>
        <td style="text-align:left; font-size: 14px; text-align:center;"><strong>
    """    
    
    if decompte_reponses[0]!=0:
        doublenote=2*decompte_reponses[1]+decompte_reponses[2]
        pair=doublenote%2==0
        insert_html += "<latex> \\[ \\frac{"+str((doublenote)//2)+("" if pair else ",5")+"}{"+str(decompte_reponses[0])+"} \\] </latex>"
    else:
        insert_html += "Pas de note"
        
    insert_html += """    
        </strong></td>
    </tr>
    <tr style="padding=0.1em; background-color:#F6DDCC;">
        <td style="text-align:left; font-size: 10px; text-align:left;">Juste 1<sup>er</sup> essai :</td>
        <td style="text-align:left; font-size: 10px; text-align:center;">
    """ 
    insert_html += str(decompte_reponses[1])
    insert_html += """    
        </td>
    </tr>
    <tr style="padding=0.1em; background-color:#F6DDCC;">
        <td style="text-align:left; font-size: 10px; text-align:left;">Juste 2<sup>ème</sup> essai :</td>
        <td style="text-align:left; font-size: 10px; text-align:center;">
    """
    insert_html += str(decompte_reponses[2])
    insert_html += """    
        </td>
    </tr>
    <tr style="padding=0.1em; background-color:#F6DDCC;">
        <td style="text-align:left; font-size: 10px; text-align:left;">Faux :</td>
        <td style="text-align:left; font-size: 10px; text-align:center;">
    """    
    insert_html += str(decompte_reponses[0]-(decompte_reponses[1]+decompte_reponses[2]))   
    insert_html += """     
        </td>
    </tr>
    </table>
    """
        
    # titre
    insert_html += '<p>'
    insert_html += '<span style="color:#123456; font-size: 8px;  text-align:center;">&copy www.python-lycee.com</span></br>'
    insert_html += '<span style="color:#123456; font-size: 16px; text-align:center;"><strong>Exercice : '+titre_exercice+'</strong></span>'
    insert_html += '</p>'
        
    insert_html += '</div>'
    
    
    return insert_html

def html_consigne(entete="",consigne="",insert_html='',align='center',width=800,height=75,backcolor='#FDF2E9',padding=0.5,margin=0.1):
    """
    création de la boîte de consigne
    entete,consigne de type str
    """
    insert_html += '<div id="consigne" style="float: '+align+'; width: '+str(width)+'px; height: '+str(height)+'px; background-color: '+backcolor+'; padding:'+str(padding)+'em; ;margin: '+str(margin)+'em;">'
    insert_html += '<h2 style="color:#123456; font-size: 14px; text-align:left;"><strong>'+entete+'</strong><br>'
    insert_html += rempl(consigne)+'</h2>'
    insert_html += '</div>'
    return insert_html

def html_correction(entete="",correction="",vide=False,insert_html='',align='center',width=800,height=350,backcolor='#FDF2E9',padding=0.5,margin=0.1):
    """
    création de la zone de correction
    entete de type str
    correction : liste des lignes de type str
    vide : booléen qui indique si la zone doit être vide
    """
    insert_html += '<div id="correction" style="float: '+align+'; min-width: '+str(width)+'px; max-width: '+str(width)+'px; width: '+str(width)+'px; height: '+str(height)+'px;  background-color: '+backcolor+'; padding:'+str(padding)+'em; ;margin: '+str(margin)+'em;">'
    if not vide: 
        insert_html += '<h2 style="color:#123456; font-size: 14px; text-align:left;"><strong>'+entete+'</strong><br>'
        for ligne in correction:
            insert_html += '<latex> \[ '+rempl(ligne)+' \] </latex> <br>'
        insert_html += '</h2>'
    insert_html += '</div>'
    return insert_html

    # overflow-x:scroll; overflow-y:scroll; window.document.getElementById(div).scrollTop = window.document.getElementById(div).scrollHeight;


def html_feedback(commentaires=[],aide=None,insert_html='',align='center',width=800,height=175,backcolor='#FAE5D3',padding=0.5,margin=0.1):
    """
    création de la zone de feedback
    feedback : liste des lignes de type str
    """
    insert_html += '<div id="correction" style="float: '+align+'; min-width: '+str(width)+'px; max-width: '+str(width)+'px; width: '+str(width)+'px; height: '+str(height)+'px;  background-color: '+backcolor+'; padding:'+str(padding)+'em; ;margin: '+str(margin)+'em;">'
    
    #affichage de l'aide
    if aide:
        

        insert_html += """
        
        <div class="Aide_parent">
        <span style="color:#14A752; font-weight:bold;"> Aide </span>
        <div class="Aide_enfant">
        <div style="color:#14A752; text-align: left; background-color: #D9FEEC;">
        """
        for ligne in aide:
            insert_html += '<latex> \[ '+rempl(ligne)+' \] </latex>' 
        insert_html += """
        </div>
        </div>
        </div>
        
        """  
    else:
        insert_html += """
        <div class="Aide_parent">
        <span style="color:#888888;"> Aide </span>
        <div class="Aide_enfant">
        <span style="font-size: 10px; color:#888888;">L'aide est accessible pour le 2ème essai</span>
        </div>
        </div>
        
        """

    
    insert_html += '<h2 style="color:#123456; font-size: 14px; text-align:left;">'
    for ligne in commentaires:
        insert_html += '<latex> \[ '+rempl(ligne)+' \] </latex>'
    insert_html += '</h2>'
    insert_html += '</div>'
    return insert_html

    # overflow-x:scroll; overflow-y:scroll; window.document.getElementById(div).scrollTop = window.document.getElementById(div).scrollHeight;

  
    

    
def Genere_html(consigne,correction,commentaires=[],vide=False,decompte_reponses=[0,0,0],aide=None,titre_exercice=""):
    """
    Fonction qui génère l'affichage html
    """   
    body = "<body>"
    body += html_presentation(titre_exercice=titre_exercice,decompte_reponses=decompte_reponses) #insertion du titre
    body += html_consigne(entete="Consigne :",consigne=consigne) #insertion de la consigne
    body += html_correction(entete="Correction :",correction=correction,vide=vide) #insertion de la zone de correction
    body += html_feedback(commentaires,aide)

    body += "</body>"    
    return body















# Récupération des Options sélectionnées   

try:
    #récupération des options si elles ont été sélectionnées
    type_coeff = list(Options_exercices.children[0].value)  
    fonc_usuel = list(Options_exercices.children[1].value)
    formules =   list(Options_exercices.children[2].value)    
except:
    #valeurs par défaut sinon (si Options_exercices n'existe pas)
    type_coeff = ['coefficients rationnels']
    fonc_usuel = ['puissances positives', 'puissances négatives', 'racine carrée']
    formules =   ['Produit par un scalaire', 'Somme de fonctions', 'Produit de fonctions', 'Quotient de fonctions']


# GENERATION DES LISTES D'EXERCICES

#exercices = [ (derivee_produit_par_scalaire,[liste_fonc]),(derivee_somme,[liste_fonc3,liste_fonc3])]    
#exercices2 = [ (derivee_produit,[liste_fonc,liste_fonc]) ]
    
Rationnel = True if 'coefficients rationnels' in type_coeff else (False if 'coefficients entiers' in type_coeff else None) 
    
def genere_Liste_exercices(type_coeff,fonc_usuel,formules):
    # GENERATION DES LISTES DE FONCTIONS USUELLES

    def f_polynome(deg, withrat=True):
        """
        génère un polynôme à coefficients entiers
        deg : degré du polynôme
        """
        f = ""
        for k in range(deg+1):
            f += choice(["+","-"])+str(randint(0 if k<deg else 1,10))+"*x**"+str(k)
        return f

    #liste_fonc2=f_trigo+f_puissance_pos
    #liste_fonc3=f_trigo+f_puissance_pos
    #liste_fonc=f_trigo+f_puissance_pos  

    fonction_corr={'puissances positives':[ 'x**'+str(k) for k in range(1,4) ],
                   'puissances négatives':[ 'x**'+str(k) for k in range(-3,0) ],
                   'racine carrée':[ 'sqrt(x)'],
                   'cosinus et sinus':[ 'cos(x)','sin(x)' ],
                   'exponentielle':[ 'exp(x)' ],
                   'logarithme népérien':[ 'ln(x)' ] }

    # CONSTRUCTION DE LA LISTE PRINCIPALE DE FONCTIONS
    liste_principale_fonc = []
    for description in fonc_usuel: liste_principale_fonc += fonction_corr[description]

    # CONSTRUCTION DE LA LISTE SECONDAIRE DE FONCTIONS
    liste_secondaire_fonc = [] # sans puissances pour éviter les simplifications sans formules
    for description in fonc_usuel: 
        if description not in ['puissances positives','puissances négatives']:
            liste_secondaire_fonc += fonction_corr[description]

    # CONSTRUCTION DE LA LISTE DES GENERATEURS DE FORMULES

    formule_corr={ 'Produit par un scalaire':derivee_produit_par_scalaire,
                   'Somme de fonctions':derivee_somme, 
                   'Produit de fonctions':derivee_produit, 
                   'Quotient de fonctions':derivee_quotient } # A MODIFIER      

    # CONSTRUCTION DE LA LISTE DES EXERCICES POSSIBLES
    
    
    Liste_exercices = []
    for formule in formules:
        
        # Exercices classiques (toutes possibilités) sauf quotient
        if formule != 'Quotient de fonctions':
            Liste_exercices.append( (formule_corr[formule],[liste_principale_fonc,liste_secondaire_fonc]) )
            Liste_exercices.append( (formule_corr[formule],[liste_secondaire_fonc,liste_principale_fonc]) )
    
        # Pour le produit : ajout de produit par polynômes
        if formule == 'Produit de fonctions' and 'puissances positives' in fonc_usuel:
            Liste_exercices.append( (formule_corr[formule],
                                     [liste_principale_fonc,[f_polynome(2,True if Rationnel else False) for k in range(3)]]) )  
        # Pour le quotient
        if formule == 'Quotient de fonctions': 
            Liste_exercices.append( (formule_corr[formule],[liste_secondaire_fonc,liste_secondaire_fonc]) )
        if formule == 'Quotient de fonctions' and 'puissances positives' in fonc_usuel:    
            Liste_exercices.append( (formule_corr[formule],[liste_secondaire_fonc,[f_polynome(2,True if Rationnel else False) for k in range(3)]]) )
        
            
    return Liste_exercices


  
    

def Exerciceur_Derivation(Liste_exercices,titre_exercice="Application des formules de dérivation"): 
    """
    Argument exercice : fonction qui génère l'exercice
    
    """
    global Options
    
    #création du head de la page html avec insertions css
    head = """
    <head>
        <meta charset="utf-8" />
        <title> Exerciseur python-lycee.com </title>
        <script type="text/javascript" src="http://latex.codecogs.com/latexit.js"></script>
        <script type="text/javascript">LatexIT.add('latex',true);</script>
        <style>
        

        
        div.Aide_enfant
            {
             display: none;
             
            }

        div.Aide_parent:hover .Aide_enfant
            {
            display:block;
            }
        div.Aide_parent
            {
            text-align: right;
            float: right;
            }
        
        </style>
    </head>      
    """ #reprendre des élements de BBDSQL pour le style
    
    
    # Constantes pour le score
    decompte_reponses = [0,0,0] # nbre de questions traitées, nbre de juste en 1, nbre de juste en 2
    
    
    
    while "on ne quitte pas":  

        # génération de l'énoncé+aide+feedback
        # l'exercice est choisi au hasard parmi la liste des possibilités
        
        
        fonction_formule,liste_fonctions_usuelles = choice(Liste_exercices)
        print("fonction_formule",fonction_formule)
        print("liste_fonctions_usuelles",liste_fonctions_usuelles)
        
        
        consigne,sol,correction,L_feedback,L_aide = fonction_formule(liste_fonctions_usuelles,Rationnel)
        
        #exercice(l=l,Rationnel=(Options.children[0].value=="Rationnel")) 
        
        
        
        
        # création de l'affichage html
        body = Genere_html(consigne,correction,vide=True,decompte_reponses=decompte_reponses,titre_exercice=titre_exercice)
                
        # raffraichissement de l'affichage
        IPython.display.clear_output(wait=True)
        raffraichi = None == display(HTML('<html>'+head+body+'</html>'))
        
        # précaution d'attente pour que le input de la requête soit inséré après le html
        while not raffraichi: None 
        sleep(0.1)                           
        
        
        for essai in [1,2]: # 2 essais possibles
            
            aide_dispo = False # on désactive l'aide
            
            # input de la proposition
            while True: 
                entree = input("\nVeuillez saisir et valider votre proposition :")
                try:
                    proposition = parse_expr(entree) ; break
                except:
                    print("Saisie invalide.")    
            
            # vérification de la proposition

            Verification = expand(proposition)==expand(sol)

            
            if Verification:        
                decompte_reponses[essai] += 1 # on incrémente le décompte correspond à l'essai concluant
                decompte_reponses[0] +=1      # on incrémente le compteur du nombre de questions
                
                commentaires = ["\\text{Votre saisie : }"+str(latex(proposition))]                
                commentaires += L_feedback[0] # création du commentaire feedback (réponse juste)
                
                
                
            else:
                if essai==1 :                     # si erreur au 1er essai
                    aide_dispo = True            # on permet l'affichage de l'aide    
                
                if essai==2 :                     # si erreur au 2e essai
                    decompte_reponses[0] +=1      # on incrémente le compteur du nombre de questions       
                commentaires = ["\\text{Votre saisie : }"+str(latex(proposition))]
                commentaires += L_feedback[essai] # création du commentaire feedback (réponse fausse)
                
                
                
                
            # création de l'affichage html
            body = Genere_html(consigne,correction,commentaires=commentaires,vide=(essai==1 and not Verification),decompte_reponses=decompte_reponses,aide=(L_aide if aide_dispo else None),titre_exercice=titre_exercice) 
            
            # raffraichissement de l'affichage
            IPython.display.clear_output(wait=True)
            raffraichi = None == display(HTML('<html>'+head+body+'</html>'))
        
            # précaution d'attente pour que le input de la requête soit inséré après le html
            while not raffraichi: None 
            sleep(0.1)                           
            
            if Verification: 
                break
        
             
        # Attente de validation pour continuer ou quitter
        Choix = input("Valider pour continuer (pour quitter :saisir q ou Q et valider)")
        if Choix in ['q','Q']: break
    
    IPython.display.clear_output()       
    return None    
        


