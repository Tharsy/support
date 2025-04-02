from random import randint

outf = open("featureplacement_set.lua", "w")
fdef = None
fx = None
fz = None
fy = None

def ex(s, k):
    return s.partition(k)[2].strip().strip(',').strip()

# Define the desired output range for rotation values
min_target = -32768
max_target = 32767

# Define the source range for radians, typically -π to π
min_source = -3.141592653589793  # -π
max_source = 3.141592653589793   # π

# Calculate the scaling factor based on the source and target ranges
scaling_factor = (max_target - min_target) / (max_source - min_source)

# Calculate the offset for the target range mapping
offset = min_target - min_source * scaling_factor

for line in open('model.lua').readlines():
    if 'defName = ' in line:
        fdef = ex(line, " defName = ")
    if ' pos = {' in line:
        fx = 0
        fz = 0
    if fx == 0 or fz == 0:
        if ' x = ' in line:
            fx = int(float(ex(line, " x = ")))
        if ' z = ' in line:
            fz = int(float(ex(line, " z = ")))
    if ' rot = {' in line:
        fy = 0
    if fy == 0 and ' y = ' in line:
        fy = float(ex(line, " y = "))  # Extract the original rotation value in radians
        # Apply the scaling factor and offset to map the source radians value to the target integer range
        fy = fy * scaling_factor + offset
        fy = int(round(fy))  # Round to nearest integer and convert to int
        o = '{ name = %s, x = %d, z = %d, rot = %d },' % (fdef, fx, fz, fy)  # Format as integer
        print(o)
        outf.write(o + '\n')
        fdef = None
        fx = None
        fz = None
        fy = None

outf.close()

