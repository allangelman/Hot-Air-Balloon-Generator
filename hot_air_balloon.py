#hot_air_balloon.py
import maya.cmds as cmds
import functools
import math

def UI(pWindowTitle, makeMushroom):
    """
    Creating the user Interface to input various paramters to create a hot air balloon
    """
    windowID = 'Hot Air Balloon'
    
    if cmds.window(windowID, exists=True):
        cmds.deleteUI(windowID)
        
    #UI window  
    cmds.window(windowID, title = pWindowTitle, sizeable=True, resizeToFitChildren=True)
    cmds.rowColumnLayout(numberOfColumns=3, columnWidth=[(1,20), (2,200), (3,200)],
                         columnOffset = [(1,'right', 3)])
    
    #input fields
    cmds.separator(h=10,style='none')
    
    cmds.text(label='Basket Hieght: ')
    basketHeight = cmds.floatField()
    cmds.separator(h=10,style='none')
    
    cmds.text(label='Basket Radius: ')
    basketRadius = cmds.floatField()
    cmds.separator(h=10,style='none')
    
    cmds.text(label='# Basket SubdivisionsX: ')
    basketSubX = cmds.intSlider(min = 3, max = 20, value=3, step=1)
    cmds.separator(h=10,style='none')
    
    cmds.text(label='Wire Hieght: ')
    wireHieght = cmds.floatField()
    cmds.separator(h=10,style='none')
    
    cmds.text(label='# Balloon SubdivisionsX: ')
    balloonSubX = cmds.intSlider(min = 3, max = 20, value=3, step=1)
    cmds.separator(h=10,style='none')
    
    cmds.text(label='# Balloon SubdivisionsY: ')
    balloonSubY = cmds.intSlider(min = 3, max = 20, value=3, step=1)
    cmds.separator(h=10,style='none')
    
    cmds.text(label='Balloon Scaling Factor: ')
    balloonScale = cmds.intSlider(min = 2, max = 20, value=2, step=1)
    cmds.separator(h=10,style='none')
 
    
    #apply button calls makeMushroom
    cmds.button(label='Apply', command=functools.partial(makeBalloon, basketHeight, basketRadius, basketSubX, wireHieght, 
                                                            balloonSubX, balloonSubY, balloonScale))
    def cancelCallback(*pArgs):
        if cmds.window(windowID, exists=True):
            cmds.deleteUI(windowID)
    cmds.button(label='Cancel', command=cancelCallback)
    cmds.showWindow()


def makeBalloon(basketHeight, basketRadius, basketSubX, wireHieght, 
      balloonSubX, balloonSubY, balloonScale, *pArgs):
    
    """
    Constructing a hot air balloon model based on user input on a variety of parameters
    """
    #user input    
    basket_hieght = cmds.floatField(basketHeight, query=True,value = True)
    basket_radius = cmds.floatField(basketRadius, query=True,value = True)
    basket_sub_x = cmds.intSlider(basketSubX, query=True,value = True)
    wire_hieght = cmds.floatField(wireHieght, query=True,value = True)
    balloon_sub_x = cmds.intSlider(balloonSubX, query=True,value = True)
    balloon_sub_y = cmds.intSlider(balloonSubY, query=True,value = True)
    balloon_radius_factor = cmds.intSlider(balloonScale, query=True,value = True)
    
    basket_sub_y = 20
    balloon_radius = basket_radius * balloon_radius_factor
    
    #scaling wire radius based on basket size
    if basket_radius <=5:
        wire_radius = 0.05
    
    if basket_radius > 5:
        wire_radius = 0.1
        
    basket_thickness = wire_radius*5
    
    basket_inst = cmds.polyCylinder(n='basket#', sx = basket_sub_x, sy=basket_sub_y, r = basket_radius, h= basket_hieght)
    balloon_inst = cmds.polySphere(n='balloon#', sx = balloon_sub_x, sy=balloon_sub_y, r = balloon_radius)
    
    start_del = basket_sub_x * (basket_sub_y + 1)
    end_del = start_del + basket_sub_x - 1
    
    start_ext = 0
    end_ext = start_del
    cmds.delete( basket_inst[0] + '.f[' + str(start_del) + ':' + str(end_del) + ']')
    cmds.select( cl=True )
    
    #making basket thick
    cmds.polyExtrudeFacet( basket_inst[0] + '.f[' + str(start_ext) + ':' + str(end_ext) + ']', kft=True, ltz=basket_thickness)
    
    #moving balloon and basket
    center_angle = 360/basket_sub_x
    interior_angle = (((balloon_sub_y*2)-2)*180)/(balloon_sub_y*2)
    if balloon_sub_y<=10:
        balloon_move = balloon_radius - (basket_radius*1.1/math.tan(math.radians(0.5*interior_angle))) + basket_hieght + wire_hieght
    else:
        balloon_move = balloon_radius + basket_hieght + wire_hieght*0.75
    cmds.move(0, basket_hieght/2, 0, basket_inst[0])
    cmds.move(0, balloon_move, 0, balloon_inst[0])
    
    #making and posiitions wires
    center_angle = 360/basket_sub_x
    wire_y = wire_hieght/2 + basket_hieght;
    angle = 90
    sin_a = math.sin(math.radians(angle))
    cos_a = math.cos(math.radians(angle))
    
    wires = cmds.group(empty = True, name ="wires")
    wire_0 = cmds.polyCylinder(n='wire0', sx = 20, sy=20, r = wire_radius, h= wire_hieght)
    cmds.move(basket_radius*sin_a, wire_y, basket_radius*cos_a, wire_0[0])
    cmds.parent(wire_0, wires)
    for i in range(1, basket_sub_x):
        angle = angle + center_angle
        sin_a = math.sin(math.radians(angle))
        cos_a = math.cos(math.radians(angle))
        wire_inst = cmds.polyCylinder(n='wire#', sx = 20, sy=20, r = wire_radius, h= wire_hieght)
        cmds.move(basket_radius*sin_a, wire_y, basket_radius*cos_a, wire_inst[0])
        cmds.parent(wire_inst, wires)
    
    #goruping
    hotairballoon = cmds.group(empty = True, name ="Hot Air Balloon")
    cmds.parent(wires, hotairballoon)
    cmds.parent(basket_inst, hotairballoon)
    cmds.parent(balloon_inst, hotairballoon)
    
UI('Hot Air Balloon Input', makeBalloon)
    
