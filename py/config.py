## Sensitivity for image detection. 
## Lower means more sensitive 
rottenSensitivity = 83
dirtSensitivity   = 10

## Threshold to which egg will be categorized
rottenThresh = 75
dirtThresh   = 20

## Pins - BCD Mode
## Refer to https://hackster.imgix.net/uploads/image/file/48843/RP2_Pinout.png?auto=compress%2Cformat&w=680&h=510&fit=max
## for guidance
pushServoPin        = 4
laneServoLeftPin    = 17
laneServoRightPin   = 18
startButtonPin      = 27

# button pin
buttonPin = 22

## Servo angles in degrees
laneAngle = 45
pushAngle = 90
returnAngle = 90

## Crop area for image in case camera is repositioned
cropArea     = [0.18, 0.35, 0.54, 0.54]
