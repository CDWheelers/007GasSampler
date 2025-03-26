import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm 

# radius of Erf
r = 1

# Initialize empty arrays
x_arr = np.array([])            # x-coord array
y_arr = np.array([])            # y-coord array
z_arr = np.array([])            # z-coord array
conc_arr = np.array([])         #concentration array
conc_norm_arr = np.array([])    #normalized concentration array
color_arr = np.array([])        #color array

# Open collected data
# Convert lat and long to cartesian coordinates
# Populate arrays

f = open('data.txt','r')
print('Reading latitude and longitude data\n')

while True:
    line = f.readline()
    if not line:
        break
    else:
        #print(line[24:33] + ' ' + line[35:46] + '\n')
        lat = float(line[24:33])
        long = float(line[35:46])
        conc = float(line[48:56])
        
        x = long
        y = lat

        # x = r*math.sin(math.radians(lat))*math.cos(math.radians(long))
        # y = r*math.sin(math.radians(long))*math.sin(math.radians(lat))
        # z = r*math.cos(math.radians(lat))

        z = 0

        if (x_arr.size == 0):
            x_arr = np.array([x])
        if (y_arr.size == 0):
            y_arr = np.array([y])
        if (z_arr.size == 0):
            z_arr = np.array([z])
        if (conc_arr.size == 0):
            conc_arr = np.array([conc])

        else:
            x_arr = np.append(x_arr, x)
            y_arr = np.append(y_arr, y)
            z_arr = np.append(z_arr, z)
            conc_arr = np.append(conc_arr, conc)
            
f.close()

# Normalize concentration array [0,1]
for member in conc_arr:
    conc_norm_arr = np.append(conc_norm_arr,(member-conc_arr.min())/(conc_arr.max()-conc_arr.min()))

# Use a continuous colormap
colormap = cm.get_cmap('YlOrRd')  # or 'plasma', 'inferno', 'hot', etc.
color_arr = colormap(conc_norm_arr)

fig, ax = plt.subplots()
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

"""
# Create color codes for normalized values
for member in conc_norm_arr:
    if (member < 0.25):
        color_arr = np.append(color_arr,'green')
    elif ((member > 0.25) and (member < 0.50)):
        color_arr = np.append(color_arr,'yellow')
    elif ((member > 0.50) and (member < 0.75)):
        color_arr = np.append(color_arr,'orange')
    elif (member > 0.75):
        color_arr = np.append(color_arr,'red')
"""

# Plot data
plt.scatter(x_arr, y_arr, c=color_arr, marker='o')

ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
plt.show()

"""
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x_arr, y_arr, z_arr, c=color_arr, marker='o')
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
plt.show()
"""