#!/usr/bin/env python3
"""
Basketball Shot Tracker - Scatter Plot Version
Creates scatter plots with FGA on x-axis and FG% on y-axis
Separate charts for 3PT, 2PT, and FT shooting
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Tuple
import pandas as pd

class BasketballScatterCharts:
    def __init__(self):
        # Define shot categories and their data structure
        self.shot_categories = {
            '3PT': {
                'zones': ['Left Corner 3', 'Right Corner 3', 'Above the Break 3'],
                'title': '3-Point Shooting',
                'x_label': '3-Point Attempts',
                'y_label': '3-Point FG%'
            },
            '2PT': {
                'zones': ['Restricted Area', 'In The Paint (Non-RA)', 'Mid-Range'],
                'title': '2-Point Shooting',
                'x_label': '2-Point Attempts',
                'y_label': '2-Point FG%'
            },
            'FT': {
                'zones': ['Free Throws'],
                'title': 'Free Throw Shooting',
                'x_label': 'Free Throw Attempts',
                'y_label': 'Free Throw %'
            }
        }
    
    def create_comparison_charts(self, player1_data: Dict, player2_data: Dict, 
                               player1_name: str, player2_name: str) -> plt.Figure:
        """Create multiple scatter plot charts comparing two players"""
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle(f'{player1_name} vs {player2_name} - Shooting Comparison', 
                    fontsize=16, fontweight='bold')
        
        # Create charts for each shot category
        chart_positions = [(0, 0), (0, 1), (1, 0)]
        chart_names = ['3PT', '2PT', 'FT']
        
        for i, category in enumerate(chart_names):
            row, col = chart_positions[i]
            ax = axes[row, col]
            
            self._create_category_chart(ax, player1_data, player2_data, 
                                      player1_name, player2_name, category)
        
        # Create overall efficiency chart in bottom right
        self._create_efficiency_chart(axes[1, 1], player1_data, player2_data, 
                                    player1_name, player2_name)
        
        plt.tight_layout()
        return fig
    
    def _create_category_chart(self, ax, player1_data: Dict, player2_data: Dict,
                             player1_name: str, player2_name: str, category: str):
        """Create a scatter plot for a specific shot category"""
        
        category_info = self.shot_categories[category]
        
        # Extract data for this category
        player1_points = self._extract_category_data(player1_data, category)
        player2_points = self._extract_category_data(player2_data, category)
        
        all_x_values = []
        all_y_values = []
        
        # Plot player 1 data
        if player1_points:
            x1, y1, labels1 = zip(*player1_points)
            all_x_values.extend(x1)
            all_y_values.extend(y1)
            ax.scatter(x1, y1, c='blue', s=100, alpha=0.7, 
                      label=player1_name, edgecolors='black', linewidth=1)
            
            # Add zone labels for player 1
            for i, (x, y, label) in enumerate(player1_points):
                ax.annotate(f'{label}\n{player1_name}', (x, y), 
                           xytext=(5, 5), textcoords='offset points',
                           fontsize=8, alpha=0.8)
        
        # Plot player 2 data
        if player2_points:
            x2, y2, labels2 = zip(*player2_points)
            all_x_values.extend(x2)
            all_y_values.extend(y2)
            ax.scatter(x2, y2, c='red', s=100, alpha=0.7, 
                      label=player2_name, edgecolors='black', linewidth=1)
            
            # Add zone labels for player 2
            for i, (x, y, label) in enumerate(player2_points):
                ax.annotate(f'{label}\n{player2_name}', (x, y), 
                           xytext=(5, -15), textcoords='offset points',
                           fontsize=8, alpha=0.8)
        
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
        ax.legend()
        
        # Add league average lines if available
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
    
    def _create_efficiency_chart(self, ax, player1_data: Dict, player2_data: Dict,
                               player1_name: str, player2_name: str):
        """Create an overall shooting efficiency comparison chart"""
        
        # Calculate total shooting stats
        player1_stats = self._calculate_total_stats(player1_data)
        player2_stats = self._calculate_total_stats(player2_data)
        
        # Create bar chart
        categories = ['Total FGA', 'Total FG%', '3PT FGA', '3PT FG%', '2PT FGA', '2PT FG%']
        player1_values = [
            player1_stats['total_fga'], player1_stats['total_fg_pct'],
            player1_stats['3pt_fga'], player1_stats['3pt_fg_pct'],
            player1_stats['2pt_fga'], player1_stats['2pt_fg_pct']
        ]
        player2_values = [
            player2_stats['total_fga'], player2_stats['total_fg_pct'],
            player2_stats['3pt_fga'], player2_stats['3pt_fg_pct'],
            player2_stats['2pt_fga'], player2_stats['2pt_fg_pct']
        ]
        
        x = np.arange(len(categories))
        width = 0.35
        
        ax.bar(x - width/2, player1_values, width, label=player1_name, 
               color='blue', alpha=0.7)
        ax.bar(x + width/2, player2_values, width, label=player2_name, 
               color='red', alpha=0.7)
        
        ax.set_xlabel('Categories')
        ax.set_ylabel('Values')
        ax.set_title('Overall Shooting Comparison')
        ax.set_xticks(x)
        ax.set_xticklabels(categories, rotation=45, ha='right')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
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
            '2pt_fg_pct': 0
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
        
        # Calculate percentages
        if stats['3pt_fga'] > 0:
            stats['3pt_fg_pct'] = (stats['3pt_fgm'] / stats['3pt_fga']) * 100
        
        if stats['2pt_fga'] > 0:
            stats['2pt_fg_pct'] = (stats['2pt_fgm'] / stats['2pt_fga']) * 100
        
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
    """Main function to demonstrate the scatter chart functionality"""
    charts = BasketballScatterCharts()
    
    print("🏀 Basketball Shot Tracker - Scatter Plot Version")
    print("=" * 60)
    print("This version creates scatter plots with FGA on x-axis and FG% on y-axis")
    print("Separate charts for 3PT, 2PT, and FT shooting")
    print()
    
    # Get player names
    player1_name = input("Enter first player name: ").strip()
    player2_name = input("Enter second player name: ").strip()
    
    print(f"\nGenerating enhanced sample data for {player1_name} and {player2_name}...")
    
    # Get sample data
    player1_data = get_enhanced_sample_data(player1_name)
    player2_data = get_enhanced_sample_data(player2_name)
    
    # Create comparison charts
    fig = charts.create_comparison_charts(player1_data, player2_data, 
                                        player1_name, player2_name)
    
    # Save the chart
    filename = f"{player1_name.replace(' ', '_')}_vs_{player2_name.replace(' ', '_')}_scatter_charts.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Charts saved as: {filename}")
    
    # Show the chart
    plt.show()
    
    # Print detailed statistics
    print(f"\n📊 Detailed Shooting Statistics:")
    print(f"\n{player1_name}:")
    for zone, data in player1_data.items():
        print(f"  {zone}: {data['FG%']:.1f}% ({data.get('FGM', 0)}/{data.get('FGA', 0)})")
    
    print(f"\n{player2_name}:")
    for zone, data in player2_data.items():
        print(f"  {zone}: {data['FG%']:.1f}% ({data.get('FGM', 0)}/{data.get('FGA', 0)})")
    
    print("\n🎯 Chart Interpretation:")
    print("  • X-axis: Field Goal Attempts (FGA)")
    print("  • Y-axis: Field Goal Percentage (FG%)")
    print("  • Blue dots: Player 1")
    print("  • Red dots: Player 2")
    print("  • Dashed line: League average")
    print("  • Higher and more to the right = better efficiency with more volume")

if __name__ == "__main__":
    main()
