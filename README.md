# Scaffolding Visualization

A Python-based 3D visualization tool for scaffolding structures with precise measurements and interactive viewing capabilities.

![Scaffolding Visualization](https://github.com/Dr-Benedek/scaffolding-visualization/blob/main/image.png)

## Project Overview

This program creates an accurate 3D visualization of a scaffolding structure based on specific measurements and geometric constraints. It calculates and verifies all required angles and distances to ensure structural accuracy while providing both static and animated views of the complete model.

## Features

- Precise 3D rendering of scaffolding structure
- Verification of all critical measurements and angles
- Color-coded visualization (visible vs. underground elements)
- Interactive rotation for comprehensive viewing
- Ground plane representation
- Support for animation export

## Requirements

- Python 3.7+
- NumPy
- Matplotlib

## Installation

```bash
# Clone the repository
git clone https://github.com/Dr-Benedek/scaffolding-visualization.git
cd scaffolding-visualization

# Install required dependencies
pip install numpy matplotlib
```

## Usage

```bash
python main.py
```

The program will display:
1. A static view of the scaffolding structure
2. An animated rotating view (It is currently commented out, the comment must be removed from the code for this to work.)

## Input Parameters

The scaffolding structure is defined by parameters contained in `parameters.txt`. Key measurements include:

- Vertical distances (AB = 3.5m, AE = 2.5m, CE = 1.5m, etc.)
- Horizontal distances (EF = 2m, XD = 2.8m, etc.)
- Angular constraints (CF makes 36.87° angle with ground)
- Parallel structure components (AA', BB', CC', etc. at 2m distance)

The full parameter set can be found in the included `parameters.txt` file. These base parameters are used as inputs for the visualization calculations.

## Structure Diagram

The scaffolding consists of:
- Main vertical supports (AB, A'B')
- Horizontal connections (AA', BB', etc.)
- Diagonal supports (CD, C'D')
- Ground level points (E, E', F, F')
- Underground points (B, B', X, X', D, D')

## Constraints Verification

The program verifies the following constraints:
- CDX angle > 36.87°
- CXD angle > 90°
- DCX angle > 53.13°
- All specified distances maintained within tolerance

## Customization

To modify the scaffolding parameters:
1. Edit the measurements at the beginning of `main.py`
2. Run the program to visualize the updated structure

## Acknowledgments

- Built using the Matplotlib 3D toolkit
- Inspired by real-world scaffolding construction requirements
