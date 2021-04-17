from ipywidgets import widgets                             # pour la gestion des menus
import IPython ; from IPython.display import display, HTML # pour l'affichage HTML

def Menu_Options():
    """
    Génération du menu pour les options
    (Dérivation)
    """    
    #Menu Coefficients
    Menu_Coefficients = widgets.SelectMultiple (
        description = "",
        options=['coefficients entiers', 'coefficients rationnels'],
        value=['coefficients rationnels'],
        #rows=10,
        disabled=False
        )    
    #Menu Fonctions
    Menu_Fonctions = widgets.SelectMultiple (
        description = "",
        options=['puissances positives', 'puissances négatives', 'racine carrée', 'cosinus et sinus','exponentielle', 'logarithme népérien'],
        value=['puissances positives', 'puissances négatives', 'racine carrée'],
        #rows=10,
        disabled=False
        ) 
    #Menu Formules utilisées
    Menu_Formules = widgets.SelectMultiple (
        description = "",
        options=['Produit par un scalaire', 'Somme de fonctions', 'Produit de fonctions', 'Quotient de fonctions'],
        value=['Produit par un scalaire', 'Somme de fonctions', 'Produit de fonctions', 'Quotient de fonctions'],
        #rows=10,
        disabled=False
        ) 

    Menu_accordeon = widgets.Accordion(children = [Menu_Coefficients, Menu_Fonctions, Menu_Formules],
                                       selected_index = None
                                      )
    
    Titres=["Coefficients","Fonctions utilisées","Formules utilisées"]
    for k in range(len(Menu_accordeon.children)):
        Menu_accordeon.set_title(k, Titres[k])
    
    return Menu_accordeon

html_presentation_Options="""
<h1> Paramétrage des exercices </h1>
<p> Utiliser les menus déroulants : Sélectionner le type de coefficients, les fonctions et les formules à utiliser pour la génération des exercices.
<br>La <strong>multisélection</strong> est possible en utilisant la touche <strong>CTRL</strong> ou la touche <strong>SHIFT</srong>.</p>

"""

Options_exercices=Menu_Options()


