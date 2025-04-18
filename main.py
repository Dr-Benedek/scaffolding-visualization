import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button

angle_ground_deg = 36.87  
angle_ground_rad = np.radians(angle_ground_deg)


points = {}


points['A'] = np.array([0, 0, 0])  
points['B'] = np.array([0, 0, -3.5])  
points['E'] = np.array([0, 0, -2.5])  
points['C'] = np.array([0, 0, -1.0])  
points['X'] = np.array([0, 0, -3.1])  
points["A'"] = np.array([2, 0, 0])
points["B'"] = np.array([2, 0, -3.5])
points["E'"] = np.array([2, 0, -2.5])
points["C'"] = np.array([2, 0, -1.0])
points["X'"] = np.array([2, 0, -3.1])

cf_horiz = 2.5 * np.cos(angle_ground_rad)

cf_vert = 2.5 * np.sin(angle_ground_rad)

points['F'] = np.array([0, cf_horiz, points['C'][2] - cf_vert])
points["F'"] = np.array([2, cf_horiz, points["C'"][2] - cf_vert])

cf_vec = points['F'] - points['C']
cf_unit = cf_vec / np.linalg.norm(cf_vec)

points['D'] = points['F'] + cf_unit * 1.0
points["D'"] = points["F'"] + cf_unit * 1.0


def distance(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

print(f"AB distance: {distance(points['A'], points['B']):.2f} m (should be 3.5)")
print(f"AE distance: {distance(points['A'], points['E']):.2f} m (should be 2.5)")
print(f"CE distance: {distance(points['C'], points['E']):.2f} m (should be 1.5)")
print(f"CX distance: {distance(points['C'], points['X']):.2f} m (should be 2.1)")
print(f"EX distance: {distance(points['E'], points['X']):.2f} m (should be 0.6)")
print(f"CF distance: {distance(points['C'], points['F']):.2f} m (should be 2.5)")
print(f"FD distance: {distance(points['F'], points['D']):.2f} m (should be 1.0)")
print(f"CD distance: {distance(points['C'], points['D']):.2f} m (should be 3.5)")


def horizontal_distance(p1, p2):
    
    p1_horiz = np.array([points[p1][0], points[p1][1], 0])
    p2_horiz = np.array([points[p2][0], points[p2][1], 0])
    return np.linalg.norm(p1_horiz - p2_horiz)

print(f"EF horizontal distance: {horizontal_distance('E', 'F'):.2f} m (should be 2.0)")
print(f"XD horizontal distance: {horizontal_distance('X', 'D'):.2f} m (should be 2.8)")


xd_horiz = horizontal_distance('X', 'D')
if abs(xd_horiz - 2.8) > 0.01:
    print(f"XD horizontal distance {xd_horiz:.2f}m doesn't match required 2.8m")
    print("Adjusting D and F positions...")
    
    points['D'] = np.array([0, 2.8, points['D'][2]])
    points["D'"] = np.array([2, 2.8, points["D'"][2]])
    
    cd_vert = 2.8 * np.tan(angle_ground_rad)
    points['D'][2] = points['C'][2] - cd_vert
    points["D'"][2] = points["C'"][2] - cd_vert
    
    cd_vec = points['D'] - points['C']
    cd_dist = np.linalg.norm(cd_vec)
    cd_unit = cd_vec / cd_dist
    
    points['F'] = points['C'] + cd_unit * 2.5
    points["F'"] = points["C'"] + cd_unit * 2.5
    
    print(f"CD distance (adjusted): {distance(points['C'], points['D']):.2f} m (should be 3.5)")
    print(f"CF distance (adjusted): {distance(points['C'], points['F']):.2f} m (should be 2.5)")
    print(f"FD distance (adjusted): {distance(points['F'], points['D']):.2f} m (should be 1.0)")
    print(f"XD horizontal distance (adjusted): {horizontal_distance('X', 'D'):.2f} m (should be 2.8)")
    print(f"EF horizontal distance (adjusted): {horizontal_distance('E', 'F'):.2f} m (should be 2.0)")


def angle_between(v1, v2):
    v1_u = v1 / np.linalg.norm(v1)
    v2_u = v2 / np.linalg.norm(v2)
    return np.degrees(np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)))

cd_vec = points['D'] - points['C']
cx_vec = points['X'] - points['C']
dx_vec = points['X'] - points['D']

cdx_angle = angle_between(cd_vec, cx_vec)
cxd_angle = angle_between(cx_vec, dx_vec)
dcx_angle = angle_between(-cd_vec, cx_vec)

print(f"CDX angle: {cdx_angle:.2f}° (should be > 36.87°)")
print(f"CXD angle: {cxd_angle:.2f}° (should be > 90°)")
print(f"DCX angle: {dcx_angle:.2f}° (should be > 53.13°)")


