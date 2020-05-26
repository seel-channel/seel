import pygame, time
import numpy as np

pygame.init()

sizeCanva = widthCanva, heightCanva = 1000, 1000
nBloques_X, nBloques_Y = 30, 30

dimBW = (widthCanva  / nBloques_X)
dimBH = (heightCanva / nBloques_Y)

gameState = np.zeros((nBloques_X, nBloques_Y))
screen = pygame.display.set_mode(sizeCanva)
pygame.display.set_caption('Redstone a Python') 

tipoBloque = 0
bloquesLigeros = (0,1,2,5,6)
ejecucion = True

def pintarBloque():
    mouseClick = pygame.mouse.get_pressed()
                
    if sum(mouseClick) > 0 and tipoBloque != 0:
        posX, posY = pygame.mouse.get_pos()
        celX, celY = int(np.floor(posX / dimBW)), int(np.floor(posY / dimBH))
        
        #Pinta el bloque con click izquierdo, si no lo limpia
        if mouseClick[0]:
            if tipoBloque == 1 and newGameState[celX, celY] == 0: #Redstone
                newGameState[celX, celY] = 1
            elif tipoBloque == 3 and newGameState[celX, celY] == 0: #Lampara
                newGameState[celX, celY] = 3
            elif tipoBloque == 5 and newGameState[celX, celY] == 0: #Palanca
                newGameState[celX, celY] = 5  
            elif newGameState[celX, celY] == 5: #Palanca activar
                newGameState[celX, celY] = 6    
            elif newGameState[celX, celY] == 6: #Palanca desactivar
                newGameState[celX, celY] = 5
            elif tipoBloque == 7 and newGameState[celX, celY] == 0: #Piedra
                newGameState[celX, celY] = 7  
            elif tipoBloque == 8 and newGameState[celX, celY] == 0: #TNT
                newGameState[celX, celY] = 8  
            elif tipoBloque == 9 and newGameState[celX, celY] == 0: #Piston Izquierda
                newGameState[celX, celY] = 9
            #Rota el piston
            elif newGameState[celX, celY] == 9: #Piston Arriba
                newGameState[celX, celY] = 10
            elif newGameState[celX, celY] == 10: #Piston Derecha
                newGameState[celX, celY] = 11
            elif newGameState[celX, celY] == 11: #Piston Abajo
                newGameState[celX, celY] = 12
            elif newGameState[celX, celY] == 12: #Piston Izquierda
                newGameState[celX, celY] = 9
                
        else:
            newGameState[celX, celY] = 0


def obtenerVecinos():
    listaVecinos = []
    
    #Template: (ID, Coordenadas(x,y), Orientación)
    if newGameState[x - 1, y] != 0: #Izquierda
        listaVecinos.append([newGameState[x - 1, y], [x - 1, y], "izquierda"])
    
    if newGameState[x + 1, y] != 0: #Derecha
        listaVecinos.append([newGameState[x + 1, y], [x + 1, y], "derecha"])
        
    if newGameState[x, y - 1] != 0: #Arriba
        listaVecinos.append([newGameState[x, y - 1], [x, y - 1], "arriba"])
        
    if newGameState[x, y + 1] != 0: #Abajo
        listaVecinos.append([newGameState[x, y + 1], [x, y + 1], "abajo"])
        
    return listaVecinos 



def remplazarBloque(posX, posY, bloqueBuscar, bloqueRemplazar):
    if newGameState[posX - 1, posY] == bloqueBuscar: #Izquierda
        newGameState[posX - 1, posY] = bloqueRemplazar
        remplazarBloque(posX - 1, posY, bloqueBuscar, bloqueRemplazar)
    if newGameState[posX + 1, posY] == bloqueBuscar: #Derecha
        newGameState[posX + 1, posY] = bloqueRemplazar
        remplazarBloque(posX + 1, posY, bloqueBuscar, bloqueRemplazar)  
    if newGameState[posX, posY - 1] == bloqueBuscar: #Arriba
        newGameState[posX, posY - 1] = bloqueRemplazar
        remplazarBloque(posX, posY - 1, bloqueBuscar, bloqueRemplazar)   
    if newGameState[posX, posY + 1] == bloqueBuscar: #Abajo
        newGameState[posX, posY + 1] = bloqueRemplazar
        remplazarBloque(posX, posY + 1, bloqueBuscar, bloqueRemplazar)
   

