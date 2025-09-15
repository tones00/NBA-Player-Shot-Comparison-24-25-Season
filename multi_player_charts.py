#!/usr/bin/env python3
"""
Basketball Shot Tracker - Multi-Player Scatter Plot Version
Creates scatter plots comparing multiple players with FGA on x-axis and FG% on y-axis
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Tuple
import pandas as pd

class MultiPlayerScatterCharts:
    def __init__(self):
        # Define shot categories and their data structure
        self.shot_categories = {
            '3PT': {
                'zones': ['Left Corner 3', 'Right Corner 3', 'Above the Break 3'],
                'title': '3-Point Shooting Comparison',
                'x_label': '3-Point Attempts',
                'y_label': '3-Point FG%'
            },
            '2PT': {
                'zones': ['Restricted Area', 'In The Paint (Non-RA)', 'Mid-Range'],
                'title': '2-Point Shooting Comparison',
                'x_label': '2-Point Attempts',
                'y_label': '2-Point FG%'
            },
            'FT': {
                'zones': ['Free Throws'],
                'title': 'Free Throw Shooting Comparison',
                'x_label': 'Free Throw Attempts',
                'y_label': 'Free Throw %'
            }
        }
        
        # Color palette for multiple players
        self.colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'gray']
        self.markers = ['o', 's', '^', 'D', 'v', '<', '>', 'p']
    
    def create_multi_player_charts(self, players_data: Dict[str, Dict]) -> plt.Figure:
        """Create scatter plot charts comparing multiple players"""
        
        num_players = len(players_data)
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle(f'Multi-Player Shooting Comparison ({num_players} players)', 
                    fontsize=16, fontweight='bold')
        
        # Create charts for each shot category
        chart_positions = [(0, 0), (0, 1), (1, 0)]
        chart_names = ['3PT', '2PT', 'FT']
        
        for i, category in enumerate(chart_names):
            row, col = chart_positions[i]
            ax = axes[row, col]
            
            self._create_multi_category_chart(ax, players_data, category)
        
        # Create efficiency summary chart in bottom right
        self._create_efficiency_summary(axes[1, 1], players_data)
        
        plt.tight_layout()
        return fig
    
    def _create_multi_category_chart(self, ax, players_data: Dict[str, Dict], category: str):
        """Create a scatter plot for a specific shot category with multiple players"""
        
        category_info = self.shot_categories[category]
        all_x_values = []
        all_y_values = []
        
        # Plot data for each player
        for i, (player_name, player_data) in enumerate(players_data.items()):
            color = self.colors[i % len(self.colors)]
            marker = self.markers[i % len(self.markers)]
            
            # Extract data for this category
            points = self._extract_category_data(player_data, category)
            
            if points:
                x_vals, y_vals, labels = zip(*points)
                all_x_values.extend(x_vals)
                all_y_values.extend(y_vals)
                ax.scatter(x_vals, y_vals, c=color, s=100, alpha=0.7, 
                          label=player_name, edgecolors='black', linewidth=1,
                          marker=marker)
                
                # Add zone labels for first few points to avoid clutter
                for j, (x, y, label) in enumerate(points[:2]):  # Only label first 2 zones
                    ax.annotate(f'{label}', (x, y), 
                               xytext=(5, 5), textcoords='offset points',
                               fontsize=7, alpha=0.8, color=color)
        
        # Calculate dynamic ranges starting from 0
        if all_x_values and all_y_values:
            x_max = max(all_x_values)
            y_max = max(all_y_values)
            y_min = min(all_y_values)
            
            # Add 10% padding to ranges
            x_range = (0, x_max * 1.1)
            y_range = (max(0, y_min * 0.9), y_max * 1.1)
        else:
            # Default ranges if no data
            x_range = (0, 100)
            y_range = (0, 100)
        
        # Set chart properties
        ax.set_xlabel(category_info['x_label'], fontsize=12)
        ax.set_ylabel(category_info['y_label'], fontsize=12)
        ax.set_title(category_info['title'], fontsize=14, fontweight='bold')
        ax.set_xlim(x_range)
        ax.set_ylim(y_range)
        ax.grid(True, alpha=0.3)
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # Add league average lines
        self._add_league_averages(ax, category)
    
    def _extract_category_data(self, player_data: Dict, category: str) -> List[Tuple]:
        """Extract FGA and FG% data for a specific category"""
        points = []
        category_info = self.shot_categories[category]
        
        for zone in category_info['zones']:
            if zone in player_data and 'FGA' in player_data[zone] and 'FG%' in player_data[zone]:
                fga = player_data[zone]['FGA']
                fg_pct = player_data[zone]['FG%']
                # Use abbreviated zone name for cleaner labels
                zone_abbrev = self._abbreviate_zone_name(zone)
                points.append((fga, fg_pct, zone_abbrev))
        
        return points
    
    def _abbreviate_zone_name(self, zone: str) -> str:
        """Create abbreviated zone names for cleaner labels"""
        abbreviations = {
            'Restricted Area': 'RA',
            'In The Paint (Non-RA)': 'Paint',
            'Mid-Range': 'Mid',
            'Left Corner 3': 'LC3',
            'Right Corner 3': 'RC3',
            'Above the Break 3': 'ATB3',
            'Free Throws': 'FT'
        }
        return abbreviations.get(zone, zone[:4])
    
    def _add_league_averages(self, ax, category: str):
        """Add league average reference lines"""
        league_averages = {
            '3PT': 35.0,
            '2PT': 52.0,
            'FT': 78.0
        }
        
        if category in league_averages:
            avg = league_averages[category]
            ax.axhline(y=avg, color='gray', linestyle='--', alpha=0.5, 
                      label=f'League Avg ({avg}%)')
    
    def _create_efficiency_summary(self, ax, players_data: Dict[str, Dict]):
        """Create an overall shooting efficiency summary chart"""
        
        # Calculate stats for each player
        player_stats = {}
        for player_name, player_data in players_data.items():
            player_stats[player_name] = self._calculate_total_stats(player_data)
        
        # Create comparison metrics
        metrics = ['Total FG%', '3PT FG%', '2PT FG%', 'FT%']
        x = np.arange(len(metrics))
        width = 0.8 / len(players_data)
        
        for i, (player_name, stats) in enumerate(player_stats.items()):
            color = self.colors[i % len(self.colors)]
            values = [
                stats['total_fg_pct'],
                stats['3pt_fg_pct'],
                stats['2pt_fg_pct'],
                stats.get('ft_fg_pct', 0)  # Will be 0 if no FT data
            ]
            
            ax.bar(x + i * width - width * (len(players_data) - 1) / 2, 
                  values, width, label=player_name, color=color, alpha=0.7)
        
        ax.set_xlabel('Shooting Categories')
        ax.set_ylabel('Field Goal Percentage (%)')
        ax.set_title('Overall Shooting Efficiency Comparison')
        ax.set_xticks(x)
        ax.set_xticklabels(metrics)
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 100)
    
    def _calculate_total_stats(self, player_data: Dict) -> Dict:
        """Calculate total shooting statistics for a player"""
        stats = {
            'total_fga': 0,
            'total_fgm': 0,
            'total_fg_pct': 0,
            '3pt_fga': 0,
            '3pt_fgm': 0,
            '3pt_fg_pct': 0,
            '2pt_fga': 0,
            '2pt_fgm': 0,
            '2pt_fg_pct': 0,
            'ft_fga': 0,
            'ft_fgm': 0,
            'ft_fg_pct': 0
        }
        
        # 3PT zones
        for zone in ['Left Corner 3', 'Right Corner 3', 'Above the Break 3']:
            if zone in player_data:
                stats['3pt_fga'] += player_data[zone].get('FGA', 0)
                stats['3pt_fgm'] += player_data[zone].get('FGM', 0)
        
        # 2PT zones
        for zone in ['Restricted Area', 'In The Paint (Non-RA)', 'Mid-Range']:
            if zone in player_data:
                stats['2pt_fga'] += player_data[zone].get('FGA', 0)
                stats['2pt_fgm'] += player_data[zone].get('FGM', 0)
        
        # Free throws
        if 'Free Throws' in player_data:
            stats['ft_fga'] = player_data['Free Throws'].get('FGA', 0)
            stats['ft_fgm'] = player_data['Free Throws'].get('FGM', 0)
        
        # Calculate percentages
        if stats['3pt_fga'] > 0:
            stats['3pt_fg_pct'] = (stats['3pt_fgm'] / stats['3pt_fga']) * 100
        
        if stats['2pt_fga'] > 0:
            stats['2pt_fg_pct'] = (stats['2pt_fgm'] / stats['2pt_fga']) * 100
        
        if stats['ft_fga'] > 0:
            stats['ft_fg_pct'] = (stats['ft_fgm'] / stats['ft_fga']) * 100
        
        stats['total_fga'] = stats['3pt_fga'] + stats['2pt_fga']
        stats['total_fgm'] = stats['3pt_fgm'] + stats['2pt_fgm']
        
        if stats['total_fga'] > 0:
            stats['total_fg_pct'] = (stats['total_fgm'] / stats['total_fga']) * 100
        
        return stats

def get_enhanced_sample_data(player_name: str) -> Dict:
    """Get enhanced sample shooting data with more realistic distributions"""
    if "curry" in player_name.lower():
        return {
            'Restricted Area': {'FGM': 45, 'FGA': 60, 'FG%': 75.0},
            'In The Paint (Non-RA)': {'FGM': 25, 'FGA': 50, 'FG%': 50.0},
            'Mid-Range': {'FGM': 30, 'FGA': 80, 'FG%': 37.5},
            'Left Corner 3': {'FGM': 15, 'FGA': 30, 'FG%': 50.0},
            'Right Corner 3': {'FGM': 18, 'FGA': 35, 'FG%': 51.4},
            'Above the Break 3': {'FGM': 120, 'FGA': 300, 'FG%': 40.0},
            'Free Throws': {'FGM': 180, 'FGA': 200, 'FG%': 90.0}
        }
    elif "lebron" in player_name.lower() or "james" in player_name.lower():
        return {
            'Restricted Area': {'FGM': 180, 'FGA': 250, 'FG%': 72.0},
            'In The Paint (Non-RA)': {'FGM': 80, 'FGA': 150, 'FG%': 53.3},
            'Mid-Range': {'FGM': 60, 'FGA': 120, 'FG%': 50.0},
            'Left Corner 3': {'FGM': 25, 'FGA': 60, 'FG%': 41.7},
            'Right Corner 3': {'FGM': 30, 'FGA': 70, 'FG%': 42.9},
            'Above the Break 3': {'FGM': 45, 'FGA': 150, 'FG%': 30.0},
            'Free Throws': {'FGM': 200, 'FGA': 280, 'FG%': 71.4}
        }
    elif "durant" in player_name.lower():
        return {
            'Restricted Area': {'FGM': 120, 'FGA': 180, 'FG%': 66.7},
            'In The Paint (Non-RA)': {'FGM': 40, 'FGA': 80, 'FG%': 50.0},
            'Mid-Range': {'FGM': 80, 'FGA': 150, 'FG%': 53.3},
            'Left Corner 3': {'FGM': 20, 'FGA': 45, 'FG%': 44.4},
            'Right Corner 3': {'FGM': 25, 'FGA': 50, 'FG%': 50.0},
            'Above the Break 3': {'FGM': 60, 'FGA': 180, 'FG%': 33.3},
            'Free Throws': {'FGM': 160, 'FGA': 180, 'FG%': 88.9}
        }
    elif "giannis" in player_name.lower() or "antetokounmpo" in player_name.lower():
        return {
            'Restricted Area': {'FGM': 200, 'FGA': 280, 'FG%': 71.4},
            'In The Paint (Non-RA)': {'FGM': 100, 'FGA': 180, 'FG%': 55.6},
            'Mid-Range': {'FGM': 20, 'FGA': 60, 'FG%': 33.3},
            'Left Corner 3': {'FGM': 10, 'FGA': 30, 'FG%': 33.3},
            'Right Corner 3': {'FGM': 12, 'FGA': 35, 'FG%': 34.3},
            'Above the Break 3': {'FGM': 25, 'FGA': 100, 'FG%': 25.0},
            'Free Throws': {'FGM': 300, 'FGA': 450, 'FG%': 66.7}
        }
    elif "embiid" in player_name.lower():
        return {
            'Restricted Area': {'FGM': 150, 'FGA': 200, 'FG%': 75.0},
            'In The Paint (Non-RA)': {'FGM': 60, 'FGA': 120, 'FG%': 50.0},
            'Mid-Range': {'FGM': 40, 'FGA': 100, 'FG%': 40.0},
            'Left Corner 3': {'FGM': 15, 'FGA': 40, 'FG%': 37.5},
            'Right Corner 3': {'FGM': 18, 'FGA': 45, 'FG%': 40.0},
            'Above the Break 3': {'FGM': 30, 'FGA': 120, 'FG%': 25.0},
            'Free Throws': {'FGM': 250, 'FGA': 300, 'FG%': 83.3}
        }
    else:
        # Generic sample data
        return {
            'Restricted Area': {'FGM': 100, 'FGA': 150, 'FG%': 66.7},
            'In The Paint (Non-RA)': {'FGM': 50, 'FGA': 100, 'FG%': 50.0},
            'Mid-Range': {'FGM': 40, 'FGA': 100, 'FG%': 40.0},
            'Left Corner 3': {'FGM': 20, 'FGA': 50, 'FG%': 40.0},
            'Right Corner 3': {'FGM': 25, 'FGA': 60, 'FG%': 41.7},
            'Above the Break 3': {'FGM': 60, 'FGA': 180, 'FG%': 33.3},
            'Free Throws': {'FGM': 120, 'FGA': 150, 'FG%': 80.0}
        }

def main():
    """Main function to demonstrate the multi-player scatter chart functionality"""
    charts = MultiPlayerScatterCharts()
    
    print("🏀 Basketball Shot Tracker - Multi-Player Scatter Plot Version")
    print("=" * 70)
    print("This version creates scatter plots comparing multiple players")
    print("with FGA on x-axis and FG% on y-axis")
    print()
    
    # Get number of players
    num_players = int(input("How many players do you want to compare? (2-8): "))
    num_players = max(2, min(8, num_players))  # Limit between 2-8
    
    players_data = {}
    
    # Get player names and data
    for i in range(num_players):
        player_name = input(f"Enter player {i+1} name: ").strip()
        players_data[player_name] = get_enhanced_sample_data(player_name)
    
    print(f"\nGenerating enhanced sample data for {num_players} players...")
    
    # Create comparison charts
    fig = charts.create_multi_player_charts(players_data)
    
    # Save the chart
    player_names = "_vs_".join([name.replace(' ', '_') for name in players_data.keys()])
    filename = f"multi_player_comparison_{player_names}_scatter_charts.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Charts saved as: {filename}")
    
    # Show the chart
    plt.show()
    
    # Print detailed statistics
    print(f"\n📊 Detailed Shooting Statistics:")
    for player_name, player_data in players_data.items():
        print(f"\n{player_name}:")
        for zone, data in player_data.items():
            print(f"  {zone}: {data['FG%']:.1f}% ({data.get('FGM', 0)}/{data.get('FGA', 0)})")
    
    print("\n🎯 Chart Interpretation:")
    print("  • X-axis: Field Goal Attempts (FGA)")
    print("  • Y-axis: Field Goal Percentage (FG%)")
    print("  • Different colors/markers: Different players")
    print("  • Dashed line: League average")
    print("  • Higher and more to the right = better efficiency with more volume")

if __name__ == "__main__":
    main()
