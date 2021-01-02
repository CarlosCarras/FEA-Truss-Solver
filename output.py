
from __future__ import division

OUT_EXT = "sol"

def get_comments(filename):
    file = open(filename, "r")
    comments = None

    for line in file:
        buffer = file.readline().split(":", 1)[0]
        if buffer == "Comments":
            comments = file.readlines()
            break

    file.close()
    return comments


def gen_output(filename, element_type, units, u):
    comments = get_comments(filename)
    file = open(filename+OUT_EXT, "w+")

    file.write("Element Type: %s\n" % element_type)
    file.write("Units: %s\n\n" % units)

    for i in range(len(u)):
        if i%2 == 0: out_str = "u"
        else: out_str = "v"
        
        out_str += str(i // 2 + 1) + " = {0}\n"
        file.write(out_str.format(float(u[i])))

    file.write("\nComments:\n")
    for line in comments:
        file.write(line)

    file.close()


def disp_output(filename, element_type, units, u):
    print("Filename: {0:s}\nElement Type: {1:s}\nUnits: {2:s}\n".format(filename, element_type, units))

    for i in range(len(u)):
        if i%2 == 0: out_str = "u"
        else: out_str = "v"
        out_str += str(i // 2 + 1) + " = {0}"
        print(out_str.format(float(u[i])))