#REDSTONE FUNCTIONS
def obtenerRedstoneOrientacion(redstoneVecinos, redstoneOrientacion, colorIntensidad):
    #Cambia la orientación de la Redstone
    if redstoneVecinos == 0:
        pygame.draw.polygon(screen, (colorIntensidad, 0, 0), bloquePequenoPosition, 0) #Punto solitario

    elif redstoneVecinos == 1:
        if "izquierda" in redstoneOrientacion or "derecha" in redstoneOrientacion: #Horizontal
            pygame.draw.polygon(screen, (colorIntensidad, 0, 0), redstonePosition1, 0)
        else: #Vertical
            pygame.draw.polygon(screen, (colorIntensidad, 0, 0), redstonePosition2, 0)

    elif redstoneVecinos == 2:
        if "izquierda" in redstoneOrientacion and "derecha" in redstoneOrientacion: #Horizontal
            pygame.draw.polygon(screen, (colorIntensidad, 0, 0), redstonePosition1, 0)
        elif "arriba" in redstoneOrientacion and "abajo" in redstoneOrientacion: #Vertical
            pygame.draw.polygon(screen, (colorIntensidad, 0, 0), redstonePosition2, 0)
        else:
            pygame.draw.polygon(screen, (colorIntensidad, 0, 0), redstonePosition3, 0) #Cruz

    else:
        pygame.draw.polygon(screen, (colorIntensidad, 0, 0), redstonePosition3, 0) #Cruz
        
        
#LÁMPARA FUNCTIONS      
def crearLampara():
    #Crea sus bordes
    pygame.draw.polygon(screen, lineColor, [bloquePosition[0], lamparaBorderPosition[0], lamparaBorderPosition[5], bloquePosition[3]], 0)
    pygame.draw.polygon(screen, lineColor, [bloquePosition[0], bloquePosition[1], lamparaBorderPosition[2], lamparaBorderPosition[7]], 0)
    pygame.draw.polygon(screen, lineColor, [lamparaBorderPosition[1], bloquePosition[1], bloquePosition[2], lamparaBorderPosition[4]], 0)
    pygame.draw.polygon(screen, lineColor, [lamparaBorderPosition[6], lamparaBorderPosition[3], bloquePosition[2], bloquePosition[3]], 0)
    #Crea las lineas conectoras de las esquinas del rombo con el borde
    pygame.draw.line(screen, lineColor, lamparaLineasPosition[0], lamparaLineasPosition[1], 3)
    pygame.draw.line(screen, lineColor, lamparaLineasPosition[2], lamparaLineasPosition[3], 3)
    pygame.draw.line(screen, lineColor, lamparaLineasPosition[4], lamparaLineasPosition[5], 3)
    pygame.draw.line(screen, lineColor, lamparaLineasPosition[6], lamparaLineasPosition[7], 3)
    #Crea el rombo del centro
    pygame.draw.line(screen, lineColor, lamparaLineasPosition[1], lamparaLineasPosition[3], 3)
    pygame.draw.line(screen, lineColor, lamparaLineasPosition[3], lamparaLineasPosition[5], 3)
    pygame.draw.line(screen, lineColor, lamparaLineasPosition[5], lamparaLineasPosition[7], 3)
    pygame.draw.line(screen, lineColor, lamparaLineasPosition[7], lamparaLineasPosition[1], 3)  
    

#TNT FUNCTIONS  
def crearExplosion(radio):
    posX1 = x - radio
    posY1 = y - radio
    posX2 = x + radio + 1
    posY2 = y + radio + 1
    
    newGameState[posX1:posX2, posY1:posY2] = 0


#PISTON FUNCTIONS
def pistonWood(p1, p2, p3, p4): #Mueve el trozo de madera cuando se estira el piston
    if obtenerVecinos():
        for bloqueVecino in obtenerVecinos():
            if bloqueVecino[0] != 2 and bloqueVecino[0] != 6:
                pygame.draw.polygon(screen, maderaColor, [p1, p2, p3, p4], 0)
    else:
        pygame.draw.polygon(screen, maderaColor, [p1, p2, p3, p4], 0)
   
    
