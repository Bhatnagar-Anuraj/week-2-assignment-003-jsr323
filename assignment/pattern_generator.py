"""
DIGM 131 - Assignment 2: Procedural Pattern Generator
======================================================

OBJECTIVE:
    Use loops and conditionals to generate a repeating pattern of 3D objects
    in Maya. You will practice nested loops, conditional logic, and
    mathematical positioning.

REQUIREMENTS:
    1. Use a nested loop (a loop inside a loop) to create a grid or pattern
       of objects.
    2. Include at least one conditional (if/elif/else) that changes an
       object's properties (type, size, color, or position offset) based
       on its row, column, or index.
    3. Generate at least 25 objects total (e.g., a 5x5 grid).
    4. Comment every major block of code explaining your logic.

GRADING CRITERIA:
    - [25%] Nested loop correctly generates a grid/pattern of objects.
    - [25%] Conditional logic visibly changes object properties based on
            position or index.
    - [20%] At least 25 objects are generated.
    - [15%] Code is well-commented with clear explanations.
    - [15%] Pattern is visually interesting and intentional.

TIPS:
    - A 5x5 grid gives you 25 objects. A 6x6 grid gives you 36.
    - Use the loop variables (row, col) to calculate X and Z positions.
    - The modulo operator (%) is great for alternating patterns:
          if col % 2 == 0:    # every other column
    - You can vary: primitive type, height, width, position offset, etc.

COMMENT HABITS (practice these throughout the course):
    - Add a comment before each logical section explaining its purpose.
    - Use inline comments sparingly and only when the code is not obvious.
    - Keep comments up to date -- if you change the code, update the comment.
"""

#Imports Maya Python command library and clears the scene
import maya.cmds as cmds

cmds.file(new=True, force=True)

def generate_pattern():

    num_rows = 5
    num_cols = 5
    spacing = 3.0

#Centering offset
#Shifts the grid so it is centered at (0, 0, 0)
    x_offset = (num_cols - 1) * spacing * 0.5
    z_offset = (num_rows - 1) * spacing * 0.5

    for row in range(num_rows):
        for col in range(num_cols):

#Apply centering offsets here also makes the name for the cubes and their colors
            x_pos = (col * spacing) - x_offset
            z_pos = (row * spacing) - z_offset

            cube_name = f"cube_row{row}_col{col}"
            obj = cmds.polyCube(name=cube_name)[0]
#(I did use AI to help me with understanding and making a material and hook it up so it can be used on geometry)
            shader = cmds.shadingNode("lambert", asShader=True, name=f"shader_{row}_{col}")
            shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True)
            cmds.connectAttr(shader + ".outColor", shading_group + ".surfaceShader")

#Center cube's scale, position, and color
            if row == 2 and col == 2:
                cmds.scale(2.0, 2.0, 2.0, obj)
                cmds.move(x_pos, 2.0, z_pos, obj)
                cmds.setAttr(shader + ".color", 0, 1, 1.5, type="double3")

#Diagonal cube's scale, position, and color
            elif row == col:
                cmds.scale(1.4, 1.4, 1.4, obj)
                cmds.move(x_pos, 0.5, z_pos, obj)
                cmds.setAttr(shader + ".color", 0, 1, 0.5, type="double3")

#Checkerboard cube's scale, position, and color
            elif (row + col) % 2 == 0:
                cmds.scale(1.1, 1.1, 1.1, obj)
                cmds.move(x_pos, 0.0, z_pos, obj)
                cmds.setAttr(shader + ".color", 0.2, 0.4, 1, type="double3")

#Default cube's scale, position, and color
            else:
                cmds.scale(0.7, 0.7, 0.7, obj)
                cmds.move(x_pos, -0.5, z_pos, obj)
                cmds.setAttr(shader + ".color", 0.8, 0.8, 0.8, type="double3")

            cmds.sets(obj, edit=True, forceElement=shading_group)

#Runs the generator and frames everything in the viewport
#Also makes a confirmation message!
generate_pattern()

cmds.viewFit(allObjects=True)
print("Centered grid generated successfully!")
