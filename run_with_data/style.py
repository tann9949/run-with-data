import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm
from pathlib import Path
import os

# Get the current file's directory
CURRENT_DIR = Path(__file__).parent

# Add font files from the font directory
FONT_DIR = CURRENT_DIR / 'font'

# Register all font files in the font directory
font_files = FONT_DIR.glob('*.ttf')
for font_path in font_files:
    fm.fontManager.addfont(str(font_path))

# Define your brand colors
BACKGROUND_COLOR = '#000000'
AXIS_COLOR = '#FFFFFF'
GRID_COLOR = '#333333'  # Light gray that works well on black
PRIMARY_COLOR = '#4DFF00'
SECONDARY_COLOR = '#FFED00'

# Create a custom style dictionary
brand_style = {
    # Font configuration
    'font.family': 'Open Sauce One',
    'font.weight': 'normal',
    
    # Title fonts - making them bold
    'axes.titleweight': 'bold',
    'figure.titleweight': 'bold',
    'legend.title_fontsize': 'large',
    
    # Figure and axes background
    'figure.facecolor': BACKGROUND_COLOR,
    'axes.facecolor': BACKGROUND_COLOR,
    
    # Axis colors and properties
    'axes.edgecolor': AXIS_COLOR,
    'axes.labelcolor': AXIS_COLOR,
    'axes.grid': True,
    'axes.labelweight': 'bold',  # Making axis labels bold
    
    # Grid properties
    'grid.color': GRID_COLOR,
    'grid.alpha': 0.3,
    'grid.linestyle': '--',
    
    # Tick properties
    'xtick.color': AXIS_COLOR,
    'ytick.color': AXIS_COLOR,
    
    # Default colors for plotting
    'axes.prop_cycle': mpl.cycler('color', [PRIMARY_COLOR, SECONDARY_COLOR]),
    
    # Text properties
    'text.color': AXIS_COLOR,
    
    # Legend properties
    'legend.facecolor': BACKGROUND_COLOR,
    'legend.edgecolor': AXIS_COLOR,
    'legend.labelcolor': AXIS_COLOR,
    
    # Font sizes
    'font.size': 12,
    'axes.labelsize': 14,
    'axes.titlesize': 16,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'legend.fontsize': 12,
    'figure.titlesize': 20
}

def apply_brand_style():
    """Apply the custom brand style to matplotlib."""
    plt.style.use('dark_background')  # Start with dark theme as base
    plt.rcParams.update(brand_style)  # Apply custom brand style
    