def desplazarBloquesPiston(xRes, yRes, desplazo): #Mueve los 14 bloques en dirección del piston
    if newGameState[x + xRes, y + yRes] in bloquesLigeros:
        newGameState[x + xRes, y + yRes] = 0
    else:
        bloqueAdelante = []
        posicionBloque = 0
        
        if desplazo == "horizontal":
            for x2 in range(abs(xRes), 13): #Hace un lista de los 13 bloques adelantes
                if xRes > 0: #Se resta a x, pero si es positivo se tiene que sumar
                    x2 = -x2
                bloqueAdelante.append(newGameState[x-x2, y + yRes])
            for x2 in range(abs(xRes)+1, 13+1): #Desplaza los bloques hasta toparse con un bloque ligero
                if bloqueAdelante[posicionBloque] in bloquesLigeros:
                    break
                else:
                    if xRes > 0: #Se resta a x, pero si es positivo se tiene que sumar
                        x2 = -x2
                    newGameState[x-x2, y + yRes] = bloqueAdelante[posicionBloque]
                    posicionBloque += 1
                    
        else:
            for y2 in range(abs(yRes), 13): #Hace un lista de los 13 bloques adelantes
                if yRes > 0: #Se resta a y, pero si es positivo se tiene que sumar
                    y2 = -y2
                bloqueAdelante.append(newGameState[x + xRes, y-y2])
            for y2 in range(abs(yRes)+1, 13+1): #Desplaza los bloques hasta toparse con un bloque ligero
                if bloqueAdelante[posicionBloque] in bloquesLigeros:
                    break
                else:
                    if yRes > 0: #Se resta a y, pero si es positivo se tiene que sumar
                        y2 = -y2
                    newGameState[x + xRes, y-y2] = bloqueAdelante[posicionBloque]
                    posicionBloque += 1    
        newGameState[x + xRes, y + yRes] = 0
    
    
