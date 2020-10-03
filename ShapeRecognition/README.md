This project is a creative approach at shape recognition in images.
As oppose to the traditional method of classifying the features of each geometric shape, I decided to find the center point of each shape,
calculate the radius of each point and then graph the radius over the degree of rotation which in all cases is 2 pi or 360 degrees. 
I then analyzed each graph and found that they all create polynomial functions. I determined that the best way to classify the graphs would
be to use the number of minimum points and local minimum points. I created a function that was able to find whether a point is a minimum 
using the x and y coordinates and then compared that to the actual min values of the function (to a degree of accuracy) to determine which 
points are absolute minimum and which are local min.

NOTE: the program can identify a shape if it is listed :
[Square, Rectangle, Circle, Equalateral Triangle, Non-Equalateral Triangle, Pentagon,
Hexagon, Heptagon, Octagon, Nonagon, Decagon]

Constraints:
- It cannot identify other shapes but if the local minimums were further analyzed it could identify any shape.
- I only coded black and white background processing so the background must be black or white

See image files for photos of the graphs representing each shapes 
