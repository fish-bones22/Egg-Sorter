## Sensitivity for image detection. 
## Lower means more sensitive 
rottenSensitivity = 65
dirtSensitivity   = 105

## Threshold to which egg will be categorized
rottenThresh = 80
dirtThresh   = 80

## Pins - BCD Mode
## Refer to https://hackster.imgix.net/uploads/image/file/48843/RP2_Pinout.png?auto=compress%2Cformat&w=680&h=510&fit=max
## for guidance
pushServoPin        = 4
laneServoLeftPin    = 17
laneServoRightPin   = 18
startButtonPin      = 27

## Servo lane angles in degrees
laneAngle = 45

## Crop area for image in case camera is repositioned
cropArea     = [0, 0, 1, 1]
