# Intel Processor Price and Performance Dashboard

## **Motivation**
Understanding the balance between price and performance is crucial for professionals, gamers, and tech enthusiasts when choosing an Intel processor. This dashboard provides a visual analysis of Intel processors over the years, helping users compare pricing trends, performance improvements, and series-wise differences. Whether you're building a PC or analyzing market trends, this tool offers valuable insights.

## **App Description**
The **Intel Processor Price and Performance Dashboard** is an interactive web application built using **Dash** and **Plotly**. It provides:

Walkthrough video: watch a demo video in the below file
[Watch the demo](/walkthrough.mp4)


- **Price Trends Over Time:** Line graph showing the price evolution of different Intel series.
- **Series Price Comparison:** Box plot for comparing prices across Intel series.
- **Price Distribution Over Years:** Bar graph visualizing price variations.
- **Performance Over Time:** Line graph showing clock rate trends over different series.

Users can filter results using:
- **Intel Series Dropdown:** Select multiple Intel series for comparison.
- **Launch Year Slider:** Adjust the range of years to focus on specific periods.

The dashboard is designed with a **blue Intel-themed background**, interactive plots, and a clean layout to enhance usability.

## **Installation Instructions**
Follow these steps to set up and run the dashboard locally:

### **1. Clone the repository**
```bash
git clone https://github.com/yourusername/intel_dashboard.git
cd intel_dashboard
```

### **2. Create and activate a Conda environment**
```bash
conda create --name intel_dashboard python=3.9 -y
conda activate intel_dashboard
```

### **3. Run the app**
```bash
python app.py
```

Now, open your browser and go to **http://127.0.0.1:8050/** to access the dashboard! 🚀