segment_distances = {
    ('A', 'B'): 3.5,
    ('A', 'E'): 2.5,
    ('C', 'E'): 1.5,
    ('C', 'X'): 2.1,
    ('E', 'X'): 0.6,
    ('C', 'F'): 2.5,
    ('F', 'D'): 1.0,
    ('C', 'D'): 3.5,
    ('E', 'F'): 2.0,
    ('X', 'D'): 2.8,
    ('A', "A'"): 2.0,
    ('B', "B'"): 2.0,
    ('C', "C'"): 2.0,
    ('D', "D'"): 2.0,
    ('E', "E'"): 2.0,
    ('F', "F'"): 2.0,
    ('X', "X'"): 2.0,
    ("A'", "B'"): 3.5,
    ("A'", "E'"): 2.5,
    ("C'", "E'"): 1.5,
    ("C'", "X'"): 2.1,
    ("E'", "X'"): 0.6,
    ("C'", "F'"): 2.5,
    ("F'", "D'"): 1.0,
    ("C'", "D'"): 3.5,
    ("E'", "F'"): 2.0,
    ("X'", "D'"): 2.8
}

class ScaffoldingVisualization:
    def __init__(self):
        self.fig = plt.figure(figsize=(12, 11))
        
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        self.show_distances = True
        
        self.segments = [
            ('A', "A'"),  
            ('A', 'B'),   
            ("A'", "B'"), 
            ('C', 'D'),   
            ("C'", "D'"), 
            ('A', 'C'),
            ("A'", "C'"),
            ('B', 'X'),
            ("B'", "X'"),
            ('C', 'X'),
            ("C'", "X'"),
            ('C', 'F'),
            ("C'", "F'"),
            ('F', 'D'),
            ("F'", "D'"),
            ('E', 'F'),
            ("E'", "F'"),
            ('E', 'X'),
            ("E'", "X'"),
            ('X', 'D'),
            ("X'", "D'"),
            ('B', "B'"),
            #('C', "C'"),
            ('D', "D'"),
            #('E', "E'"),
            #('F', "F'"),
            ('X', "X'")
        ]
        
        self.visible_lines = [('A', "A'"), ('A', 'B'), ("A'", "B'"), ('C', 'D'), ("C'", "D'")]
        self.underground_points = ['B', "B'", 'X', "X'", 'D', "D'"]
        
        plt.subplots_adjust(bottom=0.15)
        
        self.button_ax = plt.axes([0.7, 0.05, 0.25, 0.075])  # [left, bottom, width, height]
        self.button = Button(self.button_ax, 'Toggle Distances')
        self.button.on_clicked(self.toggle_distances)
        
        self.update_plot()
    
    def toggle_distances(self, event):
        self.show_distances = not self.show_distances
    
        self.button.label.set_text('Hide Distances' if self.show_distances else 'Show Distances')
        
        self.update_plot()
    
    def update_plot(self):
        self.ax.clear()
        
        for s in self.segments:
            p1, p2 = s
            x = [points[p1][0], points[p2][0]]
            y = [points[p1][1], points[p2][1]]
            z = [points[p1][2], points[p2][2]]
            
            if s in self.visible_lines:
                self.ax.plot(x, y, z, 'r-', linewidth=3)  
            elif p1 in self.underground_points and p2 in self.underground_points:
                self.ax.plot(x, y, z, 'k--', linewidth=1)  
            else:
                self.ax.plot(x, y, z, 'b-', linewidth=1.5)  
            
            if self.show_distances and s in segment_distances:
                mid_x = (x[0] + x[1]) / 2
                mid_y = (y[0] + y[1]) / 2
                mid_z = (z[0] + z[1]) / 2
                
                offset = 0.15
                label_x = mid_x
                label_y = mid_y
                label_z = mid_z + offset
                
                distance_text = f"{segment_distances[s]:.1f}m"
                
                self.ax.text(label_x, label_y, label_z, distance_text, 
                        fontsize=9, ha='center', va='center',
                        bbox=dict(facecolor='white', alpha=0.7, pad=2, edgecolor='none'))
        
        x_ground = np.linspace(-1, 3, 5)
        y_ground = np.linspace(-1, 4, 7)
        X_ground, Y_ground = np.meshgrid(x_ground, y_ground)
        Z_ground = np.ones_like(X_ground) * -2.5
        self.ax.plot_surface(X_ground, Y_ground, Z_ground, alpha=0.2, color='brown')
        
        for p, coords in points.items():
            if p in self.underground_points:
                self.ax.scatter(coords[0], coords[1], coords[2], color='gray', s=80, alpha=0.7, zorder=10)
            else:
                self.ax.scatter(coords[0], coords[1], coords[2], color='black', s=80, zorder=10)
            
            offset = 0.1
            label_x = coords[0]
            label_y = coords[1]
            label_z = coords[2] + offset
            
            self.ax.text(label_x, label_y, label_z, p, fontsize=7.5, fontweight='bold', ha='center', va='center',
                    bbox=dict(facecolor='white', alpha=0.9, pad=2, edgecolor='black'), zorder=11)
        
        self.ax.grid(True)
        self.ax.set_xlabel('X (m)')
        self.ax.set_ylabel('Y (m)')
        self.ax.set_zlabel('Z (m)')
        self.ax.set_title('3D Scaffolding Structure')
        self.ax.view_init(elev=25, azim=30)
        self.ax.set_xlim(-1, 3)
        self.ax.set_ylim(-1, 4)
        self.ax.set_zlim(-4, 1)
        
        self.fig.canvas.draw_idle()
    
    def show(self):
        plt.tight_layout()
        plt.show()