def moverPiston(orientacionPiston, direccionBloque): #Evalua de que lado esta el piston y después la dirrecion a la que apunta
    if direccionBloque == "izquierda": 
        if orientacionPiston == "izquierda":
            desplazarBloquesPiston(-2, 0, "horizontal")
            pygame.draw.polygon(screen, maderaColor, [(((x - 2) * dimBW)          , ((y) * dimBH)),  
                                                      (((x - 2) * dimBW) + dimBW/4, ((y) * dimBH)), 
                                                      (((x - 2) * dimBW) + dimBW/4, ((y + 1) * dimBH)),
                                                      (((x - 2) * dimBW)          , ((y + 1) * dimBH))], 0)
        elif orientacionPiston == "arriba":
            desplazarBloquesPiston(-1, -1, "vertical")
            pygame.draw.polygon(screen, maderaColor, [(((x - 1) * dimBW), ((y - 1) * dimBH)), 
                                                      (((x)     * dimBW), ((y - 1) * dimBH)), 
                                                      (((x)     * dimBW), ((y - 1) * dimBH) + dimBH/4),
                                                      (((x - 1) * dimBW), ((y - 1) * dimBH) + dimBH/4)], 0)
        elif orientacionPiston == "abajo":
            desplazarBloquesPiston(-1, 1, "vertical")
            pygame.draw.polygon(screen, maderaColor, [(((x - 1) * dimBW), ((y + 2) * dimBH) - dimBH/4), 
                                                      (((x)     * dimBW), ((y + 2) * dimBH) - dimBH/4), 
                                                      (((x)     * dimBW), ((y + 2) * dimBH)),
                                                      (((x - 1) * dimBW), ((y + 2) * dimBH))], 0)
            
    elif direccionBloque == "arriba":
        if orientacionPiston == "izquierda":
            desplazarBloquesPiston(-1, -1, "horizontal")
            pygame.draw.polygon(screen, maderaColor, [(((x - 1) * dimBW)          , ((y - 1) * dimBH)),  
                                                      (((x - 1) * dimBW) + dimBW/4, ((y - 1) * dimBH)), 
                                                      (((x - 1) * dimBW) + dimBW/4, ((y)     * dimBH)),
                                                      (((x - 1) * dimBW)          , ((y)     * dimBH))], 0)
        elif orientacionPiston == "arriba":
            desplazarBloquesPiston(0, -2, "vertical")
            pygame.draw.polygon(screen, maderaColor, [(((x)     * dimBW), ((y - 2) * dimBH)), 
                                                      (((x + 1) * dimBW), ((y - 2) * dimBH)), 
                                                      (((x + 1) * dimBW), ((y - 2) * dimBH) + dimBH/4),
                                                      (((x)     * dimBW), ((y - 2) * dimBH) + dimBH/4)], 0)
        elif orientacionPiston == "derecha":
            desplazarBloquesPiston(1, -1, "horizontal")
            pygame.draw.polygon(screen, maderaColor, [(((x + 2) * dimBW) - dimBW/4, ((y - 1) * dimBH)), 
                                                      (((x + 2) * dimBW)          , ((y - 1) * dimBH)), 
                                                      (((x + 2) * dimBW)          , ((y)     * dimBH) ),
                                                      (((x + 2) * dimBW) - dimBW/4, ((y)     * dimBH) )], 0)
            
    elif direccionBloque == "derecha":
        if orientacionPiston == "arriba":
            desplazarBloquesPiston(1, -1, "vertical")
            pygame.draw.polygon(screen, maderaColor, [(((x + 1) * dimBW), ((y - 1) * dimBH)), 
                                                      (((x + 2) * dimBW), ((y - 1) * dimBH)), 
                                                      (((x + 2) * dimBW), ((y - 1) * dimBH) + dimBH/4),
                                                      (((x + 1) * dimBW), ((y - 1) * dimBH) + dimBH/4)], 0)
        elif orientacionPiston == "derecha":
            desplazarBloquesPiston(2, 0, "horizontal")
            pygame.draw.polygon(screen, maderaColor, [(((x + 3) * dimBW) - dimBW/4, ((y)     * dimBH)),  
                                                      (((x + 3) * dimBW)          , ((y)     * dimBH)), 
                                                      (((x + 3) * dimBW)          , ((y + 1) * dimBH)),
                                                      (((x + 3) * dimBW) - dimBW/4, ((y + 1) * dimBH))], 0)
        elif orientacionPiston == "abajo":
            desplazarBloquesPiston(1, 1, "vertical")
            pygame.draw.polygon(screen, maderaColor, [(((x + 1) * dimBW), ((y + 2) * dimBH) - dimBH/4), 
                                                      (((x + 2) * dimBW), ((y + 2) * dimBH) - dimBH/4), 
                                                      (((x + 2) * dimBW), ((y + 2) * dimBH)),
                                                      (((x + 1) * dimBW), ((y + 2) * dimBH))], 0)
            
    elif direccionBloque == "abajo":
        if orientacionPiston == "izquierda":
            desplazarBloquesPiston(-1, 1, "horizontal")
            pygame.draw.polygon(screen, maderaColor, [(((x - 1) * dimBW)          , ((y + 1) * dimBH)),  
                                                      (((x - 1) * dimBW) + dimBW/4, ((y + 1) * dimBH)), 
                                                      (((x - 1) * dimBW) + dimBW/4, ((y + 2) * dimBH)),
                                                      (((x - 1) * dimBW)          , ((y + 2) * dimBH))], 0)
        elif orientacionPiston == "abajo":
            desplazarBloquesPiston(0, 2, "vertical")
            pygame.draw.polygon(screen, maderaColor, [(((x)     * dimBW), ((y + 3) * dimBH) - dimBH/4), 
                                                      (((x + 1) * dimBW), ((y + 3) * dimBH) - dimBH/4), 
                                                      (((x + 1) * dimBW), ((y + 3) * dimBH)),
                                                      (((x)     * dimBW), ((y + 3) * dimBH))], 0)
        elif orientacionPiston == "derecha":
            desplazarBloquesPiston(1, 1, "horizontal")
            pygame.draw.polygon(screen, maderaColor, [(((x + 2) * dimBW) - dimBW/4, ((y + 1) * dimBH)), 
                                                      (((x + 2) * dimBW)          , ((y + 1) * dimBH)), 
                                                      (((x + 2) * dimBW)          , ((y + 2) * dimBH)),
                                                      (((x + 2) * dimBW) - dimBW/4, ((y + 2) * dimBH))], 0)
   

