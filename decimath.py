"""
MODULE DECIMATH

(C) Copyright 2019-2020 Franck CHEVRIER
Développé depuis 12/2019
Version 1.05
Dernière mise à jour: 30/01/2020

www.python-lycee.com

Description:
Module créant un type decimal (codage de fractions décimales à mémoires de calcul) pour contourner les problèmes de calcul sur les float

Finalité:
Mise en oeuvre d'algorithmes mathématiques en lycée en faisant abstraction des problèmes de calculs sur les nombres de type float

Fonctions gérées:
Comparaisons, opérations élémentaires, puissances entières, racines n ème.

NB: Si nécessaire, l'import du module math (import math OU from math import*) doit être effectué AVANT l'import du module decimal, qui reconstruit une fonction sqrt étendue.

"""

from math import sqrt as private_sqrt_float

def private_est_entier(nbre):
    """
    indique si un float est entier
    """
    return nbre==int(nbre)

def private_noms_variable(a,variables=globals()):
    """
    récupère la liste des noms de toutes les variables globales égales à a
    """
    return [var for var in variables if variables[var] is a]

def private_pgcd(a,b):
    """
    renvoie le pgcd de 2 entiers
    """
    return a if b==0 else private_pgcd(b,a%b)

def private_ppcm(a,b):
    """
    renvoie le ppcm de 2 entiers
    """
    return (a*b)//private_pgcd(a,b)

