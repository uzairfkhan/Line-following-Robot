Working Principle
1.	Initialization:
Establishes a connection with the same Access Point (AP) as the laptop.
2.	Command Reception:
Waits for a starting command from Python code(Motor Speed).
3.	Line Following Algorithm:
Adjusts direction based on feedback from IR sensors to stay on the line.
4.	Alignment of Red Patch with Green Patch:
Employs computer vision to identify the red and green patches on the map.
Adjusts the direction of the LFR until the red & orange patches align horizontally with the green patch.
5.	Line Creation:
Calculates a straight line originating from the red and orange patches on the LFR.
6.	Rotation Towards Intersection:
Rotate the LFR until the line intersects with the identified green patch on the map.
7.	Movement Along Straight Line:
Follows the calculated straight line towards the green patch.
8.	Stop at Green Patch:
Halts the LFR's movement when the distance between Red and Green patch is minimal.
