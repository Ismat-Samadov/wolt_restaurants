#!/usr/bin/env python3
"""
Wolt Azerbaijan Market Analysis - Chart Generation
Generates business intelligence visualizations for executive decision-making
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set professional style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 11

# Output directory
CHARTS_DIR = Path("charts")
CHARTS_DIR.mkdir(exist_ok=True)

# Load data
print("Loading data...")
restaurants = pd.read_csv("data/restaurants.csv")
menu_items = pd.read_csv("data/menu_items.csv")

print(f"Loaded {len(restaurants)} restaurants and {len(menu_items)} menu items")

# Data preparation
restaurants['rating_score'] = pd.to_numeric(restaurants['rating_score'], errors='coerce')
restaurants['rating_count'] = pd.to_numeric(restaurants['rating_count'], errors='coerce')
restaurants['price_range'] = pd.to_numeric(restaurants['price_range'], errors='coerce')
restaurants['delivery_price_int'] = pd.to_numeric(restaurants['delivery_price_int'], errors='coerce')
menu_items['item_price'] = pd.to_numeric(menu_items['item_price'], errors='coerce')


# ============================================================================
# 1. MARKET PRESENCE ANALYSIS
# ============================================================================

def generate_market_presence_charts():
    """Generate charts showing market presence across cities"""
    print("\n1. Generating market presence analysis...")

    # Chart 1.1: Restaurant count by city
    fig, ax = plt.subplots(figsize=(12, 6))
    city_counts = restaurants['city'].value_counts().sort_values(ascending=True)
    city_counts.plot(kind='barh', ax=ax, color='#2E86AB')
    ax.set_xlabel('Number of Restaurants')
    ax.set_ylabel('City')
    ax.set_title('Market Presence: Restaurant Distribution Across Azerbaijan Cities')
    ax.grid(axis='x', alpha=0.3)

    # Add value labels
    for i, v in enumerate(city_counts):
        ax.text(v + 1, i, str(v), va='center', fontweight='bold')

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / '01_restaurant_distribution_by_city.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Chart 1.2: Menu items per city
    fig, ax = plt.subplots(figsize=(12, 6))
    city_menu_counts = menu_items['city'].value_counts().sort_values(ascending=True)
    city_menu_counts.plot(kind='barh', ax=ax, color='#A23B72')
    ax.set_xlabel('Total Menu Items')
    ax.set_ylabel('City')
    ax.set_title('Menu Variety: Total Menu Items Available by City')
    ax.grid(axis='x', alpha=0.3)

    for i, v in enumerate(city_menu_counts):
        ax.text(v + 50, i, str(v), va='center', fontweight='bold')

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / '02_menu_items_by_city.png', dpi=300, bbox_inches='tight')
    plt.close()


# ============================================================================
# 2. PRICING STRATEGY ANALYSIS
# ============================================================================

def generate_pricing_charts():
    """Generate charts analyzing pricing strategies"""
    print("\n2. Generating pricing analysis...")

    # Chart 2.1: Price range distribution
    fig, ax = plt.subplots(figsize=(10, 6))
    price_dist = restaurants['price_range'].value_counts().sort_index()
    price_labels = {1: 'Budget\n(₼)', 2: 'Moderate\n(₼₼)', 3: 'Premium\n(₼₼₼)', 4: 'Luxury\n(₼₼₼₼)'}
    price_dist.index = price_dist.index.map(lambda x: price_labels.get(x, f'Level {x}'))

    colors = ['#06D6A0', '#118AB2', '#073B4C', '#EF476F']
    ax.bar(range(len(price_dist)), price_dist.values, color=colors[:len(price_dist)])
    ax.set_xticks(range(len(price_dist)))
    ax.set_xticklabels(price_dist.index)
    ax.set_ylabel('Number of Restaurants')
    ax.set_title('Price Positioning: Restaurant Distribution by Price Tier')
    ax.grid(axis='y', alpha=0.3)

    # Add value labels
    for i, v in enumerate(price_dist.values):
        ax.text(i, v + 2, str(v), ha='center', fontweight='bold')

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / '03_price_tier_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Chart 2.2: Average menu item price by city
    menu_with_city = menu_items[menu_items['item_price'] > 0].copy()

    # Convert to AZN (assuming ALL is Albanian Lek, rough conversion for comparison)
    menu_with_city['price_azn'] = menu_with_city['item_price'] / 100

    fig, ax = plt.subplots(figsize=(12, 6))
    avg_price_by_city = menu_with_city.groupby('city')['price_azn'].mean().sort_values(ascending=True)
    avg_price_by_city.plot(kind='barh', ax=ax, color='#F18F01')
    ax.set_xlabel('Average Menu Item Price (AZN)')
    ax.set_ylabel('City')
    ax.set_title('Pricing Landscape: Average Menu Item Price by City')
    ax.grid(axis='x', alpha=0.3)

    for i, v in enumerate(avg_price_by_city):
        ax.text(v + 0.05, i, f'₼{v:.2f}', va='center', fontweight='bold')

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / '04_average_price_by_city.png', dpi=300, bbox_inches='tight')
    plt.close()


# ============================================================================
# 3. CUSTOMER SATISFACTION ANALYSIS
# ============================================================================

def generate_satisfaction_charts():
    """Generate charts analyzing customer satisfaction"""
    print("\n3. Generating customer satisfaction analysis...")

    # Chart 3.1: Rating distribution
    fig, ax = plt.subplots(figsize=(10, 6))
    restaurants_with_ratings = restaurants[restaurants['rating_score'].notna()]

    # Create rating bins
    bins = [0, 7.0, 8.0, 9.0, 10.0]
    labels = ['Needs Improvement\n(< 7.0)', 'Good\n(7.0-8.0)', 'Excellent\n(8.0-9.0)', 'Outstanding\n(9.0+)']
    restaurants_with_ratings['rating_category'] = pd.cut(restaurants_with_ratings['rating_score'],
                                                          bins=bins, labels=labels, include_lowest=True)

    rating_dist = restaurants_with_ratings['rating_category'].value_counts()
    colors = ['#EF476F', '#FFD166', '#06D6A0', '#118AB2']

    ax.bar(range(len(rating_dist)), rating_dist.values,
           color=[colors[i] for i in range(len(rating_dist))])
    ax.set_xticks(range(len(rating_dist)))
    ax.set_xticklabels(rating_dist.index, rotation=0)
    ax.set_ylabel('Number of Restaurants')
    ax.set_title('Customer Satisfaction: Restaurant Performance Distribution')
    ax.grid(axis='y', alpha=0.3)

    for i, v in enumerate(rating_dist.values):
        ax.text(i, v + 2, str(v), ha='center', fontweight='bold')

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / '05_satisfaction_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Chart 3.2: Top 15 highest-rated restaurants
    fig, ax = plt.subplots(figsize=(12, 8))
    top_rated = restaurants_with_ratings.nlargest(15, 'rating_score')[['name', 'rating_score', 'rating_count']]

    ax.barh(range(len(top_rated)), top_rated['rating_score'].values, color='#06D6A0')
    ax.set_yticks(range(len(top_rated)))
    ax.set_yticklabels(top_rated['name'].values)
    ax.set_xlabel('Customer Rating (out of 10)')
    ax.set_title('Market Leaders: Top 15 Highest-Rated Restaurants')
    ax.grid(axis='x', alpha=0.3)
    ax.set_xlim(0, 10)

    # Add rating values and review counts
    for i, (score, count) in enumerate(zip(top_rated['rating_score'].values,
                                            top_rated['rating_count'].values)):
        ax.text(score + 0.1, i, f'{score:.1f} ({int(count)} reviews)',
                va='center', fontsize=9)

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / '06_top_rated_restaurants.png', dpi=300, bbox_inches='tight')
    plt.close()


# ============================================================================
# 4. OPERATIONAL EFFICIENCY
# ============================================================================

def generate_operations_charts():
    """Generate charts analyzing operational efficiency"""
    print("\n4. Generating operational efficiency analysis...")

    # Chart 4.1: Delivery cost distribution
    delivery_rest = restaurants[restaurants['delivery_price_int'].notna() &
                                 (restaurants['delivery_price_int'] >= 0)]

    fig, ax = plt.subplots(figsize=(10, 6))

    # Group by delivery cost
    delivery_rest['delivery_category'] = pd.cut(delivery_rest['delivery_price_int'] / 100,
                                                  bins=[-0.1, 0.1, 2, 5, 100],
                                                  labels=['Free Delivery', 'Low Cost\n(< ₼2)',
                                                          'Moderate\n(₼2-5)', 'Premium\n(> ₼5)'])

    delivery_dist = delivery_rest['delivery_category'].value_counts()
    colors = ['#06D6A0', '#118AB2', '#FFD166', '#EF476F']

    ax.bar(range(len(delivery_dist)), delivery_dist.values,
           color=[colors[i] for i in range(len(delivery_dist))])
    ax.set_xticks(range(len(delivery_dist)))
    ax.set_xticklabels(delivery_dist.index)
    ax.set_ylabel('Number of Restaurants')
    ax.set_title('Delivery Strategy: Cost Distribution Across Restaurants')
    ax.grid(axis='y', alpha=0.3)

    for i, v in enumerate(delivery_dist.values):
        pct = (v / len(delivery_rest)) * 100
        ax.text(i, v + 5, f'{v}\n({pct:.1f}%)', ha='center', fontweight='bold')

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / '07_delivery_cost_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Chart 4.2: Menu size analysis
    menu_count = menu_items.groupby('restaurant_id').size().reset_index(name='menu_size')
    menu_with_info = menu_count.merge(restaurants[['id', 'name']],
                                       left_on='restaurant_id', right_on='id')

    fig, ax = plt.subplots(figsize=(12, 8))
    top_menu_size = menu_with_info.nlargest(15, 'menu_size')

    ax.barh(range(len(top_menu_size)), top_menu_size['menu_size'].values, color='#A23B72')
    ax.set_yticks(range(len(top_menu_size)))
    ax.set_yticklabels(top_menu_size['name'].values)
    ax.set_xlabel('Number of Menu Items')
    ax.set_title('Menu Complexity: Restaurants with Most Extensive Offerings')
    ax.grid(axis='x', alpha=0.3)

    for i, v in enumerate(top_menu_size['menu_size'].values):
        ax.text(v + 5, i, str(v), va='center', fontweight='bold')

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / '08_menu_complexity.png', dpi=300, bbox_inches='tight')
    plt.close()


# ============================================================================
# 5. COMPETITIVE LANDSCAPE
# ============================================================================

def generate_competitive_charts():
    """Generate charts analyzing competitive dynamics"""
    print("\n5. Generating competitive landscape analysis...")

    # Chart 5.1: Market concentration by city (top 10 restaurants per city)
    fig, ax = plt.subplots(figsize=(12, 6))

    # Get review volume by city
    city_reviews = restaurants.groupby('city')['rating_count'].sum().sort_values(ascending=True)

    ax.barh(range(len(city_reviews)), city_reviews.values, color='#073B4C')
    ax.set_yticks(range(len(city_reviews)))
    ax.set_yticklabels(city_reviews.index)
    ax.set_xlabel('Total Customer Reviews')
    ax.set_title('Market Engagement: Total Customer Reviews by City')
    ax.grid(axis='x', alpha=0.3)

    for i, v in enumerate(city_reviews.values):
        ax.text(v + 50, i, f'{int(v):,}', va='center', fontweight='bold')

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / '09_market_engagement_by_city.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Chart 5.2: Price vs Quality positioning
    fig, ax = plt.subplots(figsize=(12, 8))

    # Filter restaurants with both ratings and price range
    positioned_rest = restaurants[restaurants['rating_score'].notna() &
                                   restaurants['price_range'].notna() &
                                   (restaurants['rating_count'] > 10)]

    # Create scatter plot
    scatter = ax.scatter(positioned_rest['price_range'],
                        positioned_rest['rating_score'],
                        s=positioned_rest['rating_count'] / 5,  # Size by review volume
                        alpha=0.6,
                        c=positioned_rest['rating_score'],
                        cmap='RdYlGn',
                        edgecolors='black',
                        linewidth=0.5)

    ax.set_xlabel('Price Tier (1=Budget, 2=Moderate, 3=Premium, 4=Luxury)')
    ax.set_ylabel('Customer Rating (out of 10)')
    ax.set_title('Strategic Positioning: Price vs Quality (bubble size = review volume)')
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0.5, 4.5)
    ax.set_ylim(5, 10)

    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Customer Rating')

    # Add quadrant lines
    ax.axhline(y=8.5, color='gray', linestyle='--', alpha=0.5, linewidth=1)
    ax.axvline(x=2.5, color='gray', linestyle='--', alpha=0.5, linewidth=1)

    # Add quadrant labels
    ax.text(1.5, 9.5, 'Budget\nChampions', ha='center', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
    ax.text(3.5, 9.5, 'Premium\nLeaders', ha='center', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='gold', alpha=0.7))
    ax.text(1.5, 6, 'Budget\nOpportunity', ha='center', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.7))
    ax.text(3.5, 6, 'Premium\nRisk', ha='center', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='orange', alpha=0.7))

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / '10_price_quality_positioning.png', dpi=300, bbox_inches='tight')
    plt.close()


# ============================================================================
# 6. GROWTH OPPORTUNITIES
# ============================================================================

def generate_opportunity_charts():
    """Generate charts identifying growth opportunities"""
    print("\n6. Generating opportunity analysis...")

    # Chart 6.1: Cities with high ratings but fewer restaurants
    fig, ax = plt.subplots(figsize=(12, 6))

    city_metrics = restaurants.groupby('city').agg({
        'id': 'count',
        'rating_score': 'mean'
    }).reset_index()
    city_metrics.columns = ['city', 'restaurant_count', 'avg_rating']
    city_metrics = city_metrics.dropna()
    city_metrics = city_metrics.sort_values('avg_rating', ascending=True)

    # Create horizontal bar chart with two axes
    x = np.arange(len(city_metrics))
    width = 0.35

    ax2 = ax.twiny()

    bars1 = ax.barh(x - width/2, city_metrics['restaurant_count'].values,
                    width, label='Number of Restaurants', color='#2E86AB', alpha=0.8)
    bars2 = ax2.barh(x + width/2, city_metrics['avg_rating'].values,
                     width, label='Avg Rating', color='#06D6A0', alpha=0.8)

    ax.set_yticks(x)
    ax.set_yticklabels(city_metrics['city'].values)
    ax.set_xlabel('Number of Restaurants', color='#2E86AB')
    ax2.set_xlabel('Average Rating (out of 10)', color='#06D6A0')
    ax.set_title('Market Opportunity: Restaurant Count vs Customer Satisfaction by City')
    ax.legend(loc='lower right')
    ax2.legend(loc='lower left')
    ax.grid(axis='x', alpha=0.3)

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / '11_opportunity_matrix.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Chart 6.2: Menu item price distribution
    fig, ax = plt.subplots(figsize=(12, 6))

    menu_prices = menu_items[menu_items['item_price'] > 0]['item_price'] / 100

    # Create histogram
    n, bins, patches = ax.hist(menu_prices, bins=50, color='#F18F01', edgecolor='black', alpha=0.7)

    # Color bars based on price ranges
    for i, patch in enumerate(patches):
        if bins[i] < 2:
            patch.set_facecolor('#06D6A0')
        elif bins[i] < 5:
            patch.set_facecolor('#FFD166')
        elif bins[i] < 10:
            patch.set_facecolor('#F18F01')
        else:
            patch.set_facecolor('#EF476F')

    ax.set_xlabel('Menu Item Price (AZN)')
    ax.set_ylabel('Number of Menu Items')
    ax.set_title('Pricing Distribution: Menu Item Price Points Across Market')
    ax.grid(axis='y', alpha=0.3)
    ax.set_xlim(0, 20)

    # Add median and mean lines
    median_price = menu_prices.median()
    mean_price = menu_prices.mean()
    ax.axvline(median_price, color='red', linestyle='--', linewidth=2,
               label=f'Median: ₼{median_price:.2f}')
    ax.axvline(mean_price, color='darkred', linestyle=':', linewidth=2,
               label=f'Mean: ₼{mean_price:.2f}')
    ax.legend()

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / '12_price_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()


# ============================================================================
# 7. KEY METRICS SUMMARY
# ============================================================================

def generate_summary_chart():
    """Generate executive summary dashboard"""
    print("\n7. Generating executive summary...")

    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    fig.suptitle('Executive Dashboard: Azerbaijan Food Delivery Market Overview',
                 fontsize=16, fontweight='bold')

    # Metric 1: Total market size
    ax = axes[0, 0]
    metrics = {
        'Restaurants': len(restaurants),
        'Menu Items': len(menu_items),
        'Cities': restaurants['city'].nunique()
    }
    colors_m = ['#2E86AB', '#A23B72', '#F18F01']
    bars = ax.bar(metrics.keys(), metrics.values(), color=colors_m)
    ax.set_ylabel('Count')
    ax.set_title('Market Size', fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    for bar, value in zip(bars, metrics.values()):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(value):,}', ha='center', va='bottom', fontweight='bold')

    # Metric 2: Average ratings
    ax = axes[0, 1]
    avg_rating = restaurants['rating_score'].mean()
    total_reviews = restaurants['rating_count'].sum()

    ax.bar(['Avg Rating'], [avg_rating], color='#06D6A0', width=0.5)
    ax.set_ylim(0, 10)
    ax.set_ylabel('Rating (out of 10)')
    ax.set_title(f'Customer Satisfaction\n({int(total_reviews):,} total reviews)', fontweight='bold')
    ax.text(0, avg_rating + 0.3, f'{avg_rating:.2f}', ha='center',
            fontweight='bold', fontsize=14)
    ax.grid(axis='y', alpha=0.3)

    # Metric 3: Price distribution
    ax = axes[0, 2]
    price_counts = restaurants['price_range'].value_counts().sort_index()
    price_pcts = (price_counts / len(restaurants) * 100)

    colors_p = ['#06D6A0', '#118AB2', '#073B4C', '#EF476F']
    bars = ax.bar([f'₼'*int(i) for i in price_counts.index],
                  price_pcts.values, color=colors_p[:len(price_pcts)])
    ax.set_ylabel('Percentage of Restaurants')
    ax.set_title('Price Tier Distribution', fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    for bar, value in zip(bars, price_pcts.values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{value:.1f}%', ha='center', va='bottom', fontweight='bold')

    # Metric 4: Top cities by restaurants
    ax = axes[1, 0]
    top_cities = restaurants['city'].value_counts().head(5)
    ax.barh(range(len(top_cities)), top_cities.values, color='#2E86AB')
    ax.set_yticks(range(len(top_cities)))
    ax.set_yticklabels(top_cities.index)
    ax.set_xlabel('Restaurants')
    ax.set_title('Top 5 Cities by Restaurants', fontweight='bold')
    ax.grid(axis='x', alpha=0.3)
    for i, v in enumerate(top_cities.values):
        ax.text(v + 1, i, str(v), va='center', fontweight='bold')

    # Metric 5: Delivery cost
    ax = axes[1, 1]
    free_delivery = len(restaurants[restaurants['delivery_price_int'] == 0])
    paid_delivery = len(restaurants[restaurants['delivery_price_int'] > 0])

    delivery_data = [free_delivery, paid_delivery]
    delivery_labels = ['Free\nDelivery', 'Paid\nDelivery']
    colors_d = ['#06D6A0', '#FFD166']

    bars = ax.bar(delivery_labels, delivery_data, color=colors_d)
    ax.set_ylabel('Number of Restaurants')
    ax.set_title('Delivery Cost Strategy', fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    for bar, value in zip(bars, delivery_data):
        height = bar.get_height()
        pct = (value / len(restaurants)) * 100
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{value}\n({pct:.1f}%)', ha='center', va='bottom', fontweight='bold')

    # Metric 6: Menu size average
    ax = axes[1, 2]
    menu_sizes = menu_items.groupby('restaurant_id').size()
    avg_menu_size = menu_sizes.mean()
    median_menu_size = menu_sizes.median()
    max_menu_size = menu_sizes.max()

    stats = ['Average', 'Median', 'Maximum']
    values = [avg_menu_size, median_menu_size, max_menu_size]
    colors_s = ['#118AB2', '#06D6A0', '#F18F01']

    bars = ax.bar(stats, values, color=colors_s)
    ax.set_ylabel('Menu Items per Restaurant')
    ax.set_title('Menu Complexity', fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(value)}', ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / '00_executive_dashboard.png', dpi=300, bbox_inches='tight')
    plt.close()


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Generate all charts"""
    print("="*70)
    print("WOLT AZERBAIJAN MARKET ANALYSIS - CHART GENERATION")
    print("="*70)

    generate_summary_chart()
    generate_market_presence_charts()
    generate_pricing_charts()
    generate_satisfaction_charts()
    generate_operations_charts()
    generate_competitive_charts()
    generate_opportunity_charts()

    print("\n" + "="*70)
    print("ALL CHARTS GENERATED SUCCESSFULLY!")
    print(f"Charts saved to: {CHARTS_DIR.absolute()}")
    print("="*70)


if __name__ == "__main__":
    main()