class AnimatedScaffoldingVisualization:
    def __init__(self):
        self.fig = plt.figure(figsize=(12, 11))
        
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        self.show_distances = True
        
        self.segments = [
            ('A', "A'"),  
            ('A', 'B'),   
            ("A'", "B'"), 
            ('C', 'D'),   
            ("C'", "D'"), 
            ('A', 'C'),
            ("A'", "C'"),
            ('B', 'X'),
            ("B'", "X'"),
            ('C', 'X'),
            ("C'", "X'"),
            ('C', 'F'),
            ("C'", "F'"),
            ('F', 'D'),
            ("F'", "D'"),
            ('E', 'F'),
            ("E'", "F'"),
            ('E', 'X'),
            ("E'", "X'"),
            ('X', 'D'),
            ("X'", "D'"),
            ('B', "B'"),
            ('D', "D'"),
            ('X', "X'")
        ]
        
        self.visible_lines = [('A', "A'"), ('A', 'B'), ("A'", "B'"), ('C', 'D'), ("C'", "D'")]
        self.underground_points = ['B', "B'", 'X', "X'", 'D', "D'"]
        
        plt.subplots_adjust(bottom=0.15)
        
        self.button_ax = plt.axes([0.7, 0.05, 0.25, 0.075])
        self.button = Button(self.button_ax, 'Toggle Distances')
        self.button.on_clicked(self.toggle_distances)
        
        self.angles = np.linspace(0, 360, 120)
        self.anim = FuncAnimation(
            self.fig, 
            self.update_plot, 
            frames=self.angles, 
            interval=50, 
            blit=False
        )
    
    def toggle_distances(self, event):
        self.show_distances = not self.show_distances
        
        self.button.label.set_text('Hide Distances' if self.show_distances else 'Show Distances')
        
    
    def update_plot(self, angle):
        self.ax.clear()
        
        for s in self.segments:
            p1, p2 = s
            x = [points[p1][0], points[p2][0]]
            y = [points[p1][1], points[p2][1]]
            z = [points[p1][2], points[p2][2]]
            
            if s in self.visible_lines:
                self.ax.plot(x, y, z, 'r-', linewidth=3)  
            elif p1 in self.underground_points and p2 in self.underground_points:
                self.ax.plot(x, y, z, 'k--', linewidth=1)  
            else:
                self.ax.plot(x, y, z, 'b-', linewidth=1.5)  
            
            if self.show_distances and s in segment_distances:
                mid_x = (x[0] + x[1]) / 2
                mid_y = (y[0] + y[1]) / 2
                mid_z = (z[0] + z[1]) / 2
                
                offset = 0.15
                label_x = mid_x
                label_y = mid_y
                label_z = mid_z + offset
                
                distance_text = f"{segment_distances[s]:.1f}m"
                
                self.ax.text(label_x, label_y, label_z, distance_text, 
                        fontsize=9, ha='center', va='center',
                        bbox=dict(facecolor='white', alpha=0.7, pad=2, edgecolor='none'))
        
        x_ground = np.linspace(-1, 3, 5)
        y_ground = np.linspace(-1, 4, 7)
        X_ground, Y_ground = np.meshgrid(x_ground, y_ground)
        Z_ground = np.ones_like(X_ground) * -2.5
        self.ax.plot_surface(X_ground, Y_ground, Z_ground, alpha=0.2, color='brown')
        
        for p, coords in points.items():
            if p in self.underground_points:
                self.ax.scatter(coords[0], coords[1], coords[2], color='gray', s=80, alpha=0.7, zorder=10)
            else:
                self.ax.scatter(coords[0], coords[1], coords[2], color='black', s=80, zorder=10)
            
            offset = 0.1
            label_x = coords[0]
            label_y = coords[1]
            label_z = coords[2] + offset
            
            self.ax.text(label_x, label_y, label_z, p, fontsize=7.5, fontweight='bold', ha='center', va='center',
                    bbox=dict(facecolor='white', alpha=0.9, pad=2, edgecolor='black'), zorder=11)
        
        self.ax.grid(True)
        self.ax.set_xlabel('X (m)')
        self.ax.set_ylabel('Y (m)')
        self.ax.set_zlabel('Z (m)')
        self.ax.set_title('3D Scaffolding Structure')
        self.ax.view_init(elev=25, azim=angle)
        self.ax.set_xlim(-1, 3)
        self.ax.set_ylim(-1, 4)
        self.ax.set_zlim(-4, 1)
        
        return self.ax
    
    def show(self):
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    viz = ScaffoldingVisualization()
    viz.show()
    
    # Uncomment to use animated version with button
    #animated_viz = AnimatedScaffoldingVisualization()
    #animated_viz.show()