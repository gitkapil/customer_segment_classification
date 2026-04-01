"""
Customer Segmentation Dashboard (Quick Version)

Fast interactive dashboard for management presentation.
Works directly with CSV data.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add modules to path
sys.path.insert(0, str(Path(__file__).parent))

from config.config import *

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')


class QuickDashboard:
    """Generate interactive dashboard quickly."""
    
    def __init__(self, csv_path=None):
        """Initialize dashboard with CSV data."""
        if csv_path is None:
            csv_path = INPUT_FILE
        
        print(f"Loading data from: {csv_path}")
        
        # Try different encodings
        encodings = ['utf-8', 'iso-8859-1', 'latin1', 'cp1252']
        df = None
        
        for encoding in encodings:
            try:
                df = pd.read_csv(csv_path, encoding=encoding)
                print(f"✓ Successfully loaded with encoding: {encoding}")
                break
            except UnicodeDecodeError:
                continue
        
        if df is None:
            raise ValueError(f"Could not read CSV with any supported encoding")
        
        self.df = df
        self.df['InvoiceDate'] = pd.to_datetime(self.df['InvoiceDate'])
        self.df['TotalPrice'] = self.df['Quantity'] * self.df['UnitPrice']
        
        print(f"✓ Loaded {len(self.df):,} rows")
    
    def create_full_dashboard(self):
        """Create comprehensive dashboard."""
        print("Generating dashboard visualizations...")
        
        # Create subplots
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=(
                'Top 10 Countries by Transactions',
                'Top 10 Countries by Revenue',
                'Product Price Distribution',
                'Transaction Timeline',
                'Transaction Amount Distribution',
                'Top 10 Customers by Transaction Count'
            ),
            specs=[
                [{"secondary_y": False}, {"secondary_y": False}],
                [{"secondary_y": False}, {"secondary_y": False}],
                [{"secondary_y": False}, {"secondary_y": False}]
            ],
            vertical_spacing=0.12,
            horizontal_spacing=0.12
        )
        
        # 1. Top Countries (top left)
        country_data = self.df['Country'].value_counts().head(10)
        fig.add_trace(
            go.Bar(
                x=country_data.values,
                y=country_data.index,
                orientation='h',
                marker=dict(
                    color=country_data.values,
                    colorscale='Blues',
                    showscale=False
                ),
                text=country_data.values,
                textposition='auto',
                name='Transactions',
                hovertemplate='<b>%{y}</b><br>Transactions: %{x:,}',
                showlegend=False
            ),
            row=1, col=1
        )
        
        # 2. Revenue by Country bar (top right)
        revenue_by_country = self.df.groupby('Country')['TotalPrice'].sum().sort_values(ascending=False).head(10)
        fig.add_trace(
            go.Bar(
                x=revenue_by_country.values,
                y=revenue_by_country.index,
                orientation='h',
                marker=dict(
                    color=revenue_by_country.values,
                    colorscale='Greens',
                    showscale=False
                ),
                text=[f"${x:,.0f}" for x in revenue_by_country.values],
                textposition='auto',
                name='Revenue',
                hovertemplate='<b>%{y}</b><br>Revenue: $%{x:,.0f}',
                showlegend=False
            ),
            row=1, col=2
        )
        
        # 3. Price Distribution (middle left)
        fig.add_trace(
            go.Histogram(
                x=self.df['UnitPrice'],
                nbinsx=50,
                marker=dict(color='#3498db', opacity=0.7),
                name='Unit Price',
                hovertemplate='Price: $%{x:.2f}<br>Count: %{y:,}',
                showlegend=False
            ),
            row=2, col=1
        )
        
        # 4. Transaction Timeline (middle right)
        daily_sales = self.df.groupby(self.df['InvoiceDate'].dt.date).agg({
            'InvoiceNo': 'count',
            'TotalPrice': 'sum'
        }).reset_index()
        daily_sales.columns = ['Date', 'Count', 'Revenue']
        
        fig.add_trace(
            go.Scatter(
                x=daily_sales['Date'],
                y=daily_sales['Count'],
                mode='lines',
                name='Transactions',
                line=dict(color='#2ecc71', width=2),
                fill='tozeroy',
                hovertemplate='%{x}<br>Transactions: %{y:,}',
                showlegend=False
            ),
            row=2, col=2
        )
        
        # 5. Amount Distribution (bottom left)
        fig.add_trace(
            go.Histogram(
                x=self.df['TotalPrice'],
                nbinsx=50,
                marker=dict(color='#e74c3c', opacity=0.7),
                name='Total Price',
                hovertemplate='Amount: $%{x:.2f}<br>Count: %{y:,}',
                showlegend=False
            ),
            row=3, col=1
        )
        
        # 6. Top Customers by Transaction Count (bottom right)
        top_customers = self.df['CustomerID'].value_counts().head(10)
        fig.add_trace(
            go.Bar(
                x=top_customers.index.astype(str),
                y=top_customers.values,
                marker=dict(
                    color=top_customers.values,
                    colorscale='Oranges',
                    showscale=False
                ),
                text=top_customers.values,
                textposition='auto',
                name='Transactions',
                hovertemplate='Customer: %{x}<br>Transactions: %{y:,}',
                showlegend=False
            ),
            row=3, col=2
        )
        
        # Update axes labels
        fig.update_xaxes(title_text="Transactions", row=1, col=1)
        fig.update_yaxes(title_text="Country", row=1, col=1)
        
        fig.update_xaxes(title_text="Revenue ($)", row=1, col=2)
        fig.update_yaxes(title_text="Country", row=1, col=2)
        
        fig.update_xaxes(title_text="Unit Price ($)", row=2, col=1)
        fig.update_yaxes(title_text="Frequency", row=2, col=1)
        
        fig.update_xaxes(title_text="Date", row=2, col=2)
        fig.update_yaxes(title_text="Transactions", row=2, col=2)
        
        fig.update_xaxes(title_text="Transaction Amount ($)", row=3, col=1)
        fig.update_yaxes(title_text="Frequency", row=3, col=1)
        
        fig.update_xaxes(title_text="Customer ID", row=3, col=2)
        fig.update_yaxes(title_text="Transaction Count", row=3, col=2)
        
        fig.update_layout(
            title_text="<b>Customer Segmentation Analytics Dashboard</b><br><sub>6-Panel Overview</sub>",
            height=1400,
            showlegend=False,
            hovermode='closest',
            template='plotly_white',
            font=dict(family="Arial, sans-serif", size=11)
        )
        
        return fig
    
    def get_key_metrics(self):
        """Calculate key metrics."""
        return {
            'Total Customers': len(self.df['CustomerID'].unique()),
            'Total Transactions': len(self.df),
            'Total Products': len(self.df['StockCode'].unique()),
            'Countries': len(self.df['Country'].unique()),
            'Avg Transaction Value': self.df['TotalPrice'].mean(),
            'Total Revenue': self.df['TotalPrice'].sum(),
            'Avg Quantity': self.df['Quantity'].mean(),
            'Date Range': f"{self.df['InvoiceDate'].min().date()} to {self.df['InvoiceDate'].max().date()}"
        }
    
    def create_metrics_html(self):
        """Create metrics cards HTML."""
        metrics = self.get_key_metrics()
        
        cards = f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
            <div class="metric-label">Total Customers</div>
            <div class="metric-value">{metrics['Total Customers']:,}</div>
        </div>
        <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <div class="metric-label">Total Transactions</div>
            <div class="metric-value">{metrics['Total Transactions']:,}</div>
        </div>
        <div class="metric-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <div class="metric-label">Unique Products</div>
            <div class="metric-value">{metrics['Total Products']:,}</div>
        </div>
        <div class="metric-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
            <div class="metric-label">Countries</div>
            <div class="metric-value">{metrics['Countries']}</div>
        </div>
        <div class="metric-card" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
            <div class="metric-label">Avg Transaction</div>
            <div class="metric-value">${metrics['Avg Transaction Value']:.2f}</div>
        </div>
        <div class="metric-card" style="background: linear-gradient(135deg, #30cfd0 0%, #330867 100%);">
            <div class="metric-label">Total Revenue</div>
            <div class="metric-value">${metrics['Total Revenue']:,.0f}</div>
        </div>
        """
        
        return cards
    
    def save_dashboard(self, output_path=None):
        """Save dashboard to HTML file."""
        if output_path is None:
            output_path = OUTPUT_DIR / 'dashboard.html'
        
        print(f"Creating dashboard at {output_path}...")
        
        # Get metrics
        metrics_html = self.create_metrics_html()
        
        # Create dashboard
        fig = self.create_full_dashboard()
        dashboard_json = fig.to_json()
        
        # Create HTML
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Customer Segmentation Dashboard</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                    color: #333;
                    padding: 20px;
                }}
                
                .container {{
                    max-width: 1600px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 12px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                    overflow: hidden;
                }}
                
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 40px;
                    text-align: center;
                }}
                
                .header h1 {{
                    font-size: 2.8em;
                    margin-bottom: 10px;
                    font-weight: 700;
                }}
                
                .header p {{
                    font-size: 1.1em;
                    opacity: 0.9;
                }}
                
                .metrics {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                    gap: 20px;
                    padding: 40px;
                    background: #f8f9fa;
                }}
                
                .metric-card {{
                    padding: 30px 25px;
                    border-radius: 10px;
                    color: white;
                    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
                    transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
                    cursor: pointer;
                    text-align: center;
                }}
                
                .metric-card:hover {{
                    transform: translateY(-8px);
                    box-shadow: 0 15px 40px rgba(0,0,0,0.25);
                }}
                
                .metric-label {{
                    font-size: 0.95em;
                    opacity: 0.95;
                    font-weight: 500;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                    margin-bottom: 12px;
                }}
                
                .metric-value {{
                    font-size: 2.2em;
                    font-weight: 700;
                    letter-spacing: -1px;
                }}
                
                .content {{
                    padding: 40px;
                }}
                
                .chart-section {{
                    margin-bottom: 30px;
                }}
                
                .chart-title {{
                    font-size: 1.5em;
                    font-weight: 700;
                    color: #2c3e50;
                    margin-bottom: 20px;
                    display: flex;
                    align-items: center;
                }}
                
                .chart-title::before {{
                    content: '';
                    width: 5px;
                    height: 25px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border-radius: 3px;
                    margin-right: 15px;
                }}
                
                #dashboard {{
                    border-radius: 10px;
                    box-shadow: 0 3px 15px rgba(0,0,0,0.1);
                    overflow: hidden;
                }}
                
                .footer {{
                    background: #2c3e50;
                    color: white;
                    padding: 30px 40px;
                    text-align: center;
                    font-size: 0.95em;
                }}
                
                .footer p {{
                    margin: 5px 0;
                }}
                
                .footer-highlight {{
                    color: #3498db;
                    font-weight: 600;
                }}
                
                @media (max-width: 768px) {{
                    .header h1 {{
                        font-size: 1.8em;
                    }}
                    .metrics {{
                        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                        gap: 15px;
                        padding: 20px;
                    }}
                    .content {{
                        padding: 20px;
                    }}
                    .metric-value {{
                        font-size: 1.5em;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📊 Customer Segmentation Analytics</h1>
                    <p>Interactive Dashboard for Strategic Decision Making</p>
                </div>
                
                <div class="metrics">
                    {metrics_html}
                </div>
                
                <div class="content">
                    <div class="chart-section">
                        <div class="chart-title">Analytics Overview</div>
                        <div id="dashboard"></div>
                    </div>
                </div>
                
                <div class="footer">
                    <p><span class="footer-highlight">📈 Dashboard Generated:</span> {pd.Timestamp.now().strftime('%B %d, %Y at %H:%M:%S')}</p>
                    <p>Customer Segmentation & Classification Analytics Platform</p>
                    <p style="margin-top: 15px; opacity: 0.7;">💡 Tip: Hover over charts for details • Click legend to toggle series • Use camera icon to export</p>
                </div>
            </div>
            
            <script>
                var dashboardData = {dashboard_json};
                Plotly.newPlot('dashboard', dashboardData.data, dashboardData.layout, {{responsive: true, displayModeBar: true, displaylogo: false}});
            </script>
        </body>
        </html>
        """
        
        # Save to file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✓ Dashboard saved successfully!")
        print(f"✓ Location: {output_path}")
        return str(output_path)


def main():
    """Generate dashboard."""
    print("=" * 70)
    print("CUSTOMER SEGMENTATION DASHBOARD GENERATOR".center(70))
    print("=" * 70)
    
    try:
        # Initialize dashboard
        dashboard = QuickDashboard()
        
        # Print metrics
        metrics = dashboard.get_key_metrics()
        print("\n📊 Key Metrics:")
        print("-" * 70)
        for key, value in metrics.items():
            if isinstance(value, (int, float)) and key in ['Avg Transaction Value', 'Total Revenue']:
                print(f"  {key:.<45} ${value:>15,.2f}")
            elif isinstance(value, (int, float)):
                print(f"  {key:.<45} {value:>15,}")
            else:
                print(f"  {key:.<45} {value:>15}")
        
        # Save dashboard
        dashboard_path = dashboard.save_dashboard()
        
        print("\n" + "=" * 70)
        print("DASHBOARD GENERATION COMPLETE".center(70))
        print("=" * 70)
        print(f"\n✨ Your interactive dashboard is ready for presentation!")
        print(f"\n📁 File Location:")
        print(f"   {dashboard_path}")
        print(f"\n🚀 How to use:")
        print(f"   1. Open the HTML file in any web browser")
        print(f"   2. Hover over charts to see detailed information")
        print(f"   3. Click on legend items to show/hide data series")
        print(f"   4. Use the camera icon to export charts as images")
        print(f"   5. Share with stakeholders for review")
        print("\n" + "=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
