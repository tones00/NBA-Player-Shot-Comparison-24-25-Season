#!/usr/bin/env python3
"""
Demo version of the Basketball Shot Tracker
This version uses sample data to demonstrate the shot chart functionality
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from typing import Dict

class ShotChartVisualizer:
    def __init__(self):
        self.court_zones = {
            'Restricted Area': {'x': 0, 'y': 0, 'radius': 4},
            'In The Paint (Non-RA)': {'x': 0, 'y': 0, 'radius': 8},
            'Mid-Range': {'x': 0, 'y': 0, 'radius': 16},
            'Left Corner 3': {'x': -22, 'y': -8, 'radius': 3},
            'Right Corner 3': {'x': 22, 'y': -8, 'radius': 3},
            'Above the Break 3': {'x': 0, 'y': -23, 'radius': 3}
        }
    
    def create_shot_chart(self, player_data: Dict, title: str = "Player Shot Chart") -> plt.Figure:
        """Create a shot chart visualization"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Draw basketball court outline
        self._draw_court(ax)
        
        # Plot shooting zones
        for zone, data in player_data.items():
            if zone in self.court_zones and 'FG%' in data:
                zone_info = self.court_zones[zone]
                fg_pct = data['FG%']
                fga = data.get('FGA', 0)
                
                # Color based on shooting percentage
                if fg_pct >= 50:
                    color = 'green'
                    alpha = 0.8
                elif fg_pct >= 40:
                    color = 'yellow'
                    alpha = 0.6
                else:
                    color = 'red'
                    alpha = 0.4
                
                circle = plt.Circle((zone_info['x'], zone_info['y']), 
                                  zone_info['radius'], 
                                  color=color, alpha=alpha, 
                                  edgecolor='black', linewidth=2)
                ax.add_patch(circle)
                
                # Add text with shooting percentage
                ax.text(zone_info['x'], zone_info['y'], 
                       f'{fg_pct:.1f}%\n({fga} FGA)', 
                       ha='center', va='center', 
                       fontsize=8, fontweight='bold')
        
        ax.set_xlim(-30, 30)
        ax.set_ylim(-30, 10)
        ax.set_aspect('equal')
        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.axis('off')
        
        # Add legend
        legend_elements = [
            plt.Circle((0, 0), 1, color='green', alpha=0.8, label='50%+ FG%'),
            plt.Circle((0, 0), 1, color='yellow', alpha=0.6, label='40-49% FG%'),
            plt.Circle((0, 0), 1, color='red', alpha=0.4, label='<40% FG%')
        ]
        ax.legend(handles=legend_elements, loc='upper right')
        
        plt.tight_layout()
        return fig
    
    def compare_players(self, player1_data: Dict, player2_data: Dict, 
                       player1_name: str, player2_name: str) -> plt.Figure:
        """Create a side-by-side comparison of two players"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
        
        # Player 1 chart
        self._draw_court(ax1)
        self._plot_player_zones(ax1, player1_data)
        ax1.set_title(f"{player1_name} Shot Chart", fontsize=14, fontweight='bold')
        
        # Player 2 chart
        self._draw_court(ax2)
        self._plot_player_zones(ax2, player2_data)
        ax2.set_title(f"{player2_name} Shot Chart", fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        return fig
    
    def _draw_court(self, ax):
        """Draw a simple basketball court outline"""
        # Court outline
        court = plt.Rectangle((-25, -25), 50, 50, fill=False, color='black', linewidth=2)
        ax.add_patch(court)
        
        # Three-point line
        three_point_left = patches.Arc((-25, 0), 47, 47, angle=0, theta1=90, theta2=270, 
                                 color='black', linewidth=2)
        three_point_right = patches.Arc((25, 0), 47, 47, angle=0, theta1=270, theta2=90, 
                                  color='black', linewidth=2)
        ax.add_patch(three_point_left)
        ax.add_patch(three_point_right)
        
        # Paint
        paint = plt.Rectangle((-8, -25), 16, 19, fill=False, color='black', linewidth=2)
        ax.add_patch(paint)
        
        # Restricted area
        restricted = plt.Circle((0, -6), 4, fill=False, color='black', linewidth=2)
        ax.add_patch(restricted)
    
    def _plot_player_zones(self, ax, player_data):
        """Plot shooting zones for a player"""
        for zone, data in player_data.items():
            if zone in self.court_zones and 'FG%' in data:
                zone_info = self.court_zones[zone]
                fg_pct = data['FG%']
                fga = data.get('FGA', 0)
                
                # Color based on shooting percentage
                if fg_pct >= 50:
                    color = 'green'
                    alpha = 0.8
                elif fg_pct >= 40:
                    color = 'yellow'
                    alpha = 0.6
                else:
                    color = 'red'
                    alpha = 0.4
                
                circle = plt.Circle((zone_info['x'], zone_info['y']), 
                                  zone_info['radius'], 
                                  color=color, alpha=alpha, 
                                  edgecolor='black', linewidth=2)
                ax.add_patch(circle)
                
                # Add text with shooting percentage
                ax.text(zone_info['x'], zone_info['y'], 
                       f'{fg_pct:.1f}%\n({fga} FGA)', 
                       ha='center', va='center', 
                       fontsize=8, fontweight='bold')

def get_sample_data(player_name: str) -> Dict:
    """Get sample shooting data for demonstration"""
    if "curry" in player_name.lower():
        return {
            'Restricted Area': {'FGM': 45, 'FGA': 60, 'FG%': 75.0},
            'In The Paint (Non-RA)': {'FGM': 25, 'FGA': 50, 'FG%': 50.0},
            'Mid-Range': {'FGM': 30, 'FGA': 80, 'FG%': 37.5},
            'Left Corner 3': {'FGM': 15, 'FGA': 30, 'FG%': 50.0},
            'Right Corner 3': {'FGM': 18, 'FGA': 35, 'FG%': 51.4},
            'Above the Break 3': {'FGM': 120, 'FGA': 300, 'FG%': 40.0}
        }
    elif "lebron" in player_name.lower() or "james" in player_name.lower():
        return {
            'Restricted Area': {'FGM': 180, 'FGA': 250, 'FG%': 72.0},
            'In The Paint (Non-RA)': {'FGM': 80, 'FGA': 150, 'FG%': 53.3},
            'Mid-Range': {'FGM': 60, 'FGA': 120, 'FG%': 50.0},
            'Left Corner 3': {'FGM': 25, 'FGA': 60, 'FG%': 41.7},
            'Right Corner 3': {'FGM': 30, 'FGA': 70, 'FG%': 42.9},
            'Above the Break 3': {'FGM': 45, 'FGA': 150, 'FG%': 30.0}
        }
    elif "durant" in player_name.lower():
        return {
            'Restricted Area': {'FGM': 120, 'FGA': 180, 'FG%': 66.7},
            'In The Paint (Non-RA)': {'FGM': 40, 'FGA': 80, 'FG%': 50.0},
            'Mid-Range': {'FGM': 80, 'FGA': 150, 'FG%': 53.3},
            'Left Corner 3': {'FGM': 20, 'FGA': 45, 'FG%': 44.4},
            'Right Corner 3': {'FGM': 25, 'FGA': 50, 'FG%': 50.0},
            'Above the Break 3': {'FGM': 60, 'FGA': 180, 'FG%': 33.3}
        }
    else:
        # Generic sample data
        return {
            'Restricted Area': {'FGM': 100, 'FGA': 150, 'FG%': 66.7},
            'In The Paint (Non-RA)': {'FGM': 50, 'FGA': 100, 'FG%': 50.0},
            'Mid-Range': {'FGM': 40, 'FGA': 100, 'FG%': 40.0},
            'Left Corner 3': {'FGM': 20, 'FGA': 50, 'FG%': 40.0},
            'Right Corner 3': {'FGM': 25, 'FGA': 60, 'FG%': 41.7},
            'Above the Break 3': {'FGM': 60, 'FGA': 180, 'FG%': 33.3}
        }

def main():
    """Main demo function"""
    visualizer = ShotChartVisualizer()
    
    print("🏀 Basketball Shot Chart Demo")
    print("=" * 50)
    print("This demo uses sample data to show shot chart functionality")
    print()
    
    # Get player names
    player1_name = input("Enter first player name: ").strip()
    player2_name = input("Enter second player name: ").strip()
    
    print(f"\nGenerating sample data for {player1_name} and {player2_name}...")
    
    # Get sample data
    player1_data = get_sample_data(player1_name)
    player2_data = get_sample_data(player2_name)
    
    # Create comparison chart
    fig = visualizer.compare_players(player1_data, player2_data, 
                                   player1_name, player2_name)
    
    # Save the chart
    filename = f"{player1_name.replace(' ', '_')}_vs_{player2_name.replace(' ', '_')}_shot_chart.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Chart saved as: {filename}")
    
    # Show the chart
    plt.show()
    
    # Print summary statistics
    print(f"\n{player1_name} Shooting Summary:")
    for zone, data in player1_data.items():
        print(f"  {zone}: {data['FG%']:.1f}% ({data.get('FGM', 0)}/{data.get('FGA', 0)})")
    
    print(f"\n{player2_name} Shooting Summary:")
    for zone, data in player2_data.items():
        print(f"  {zone}: {data['FG%']:.1f}% ({data.get('FGM', 0)}/{data.get('FGA', 0)})")
    
    print("\n🎉 Demo completed! The chart shows:")
    print("  🟢 Green: 50%+ field goal percentage")
    print("  🟡 Yellow: 40-49% field goal percentage")
    print("  🔴 Red: <40% field goal percentage")

if __name__ == "__main__":
    main()