"""Ejecuta en búcle el juego"""         
while ejecucion:
    newGameState = np.copy(gameState)
    
    #Colores 
    backgroundColor = (248, 248, 248)
    piedraColor = (128,128,128)
    maderaColor = (92, 45, 12)
    negroColor = (0, 0, 0)
    lineColor = (38, 8, 1)
    
    screen.fill(backgroundColor)
    
    
    
    """Cambia de bloque al presionar su número"""
    for event in pygame.event.get():   
        if event.type == pygame.QUIT: #Cerrar programa
            ejecucion = False
            
        if event.type == pygame.KEYDOWN: #Detecta si selecciona un color
            if event.key == pygame.K_1: #Redstone
                tipoBloque = 1
            elif event.key == pygame.K_2: #Lámpara
                tipoBloque = 3
            elif event.key == pygame.K_3: #Palanca
                tipoBloque = 5
            elif event.key == pygame.K_4: #Piedra
                tipoBloque = 7
            elif event.key == pygame.K_5: #TNT
                tipoBloque = 8
            elif event.key == pygame.K_6: #Piston
                tipoBloque = 9
            else:
                tipoBloque = 0
        pintarBloque()   
            
    
    
    
    
    for x in range(0, nBloques_X):
        for y in range(0, nBloques_Y):
            """Evalua todos los bloques de la rejilla"""
            "sjsdsdksjdjsdsdsdjj"
    
    
    
    
    
            
    for x in range(0, nBloques_X):
        for y in range(0, nBloques_Y):
            """Crea los diseños de los bloques (posiciones del poligono)"""
            #Crea el bloque
            bloquePosition = [((x)     * dimBW, (y)     * dimBH), 
                              ((x + 1) * dimBW, (y)     * dimBH),
                              ((x + 1) * dimBW, (y + 1) * dimBH),
                              ((x)     * dimBW, (y + 1) * dimBH)]
                              
            #Crea el bloque pequeño
            bloquePequenoPosition = [(((x)     * dimBW) + dimBW/4, ((y)     * dimBH) + dimBH/4), 
                                     (((x + 1) * dimBW) - dimBW/4, ((y)     * dimBH) + dimBH/4), 
                                     (((x + 1) * dimBW) - dimBW/4, ((y + 1) * dimBH) - dimBH/4),
                                     (((x)     * dimBW) + dimBW/4, ((y + 1) * dimBH) - dimBH/4)]

            #Crea la redstone en horizontal
            redstonePosition1 = [(((x + 1) * dimBW), ((y + 1) * dimBH) - dimBH/3), 
                                 (((x + 1) * dimBW), ((y)     * dimBH) + dimBH/3), 
                                 (((x)     * dimBW), ((y)     * dimBH) + dimBH/3), 
                                 (((x)     * dimBW), ((y + 1) * dimBH) - dimBH/3)]
            
            #Crea la redstone en vertical
            redstonePosition2 = [(((x + 1) * dimBW) - dimBW/3, ((y + 1) * dimBH)), 
                                 (((x + 1) * dimBW) - dimBW/3, ((y)     * dimBH)), 
                                 (((x)     * dimBW) + dimBW/3, ((y)     * dimBH)), 
                                 (((x)     * dimBW) + dimBW/3, ((y + 1) * dimBH))]
            
            #Crea la redstone en cruz (instersección)
            redstonePosition3 = [(((x)     * dimBW) + dimBW/3, ((y)     * dimBH)),
                                 (((x)     * dimBW) + dimBW/3, ((y)     * dimBH) + dimBH/3),
                                 (((x)     * dimBW)          , ((y)     * dimBH) + dimBH/3),
                                 (((x)     * dimBW)          , ((y + 1) * dimBH) - dimBH/3),
                                 (((x)     * dimBW) + dimBW/3, ((y + 1) * dimBH) - dimBH/3),
                                 (((x)     * dimBW) + dimBW/3, ((y + 1) * dimBH)),
                                 (((x + 1) * dimBW) - dimBW/3, ((y + 1) * dimBH)),
                                 (((x + 1) * dimBW) - dimBW/3, ((y + 1) * dimBH) - dimBH/3),
                                 (((x + 1) * dimBW)          , ((y + 1) * dimBH) - dimBH/3),
                                 (((x + 1) * dimBW)          , ((y)     * dimBH) + dimBH/3),
                                 (((x + 1) * dimBW) - dimBW/3, ((y)     * dimBH) + dimBH/3),
                                 (((x + 1) * dimBW) - dimBW/3, ((y)     * dimBH))]
            
            #Crea el borde de la lámpara
            lamparaBorderPosition = [(((x)     * dimBW) + dimBW/8, ((y)     * dimBH)), 
                                     (((x + 1) * dimBW) - dimBW/8, ((y)     * dimBH)), 
                                     (((x + 1) * dimBW)          , ((y)     * dimBH) + dimBH/8),
                                     (((x + 1) * dimBW)          , ((y + 1) * dimBH) - dimBH/8),
                                     (((x + 1) * dimBW) - dimBW/8, ((y + 1) * dimBH)),
                                     (((x)     * dimBW) + dimBW/8, ((y + 1) * dimBH)),
                                     (((x)     * dimBW)          , ((y + 1) * dimBH) - dimBH/8),
                                     (((x)     * dimBW)          , ((y)     * dimBH) + dimBH/8)]
            
            #Crea los detalles de la lámpara
            lamparaLineasPosition = [(((x)     * dimBW) + dimBW/2, ((y)     * dimBH)), 
                                     (((x)     * dimBW) + dimBW/2, ((y)     * dimBH) + dimBH/4), 
                                     (((x + 1) * dimBW)          , ((y)     * dimBH) + dimBH/2),
                                     (((x + 1) * dimBW) - dimBW/4, ((y)     * dimBH) + dimBH/2),
                                     (((x)     * dimBW) + dimBW/2, ((y + 1) * dimBH)),
                                     (((x)     * dimBW) + dimBW/2, ((y + 1) * dimBH) - dimBH/4),
                                     (((x)     * dimBW)          , ((y)     * dimBH) + dimBH/2),
                                     (((x)     * dimBW) + dimBW/4, ((y)     * dimBH) + dimBH/2)]
            
            #Crea la palanca apagada
            palancaPositionOn = [(((x)     * dimBW) + dimBW/16, ((y + 1) * dimBH) - dimBH/2.5), 
                                 (((x)     * dimBW) + dimBW/16, ((y)     * dimBH) + dimBH/2.5), 
                                 (((x + 1) * dimBW) - dimBW/2 , ((y)     * dimBH) + dimBH/2.5), 
                                 (((x + 1) * dimBW) - dimBW/2 , ((y + 1) * dimBH) - dimBH/2.5)]
            
            #Crea la palanca encendida
            palancaPositionOff = [(((x)     * dimBW) + dimBW/2 , ((y + 1) * dimBH) - dimBH/2.5), 
                                  (((x)     * dimBW) + dimBW/2 , ((y)     * dimBH) + dimBH/2.5), 
                                  (((x + 1) * dimBW) - dimBW/16, ((y)     * dimBH) + dimBH/2.5), 
                                  (((x + 1) * dimBW) - dimBW/16, ((y + 1) * dimBH) - dimBH/2.5)]
            
            #Crea la primeta T de TNT
            tntLetraTPosition = [(((x) * dimBW) + dimBW/8, ((y) * dimBH) + dimBH/2.5),
                                 (((x) * dimBW) + dimBW/4, ((y) * dimBH) + dimBH/2.5),
                                 (((x) * dimBW) + dimBW/5, ((y) * dimBH) + dimBH/2.5),
                                 (((x) * dimBW) + dimBW/5, ((y + 1) * dimBH) - dimBH/2.5)]
            
            #Crea la N del centro de TNT
            tntLetraNPosition = [(((x)     * dimBW) + dimBW/2.5, ((y)     * dimBH) + dimBH/2.5),
                                 (((x)     * dimBW) + dimBW/2.5, ((y + 1) * dimBH) - dimBH/2.5),
                                 (((x + 1) * dimBW) - dimBW/2.5, ((y)     * dimBH) + dimBH/2.5),
                                 (((x + 1) * dimBW) - dimBW/2.5, ((y + 1) * dimBH) - dimBH/2.5)]     
            
            #Crea la segunda T de TNT
            tntLetraT2Position = [(((x + 1) * dimBW) - dimBW/8, ((y)     * dimBH) + dimBH/2.5),
                                  (((x + 1) * dimBW) - dimBW/4, ((y)     * dimBH) + dimBH/2.5),
                                  (((x + 1) * dimBW) - dimBW/5, ((y)     * dimBH) + dimBH/2.5),
                                  (((x + 1) * dimBW) - dimBW/5, ((y + 1) * dimBH) - dimBH/2.5)]

            #Crea el piston (posiciones)
            pistonPosition = [(((x)     * dimBW) + dimBW/4, ((y)     * dimBH)), 
                              (((x + 1) * dimBW) - dimBW/4, ((y)     * dimBH)), 
                              (((x + 1) * dimBW)          , ((y)     * dimBH) + dimBH/4),
                              (((x + 1) * dimBW)          , ((y + 1) * dimBH) - dimBH/4),
                              (((x + 1) * dimBW) - dimBW/4, ((y + 1) * dimBH)),
                              (((x)     * dimBW) + dimBW/4, ((y + 1) * dimBH)),
                              (((x)     * dimBW)          , ((y + 1) * dimBH) - dimBH/4),
                              (((x)     * dimBW)          , ((y)     * dimBH) + dimBH/4)]
            
        
        
            """Crea los bloques y sus comportamientos"""
            #Pintar el bloque
            if newGameState[x, y] == 0: #Aire
                pygame.draw.polygon(screen, (150, 150, 150), bloquePosition, 1)
                        
            #Redstone
            elif newGameState[x, y] == 1: 
                redstoneVecinos = 0
                redstoneOrientacion = []
                for bloqueVecino in obtenerVecinos(): #Obtiene los vecinos de Redstone
                    if bloqueVecino[0] == 1:
                        redstoneVecinos += 1
                        redstoneOrientacion.append(bloqueVecino[2])
                    elif bloqueVecino[0] == 4:
                        newGameState[bloqueVecino[1][0], bloqueVecino[1][1]] = 3 #Apaga la lámpara
                        remplazarBloque(bloqueVecino[1][0], bloqueVecino[1][1], 4, 3)
                obtenerRedstoneOrientacion(redstoneVecinos, redstoneOrientacion, 128)


            #Redstone activada
            elif newGameState[x, y] == 2: 
                redstoneVecinos = 0
                redstoneOrientacion = []
                for bloqueVecino in obtenerVecinos(): 
                    if bloqueVecino[0] == 1: #Enciende la redstone
                        newGameState[bloqueVecino[1][0], bloqueVecino[1][1]] = 2  
                    elif bloqueVecino[0] == 2: #Obtiene vecinos de Redstone Activa
                        redstoneVecinos += 1
                        redstoneOrientacion.append(bloqueVecino[2])
                    elif bloqueVecino[0] == 3: #Enciende la lámpara
                        newGameState[bloqueVecino[1][0], bloqueVecino[1][1]] = 4
                    elif bloqueVecino[0] == 8: #Enciende la TNT
                        crearExplosion(4)
                    elif bloqueVecino[0] == 9: #Mueve el piston
                        moverPiston("izquierda", bloqueVecino[2])
                    elif bloqueVecino[0] == 10: #Mueve el piston
                        moverPiston("arriba", bloqueVecino[2])
                    elif bloqueVecino[0] == 11: #Mueve el piston
                        moverPiston("derecha", bloqueVecino[2])
                    elif bloqueVecino[0] == 12: #Mueve el piston
                        moverPiston("abajo", bloqueVecino[2])
                obtenerRedstoneOrientacion(redstoneVecinos, redstoneOrientacion, 200)
            
            
            #Lámpara
            elif newGameState[x, y] == 3:  
                pygame.draw.polygon(screen, (140, 60, 30), bloquePosition, 0)
                crearLampara()

            #Lámpara activada
            elif newGameState[x, y] == 4:  
                pygame.draw.polygon(screen, (220, 140, 50), bloquePosition, 0)
                crearLampara()
            
            
            #Palanca desactivada
            elif newGameState[x, y] == 5: 
                pygame.draw.polygon(screen, piedraColor, bloquePequenoPosition, 0)
                pygame.draw.polygon(screen, maderaColor, palancaPositionOn, 0)
                for bloqueVecino in obtenerVecinos(): #Busca los vecinos
                    if bloqueVecino[0] == 2:
                        newGameState[bloqueVecino[1][0], bloqueVecino[1][1]] = 1 #Apaga la redstone
                        remplazarBloque(bloqueVecino[1][0], bloqueVecino[1][1], 2, 1)
                    elif bloqueVecino[0] == 4:
                        newGameState[bloqueVecino[1][0], bloqueVecino[1][1]] = 3 #Apaga la lámpara
                        remplazarBloque(bloqueVecino[1][0], bloqueVecino[1][1], 4, 3)


            #Palanca activada
            elif newGameState[x, y] == 6: 
                pygame.draw.polygon(screen, (130, 160, 160), bloquePequenoPosition, 0)
                pygame.draw.polygon(screen, maderaColor, palancaPositionOff, 0)
                for bloqueVecino in obtenerVecinos(): #Busca los vecinos
                    if bloqueVecino[0] == 1:
                        newGameState[bloqueVecino[1][0], bloqueVecino[1][1]] = 2 #Enciende la redstone
                        remplazarBloque(bloqueVecino[1][0], bloqueVecino[1][1], 1, 2)
                    elif bloqueVecino[0] == 3:
                        newGameState[bloqueVecino[1][0], bloqueVecino[1][1]] = 4 #Enciende la lámpara
                    elif bloqueVecino[0] == 8: #Enciende la TNT
                        crearExplosion(4)
                    elif bloqueVecino[0] == 9: #Mueve el piston
                        moverPiston("izquierda", bloqueVecino[2])
                    elif bloqueVecino[0] == 10: #Mueve el piston
                        moverPiston("arriba", bloqueVecino[2])
                    elif bloqueVecino[0] == 11: #Mueve el piston
                        moverPiston("derecha", bloqueVecino[2])
                    elif bloqueVecino[0] == 12: #Mueve el piston
                        moverPiston("abajo", bloqueVecino[2])
                    
                    
            #Piedra
            elif newGameState[x, y] == 7:  
                pygame.draw.polygon(screen, piedraColor, bloquePosition, 0)
            
            #TNT
            elif newGameState[x, y] == 8:  
                pygame.draw.polygon(screen, (190, 60, 25), bloquePosition, 0)
                pygame.draw.polygon(screen, (220, 220, 220), redstonePosition1, 0)
                pygame.draw.line(screen, negroColor, tntLetraTPosition[0], tntLetraTPosition[1], 1) #Crea la letra T
                pygame.draw.line(screen, negroColor, tntLetraTPosition[2], tntLetraTPosition[3], 1)
                pygame.draw.line(screen, negroColor, tntLetraNPosition[0], tntLetraNPosition[1], 1) #Crea la letra N
                pygame.draw.line(screen, negroColor, tntLetraNPosition[0], tntLetraNPosition[3], 1)
                pygame.draw.line(screen, negroColor, tntLetraNPosition[2], tntLetraNPosition[3], 1)
                pygame.draw.line(screen, negroColor, tntLetraT2Position[0], tntLetraT2Position[1], 1) #Crea la letra T
                pygame.draw.line(screen, negroColor, tntLetraT2Position[2], tntLetraT2Position[3], 1)
            
    
            #Piston Izquierda
            elif newGameState[x, y] == 9:  
                pygame.draw.polygon(screen, piedraColor, [pistonPosition[0], bloquePosition[1], bloquePosition[2], pistonPosition[5]], 0)
                pistonWood(bloquePosition[0], pistonPosition[0], pistonPosition[5], bloquePosition[3])


            #Piston Arriba
            elif newGameState[x, y] == 10:
                pygame.draw.polygon(screen, piedraColor, [pistonPosition[7], pistonPosition[2], bloquePosition[2], bloquePosition[3]], 0)
                pistonWood(bloquePosition[0], bloquePosition[1], pistonPosition[2], pistonPosition[7])

            #Piston Derecha
            elif newGameState[x, y] == 11:
                pygame.draw.polygon(screen, piedraColor, [bloquePosition[0], pistonPosition[1], pistonPosition[4], bloquePosition[3]], 0)
                pistonWood(pistonPosition[1], bloquePosition[1], bloquePosition[2], pistonPosition[4])
                    
            #Piston Abajo
            elif newGameState[x, y] == 12:  
                pygame.draw.polygon(screen, piedraColor, [bloquePosition[0], bloquePosition[1], pistonPosition[3], pistonPosition[6]], 0)
                pistonWood(pistonPosition[6], pistonPosition[3], bloquePosition[2], bloquePosition[3])

                
                
    #Actualiza la pantalla
    gameState = np.copy(newGameState)
    pygame.display.flip()
    
pygame.quit() 
    
    
    
    
    
    
    
    
    
    
    
    