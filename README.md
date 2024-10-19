# MIRMI_2DOF_Drawing_Bot
 
This respository contains all the CAD files, firmware and API to build an use the 2 DOF drawing robot by MIRMI lab.

# API
Use the API to interface with the drawing robot system:

## Includes
First of, import the api and the predefined shapes via:
```
from drawing_bot_api import Drawing_bot
from drawing_bot_api import shapes
```

## Intialisation
To communication with the robot you need to create an instance of Drawing_bot class:
```
drawing_bot = Drawing_bot() # Creates an instance with default parameters
```
Parameters:
- unit: Changes the unit used to describe the robots position within the working area (default: 'mm') \
  options:
  * millimeter: 'mm'
  * centimeter: 'cm'
  * meter: 'm'
- speed: Changs the speed at which the drawing robot runs in unit/sec (default: 200)

```
# example
drawing_bot = Drawing_bot(unit='m', speed=400)
```

## Add shapes or move
To create a program sequence you add shapes to your instance of the Drawing_bot class.
```
# example
drawing_bot.add_shape(shapes.Line([20, 80], [40, 120]))
```

### Point

### Line
To draw a line use `shapes.Line(start_point, end_point)´
Parameters:
- start_point: Defines where the line should start
- end_point: Defines where the line should end
```
# example
shapes.Line([20, 80], [40, 120])
```



