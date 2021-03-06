""" Mini Project #2: Computational Art
Software Design Spring 2017
Gracey Wilson """

import random
from random import choice
from PIL import Image
import math

def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """
    depth = random.randint(min_depth,max_depth)
    f_options = ['prod','avg','cos_pi','sin_pi','squared']
    f_chosen = choice(f_options)
    f = []

    if min_depth == 1:
        return choice([['x'],['y']])
    else:
        f.append(f_chosen)
        if f_chosen == 'prod' or f_chosen == 'avg':
            f.append(build_random_function(min_depth-1,max_depth-1))
            f.append(build_random_function(min_depth-1,max_depth-1))
        else:
            f.append(build_random_function(min_depth-1,max_depth-1))
        return f

def evaluate_random_function(f, x, y):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
    """
    if f[0] == 'x':
        return x
    elif f[0] == 'y':
        return y
    elif f[0] == 'prod':
        return evaluate_random_function(f[1], x, y) * evaluate_random_function(f[2], x, y)
    elif f[0] == 'squared':
        return evaluate_random_function(f[1],x,y)**2
    elif f[0] == "avg":
        return 0.5 * (evaluate_random_function(f[1], x, y) + (
            evaluate_random_function(f[2], x, y)))
    elif f[0] == "cos_pi":
        return math.cos(math.pi * evaluate_random_function(f[1], x, y))
    elif f[0] == "sin_pi":
        return math.sin(math.pi * evaluate_random_function(f[1], x, y))
    else:
        print('Please try again')

def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_interval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """

    old_ratio = (val - input_interval_start) / (input_interval_end - input_interval_start)
    output = output_interval_end - output_interval_start
    new_val = (old_ratio * output) + output_interval_start
    return new_val

def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    # im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(1,4)
    green_function = build_random_function(5,7)
    blue_function = build_random_function(1,2)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)),
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y))
                    )

    im.save(filename)

def get_an_uncontroversial_name():
    """ Find a filename that doesn't to not overwrite existing art.

        Do this in a roudabout way of finding all the current art files that
        follow a convention of base_string + an_int + extension, finding the
        largest an_int, and +1-ing that to get the returned filename.

        The irony of this is that in the process of writing
        and testing this function many arts were created and overwritten.

         - Evan Lloyd New-Schmidt (@newsch)

        returns: filename as a string
    """
    import glob
    base_string = 'myart'  # prefix for filenames
    extension = '.png'
    files = glob.glob('myart*.png')  # get all files that match the pattern
    # parse number out of filename and get biggest one
    big_int = 1
    for file in files:
        int_begin = len(base_string)
        int_end = file.find(extension)
        new_int = file[int_begin:int_end]
        # check to make sure this is really an int and if it's bigger or not
        if new_int.isdigit():
            new_int = int(new_int)
            if new_int > big_int:
                big_int = new_int

    bigger_int = big_int + 1  # make a bigger int for the new filename
    an_uncontroversial_filename = base_string + str(bigger_int) + extension
    return(an_uncontroversial_filename)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    generate_art(get_an_uncontroversial_name())

    # Test that PIL is installed correctly
    # test_image("noise.png")
