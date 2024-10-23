import matplotlib.pyplot as plt
import pandas as pd
import yaml

# Read schedule from YAML file
with open('schedule.yaml', 'r') as file:
    data = yaml.safe_load(file)

# Create a DataFrame from the data
df = pd.DataFrame(data, columns=['Day', 'Start', 'End', 'ClassName', 'ClassNumber', 'Room'])

# Create a list of unique classes 
unique_classes = list(set(df['ClassName'])) 

# Read the all the colors from the YAML file
with open('colors.yaml', 'r') as file:
    colors_data = yaml.safe_load(file)

# Ensure colors_data is a list of colors
colors_list = colors_data if isinstance(colors_data, list) else list(colors_data.values())

# Create a map with the class and colors, cycling through the colors using modulo
class_colors = {class_name: colors_list[i % len(colors_list)] for i, class_name in enumerate(unique_classes)}

# Create figure and axis
fig, ax = plt.subplots(figsize=(10, 8))

# Define time slots for the left side and days for the top
times = ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00']
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

# Set the grid
ax.set_xticks([i for i in range(len(days))])
ax.set_xticklabels(days)

ax.set_yticks([i for i in range(len(times))])
ax.set_yticklabels(times)

# Flip the x-axis labels to the top
ax.xaxis.tick_top()

# Adjust the x-ticks to make sure they are aligned in the middle of each day
ax.set_xlim(-0.5, len(days) - 0.5)

# Invert the y-axis to start times from the top
ax.invert_yaxis()

# Add gridlines to represent time slots and days
ax.grid(True, which='both', linestyle='--', color='gray', linewidth=0.5)

ax.grid(axis='x', visible=False)

# Function to convert time (e.g., '08:30') to fractional hours (e.g., 8.5)
def time_to_float(time_str):
    h, m = map(int, time_str.split(':'))
    return h + m / 60

# Add class blocks to the grid
for _, row in df.iterrows():
    # Get class info
    day = row['Day']
    start = time_to_float(row['Start'])
    end = time_to_float(row['End'])
    start_date = row['Start']
    end_date = row['End']
    class_name = row['ClassName']
    class_number = row['ClassNumber']
    room = row['Room']

    # Day index and width
    day_index = days.index(day)
    
    # Convert time to fractional positions and determine block height
    start_time_index = time_to_float(row['Start']) - 8  # Start at 08:00, so subtract 8
    end_time_index = time_to_float(row['End']) - 8
    
    height = end_time_index - start_time_index  # Calculate the height based on duration

    # Create a rectangle for the class with some margin to avoid overlap with grid lines
    ax.add_patch(plt.Rectangle((day_index - 0.4, start_time_index), 0.8, height, facecolor=class_colors[class_name], edgecolor='black', linewidth=1.5))

    # Add the top start and end times of the class
    ax.text(day_index, start_time_index + 0.2, f"{start_date} - {end_date}", va='top', ha='center', fontsize=8, color='black', fontweight='bold')

    # Add text inside the rectangle
    ax.text(day_index, (start_time_index + end_time_index) / 2, f"{class_name} {class_number}\n{room}", 
            va='center', ha='center', fontsize=10, color='black')

# Set labels and title
ax.set_title('Weekly Schedule', fontsize=16)

# Ensure that the layout is tight and the spacing is proper
plt.tight_layout()

# Save the schedule as an image
plt.savefig('schedule.png')

# Show the plot
plt.show()