class decimal(): 
    
    def __init__(self,nbre=None):
        """
        création d'une fraction décimale à partir d'un élément de type float ou int 
        
        Caractéristiques:
        
        num: (type int) numerateur de la fraction 
        
        puiss: (type int) exposant de la puiss de 10 du denominateur 
        
        exact: (type bool) indique si la valeur est exacte 
        (ce booléen devient False si le décimal est construit comme quotient non exact ou comme racine n ème non exacte)
        
        puissances_exactes:  (type dict) recense les puissances exactes connues (puissances en clés)
        
        self.produits_exacts: (type dict) recense les produits connus (facteur en clés)
        """
        if type(nbre) is int:
            
            chaine=str(nbre)
            puiss=None
            if 'e' in chaine:
                place_e=chaine.index('e')
                self.num=int(chaine[:place_e])
                self.puiss=int(chaine[place_e+1:])
            else:
                self.num=nbre
                self.puiss=0
        
        elif type(nbre) is float:
            if private_est_entier(nbre):
                self.num=int(nbre)
                self.puiss=0
            else:
                chaine=str(nbre)
                puiss=0
                
                if 'e' in chaine:
                    place_e=chaine.index('e')
                    puiss-=int(chaine[place_e+1:])
                    chaine=chaine[:place_e]
                
                if '.' in chaine:
                    place_virgule=chaine.index('.')
                    chaine=chaine[:place_virgule]+chaine[place_virgule+1:]
                    puiss+=len(chaine)-place_virgule
                
                if puiss<0:
                    chaine=chaine+("0"*(-puiss))
                    puiss=0    
                
                self.num=int(chaine)
                self.puiss=puiss
        
        else:
            self.num=0
            self.puiss=0
        
        #indique si la valeur est exacte    
        self.exact=True
        
        #mise en memoire si connues des puissances exactes du nombre
        self.puissances_exactes={}
        
        #mise en memoire si connus des produits exacts
        self.produits_exacts=[] 
    
    def fdec(self,affiche=True,renvoie=False): 
        """
        fonction d'affichage du decimal sous la forme d'une fraction decimale
        par defaut: affiche en console (argument affiche)
                    ne renvoie rien (argument renvoie)
        (si renvoie: renvoie la chaine avec sauts de ligne \n)
        """
        chaine="\n"
        taille_frac=0 if self.puiss==0 else max(len(str(self.num)),3+len(str(self.puiss)))
        if taille_frac==0:
            chaine+=str(self.num)
        else:
            chaine+=" "*((taille_frac-len(str(self.num)))//2)+str(self.num)+"\n"+"_"*taille_frac
            
            if self.puiss>1:
                decalage=taille_frac-len(str(self.puiss))-3
                chaine+="\n"+(" "*(decalage//2+2))+str(self.puiss)+"\n"+(" "*(decalage//2))+"10"
                
            else:
                chaine+="\n"+(" "*((taille_frac-len(str(self.puiss)))//2))+"10"
                
        if affiche: print(chaine)
        if renvoie: return chaine
    
    def __liste_formel__(self):
        """
        renvoie une liste d'écritures formelles du decimal
        """
        L=[]
        
        for m in self.puissances_exactes:
            for val in self.puissances_exactes[m].__liste_formel__():
                L.append("("+val+")**(1/"+str(m)+")")
        
        for couple in self.produits_exacts:
            for valden in couple[0].__liste_formel__():
                for valnum in couple[1].__liste_formel__():
                    L.append("("+valnum+")/("+valden+")")
        
        return L if L else [str(self)]
    
    def formel(self):
        """
        affiche en console des écritures formelles du decimal
        """
        for ecriture in self.__liste_formel__():
            print(ecriture)
        
    def __str__(self): #conversion en str
        """
        conversion du decimal en str
        """
        self.__simplification__()
        num=self.num
        chaine=""
        
        if self.num<0:
            chaine+="-"
            num=-num

        chiffres=str(num)
        
        if len(chiffres)<=self.puiss:
            return chaine+("0."+"0"*(self.puiss-len(chiffres))+str(num))
        
        return chaine+chiffres[:len(chiffres)-self.puiss]+("." if self.puiss>0 else "")+chiffres[len(chiffres)-self.puiss:]
    
    def __int__(self): #conversion en int
        """
        conversion du decimal en int
        """
        return self.num//(10**self.puiss)
        
    def __float__(self): #conversion en float
        """
        conversion du decimal en float
        """
        return float(str(self))   
          
    def __repr__(self):
        """
        représentation extérieure du decimal (affichage console) 
        """
        return str(self)

    def __simplification__(self):
        """
        Simplification d'un decimal
        """
        if self.num==0:
            self.puiss=0
        else:
            while private_est_entier(self.num/10) and self.puiss>0:
                self.puiss-=1
                self.num=self.num//10

    def __add__(self,other): #symbole +
        """
        Somme de deux décimaux
        """
        if type(other)!=decimal: other=decimal(other)
        somme=decimal()
        somme.num=self.num*10**other.puiss+other.num*10**self.puiss
        somme.puiss=self.puiss+other.puiss
        somme.__simplification__()
        
        somme.exact=self.exact and other.exact
        
        return somme
        
    def __radd__(self,other):    
        conv=decimal(other)
        return self.__add__(conv)
        
    def __mul__(self,other): #symbole *
        """
        Produit de deux décimaux
        """
        if type(other)!=decimal: other=decimal(other)
        
        #recherche d'un produit exact connu
        for facteurs in [[self,other],[other,self]]:
            for couple in facteurs[0].produits_exacts:  
                if facteurs[1]==couple[0]: return couple[1] 
        
        #tentative de construction d'un produit à partir des produits connus
        for facteurs in [[self,other],[other,self]]:
            for couple in facteurs[0].produits_exacts:
                quotient=other/couple[0]
                if quotient.exact: return couple[1]*quotient
        
        #calcul du produit
        produit=decimal()
        produit.num=self.num*other.num
        produit.puiss=self.puiss+other.puiss
        produit.__simplification__()
        
        produit.exact=self.exact and other.exact
        
        #UNIQUEMENT si le produit n'est pas exact:
        
        if not produit.exact:
            #récupération profonde des propriétés
            for facteurs in [[self,other],[other,self]]:    
                for f in facteurs[0].puissances_exactes:
                    produit.puissances_exactes[f]=(facteurs[1]**f)*facteurs[0].puissances_exactes[f]
            for facteurs in [[self,other],[other,self]]:
                for couple in facteurs[0].produits_exacts:
                    produit.produits_exacts.append([couple[0],facteurs[1]*couple[1]])
            
        return produit  
    
    def __rmul__(self,other):
        conv=decimal(other)
        return self.__mul__(conv)        

    def __pos__(self): # précédé de +
        return self
    
    def __neg__(self): # précédé de -
        """
        Opposé d'un décimal
        """
        opp=decimal()
        opp.num=-self.num
        opp.puiss=self.puiss
        opp.exact=self.exact
        
        #récuperation profonde des propriétés
        for couple in self.produits_exacts:
            opp.produits_exacts.append([couple[0],-couple[1]])
        for m in self.puissances_exactes:
            opp.puissances_exactes[m]= (-self.puissances_exactes[m] if m%2 else self.puissances_exactes[m])
          
        return opp
    
    def __sub__(self,other): #symbole -
        """
        Différence de deux decimaux
        """
        if type(other)!=decimal: other=decimal(other)
        return self + (-other)
        
    def __lsub__(self,other):
        conv=decimal(other)
        return conv.__sub__(self)
    
    def __rsub__(self,other):
        conv=decimal(other)
        return conv.__sub__(self)
    
    def __truediv__(self,other):  #symbole /   
        """
        Quotient de deux decimaux
        """
        if type(other)!=decimal: other=decimal(other)
        
        #calcul du quotient
        quotient=decimal(float(self)/float(other))
        quotient.__simplification__()
        
        #recuperation initiale de la propriété exact
        quotient.exact=self.exact and other.exact
        
        #verification du caractere exact (par dernier chiffre)
        if quotient.exact:
            self.__simplification__()
            other.__simplification__()
            chif=(other.num%10)*(quotient.num%10)
            if (chif%10 if chif%10!=0 else chif//10)!=self.num%10: quotient.exact=False
        
        #UNIQUEMENT SI LA VALEUR N'EST PAS EXACTE:
        if not quotient.exact:
            #mise en memoire du produit exact
            quotient.produits_exacts.append([other,self]) 

            #recuperation profonde des propriétés
            for couple in self.produits_exacts:
                quotient.produits_exacts.append([couple[0],couple[1]/other])
            for couple in other.produits_exacts:
                quotient.produits_exacts.append([couple[1],couple[0]*self])
            for m in self.puissances_exactes:
                quotient.puissances_exactes[m]=self.puissances_exactes[m]/(other**m)
            for m in other.puissances_exactes:
                quotient.puissances_exactes[m]=(self**m)/other.puissances_exactes[m]           
            
        return quotient
    
    def __ltruediv__(self,other):
        conv=decimal(other)
        return conv.__truediv__(self)        
    
    def __rtruediv__(self,other):
        conv=decimal(other)
        return conv.__truediv__(self)          
    
    
    def __pow__(self,n): #symbole **
        """
        Puissance d'une fraction decimale
        ATTENTION: n est suppose entier dans cette version (upgrade a ecrire)
        """
        #cas où n<=0
        if n==0: return decimal(1)
        if n<0: return 1/decimal(self)**(-n)
        
        #recuperation de la valeur exacte de la puissance si elle est connue
        for m in self.puissances_exactes:
            if n%m==0:
                p= self.puissances_exactes[m]**(n//m)
                return p
                 
        #calcul de la puissance
        p=decimal()
        p.num=self.num**n
        p.puiss=self.puiss*n
        p.__simplification__()
        p.exact=self.exact
        
        #récupération des propriétés profondes
        for m in self.puissances_exactes:
            pgcd=private_pgcd(n,m)
            mdiv=m//pgcd
            ndiv=n//pgcd
            p.puissances_exactes[mdiv]=self.puissances_exactes[m]**ndiv
        for couple in self.produits_exacts:
            p.produits_exacts.append([couple[0]**n,couple[1]**n])
        
        return p
    
    def __eq__(self,other): #==
        """
        test a==b pour a,b de type decimal
        """
        if type(other)!=decimal: other=decimal(other)
        self.__simplification__()
        other.__simplification__()
        return self.exact==other.exact and self.num==other.num and self.puiss==other.puiss          
        #!!! Ajouter les tests sur les puiss et racines et sur exact   
    
    def __lt__(self,other): #<
        """
        test a<b pour a,b de type decimal
        """
        return float(self)<float(other)
    
    def __gt__(self,other): #>
        """
        test a>b pour a,b de type decimal
        """
        return float(self)>float(other)
    
    def __le__(self,other): #<=
        """
        test a<=b pour a,b de type decimal
        """
        return self==other or float(self)<float(other)
    
    def __ge__(self,other): #>=
        """
        test a>=b pour a,b de type decimal
        """
        return self==other or float(self)>float(other)  

    def __pos__(self): # précédé de signe +
        """
        renvoie +a càd a
        """
        return self

    def prop(self): #affiche les propriétés de la valeur
        
        #récupération du nom de la variable
        
        liste_x=""
        nvar=private_noms_variable(self)
        if not nvar:
            liste_x="var"
        else:
            for var in nvar:
                liste_x+=(var+"=")
            liste_x=liste_x[:len(liste_x)-1]
        
        print(liste_x,"=",self)
        print("Cette valeur de",liste_x,"est","exacte" if self.exact else "approchée")
        if self.puissances_exactes or self.produits_exacts:
            print("La valeur exacte de",liste_x,"a pour caractéristique(s):")
            for n in self.puissances_exactes:
                print(nvar[0],"**",n," = ",self.puissances_exactes[n]," (exact)" if self.puissances_exactes[n].exact else " (approché)",sep='')
            for b in self.produits_exacts:
                print(nvar[0],"*",b[0],"=",b[1]," (exact)" if b[1].exact else " (approché)",)
        
    def __invert__(self): # précédé du signe ~
        return self.formel()


def sqrt_decimal(x,n=2): 
    """
    racine (carrée par defaut) d'un nombre de type decimal
    pour calculer une racine n ème, ajouter l'argument n de type int
    """
    if type(x)!=decimal: x=decimal(x)
    
    x.__simplification__()
    racine=decimal((x.num/(10**(x.puiss%n)))**(1/n))
    racine.puiss+=x.puiss//n
        
    racine.__simplification__()
        
    #verification de valeur exacte (par dernier chiffre du numérateur)
    
    racine.exact=x.exact
    
    puisscalculee=racine**n
    puisscalculee.__simplification__()
    
    if puisscalculee.puiss!=x.puiss or str(puisscalculee.num)[-1]!=str(int(str(racine.num)[-1])**2)[-1]: 
        racine.exact=False
        
        #mise en mémoire de la puissance m ème exacte du decimal
        racine.puissances_exactes[n]=x
    
        for m in x.puissances_exactes:
            racine.puissances_exactes[m*n]=x.puissances_exactes[m]
    
    #récuperation profonde des propriétés de x
    for couple in x.produits_exacts:
        racine.produits_exacts.append([sqrt(couple[0],n),sqrt(couple[1],n)])
        
    for m in x.puissances_exactes:
        racine.puissances_exactes[m]=sqrt(x.puissances_exactes[m],n)      
        
    return racine

def sqrt(x,n=2,conv_decimal=False):
    """
    extension de la fonction sqrt, pour tous types
    
    racine (carrée par defaut) d'un nombre de type decimal
    pour calculer une racine n ème, ajouter l'argument n de type int
    
    pour forcer le résultat decimal lorsque la valeur entrée est un flottant, effectuer l'appel avec conv_decimal=True
    """
    return sqrt_decimal(x,n) if (type(x)==decimal or conv_decimal) else private_sqrt_float(x) if n==2 else x**(1/n)
    

    
    
    
    
    
    
    
    