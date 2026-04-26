# 📦 Factory-to-Customer Shipping Route Efficiency Analysis

## Project Overview

Efficient logistics operations are critical for timely deliveries, cost optimization, and customer satisfaction. However, large-scale distribution networks often face challenges in identifying inefficient routes, delivery delays, and geographic bottlenecks.

This project analyzes shipping route performance using shipment-level data to uncover inefficiencies across routes, regions, and shipping modes.

The project includes Exploratory Data Analysis (EDA), logistics KPIs, and an interactive Streamlit dashboard for real-time shipping performance analysis.

---

## Project Objectives

Primary Objectives

• Evaluate shipping performance across factory-to-customer routes  
• Identify inefficient routes and delivery bottlenecks  
• Analyze the impact of shipping modes on delivery performance  

Secondary Objectives

• Improve logistics decision-making using data analytics  
• Optimize delivery time and reduce delays  
• Support data-driven supply chain strategies  

---

## Dataset Description

The dataset contains shipment-level logistics data including order details, shipping information, geographic attributes, and financial metrics.

Row ID – Unique record identifier  
Order ID – Unique order identifier  
Order Date – Date when order was placed  
Ship Date – Date when order was shipped  
Ship Mode – Shipping method used  
Customer ID – Unique customer identifier  
Country/Region – Customer country  
City – Customer city  
State/Province – Customer state  
Postal Code – ZIP code  
Region – Customer region  
Product ID – Unique product identifier  
Product Name – Name of product  
Division – Product category  
Sales – Total sales value  
Cost – Product cost  
Gross Profit – Profit (Sales − Cost)

---

## Key Performance Indicators (KPIs)

Shipping Lead Time  
Time taken to deliver an order (Ship Date − Order Date)

Average Lead Time  
Average delivery duration per route

Delay Rate  
Percentage of shipments exceeding the defined lead time threshold

Route Volume  
Total number of shipments per route

Lead Time Variability  
Consistency of delivery performance across shipments

Route Efficiency Score  
Normalized performance metric to compare route efficiency

---

## Analytical Methodology

The project follows a structured analytics workflow:

1. Data Cleaning and Validation  
2. Feature Engineering (Lead Time, Route Mapping)  
3. Exploratory Data Analysis (EDA)  
4. Route-Level Aggregation  
5. KPI Calculation  
6. Efficiency Benchmarking  
7. Geographic Bottleneck Analysis  
8. Ship Mode Performance Analysis  
9. Dashboard Development  

---

## Streamlit Dashboard

An interactive Streamlit dashboard was developed to provide real-time insights into logistics performance.

### Core Modules

• Route Efficiency Overview  
• Geographic Heatmap Analysis  
• Ship Mode Comparison  
• Route Drill-Down Analysis  

### User Capabilities

The dashboard allows dynamic analysis using:

• Date range filters  
• Region and state selection  
• Ship mode filters  
• Lead time threshold adjustment  

---

## Technologies Used

Python  
Pandas  
NumPy  
Plotly  
Streamlit  
Data Visualization  
Exploratory Data Analysis  

---

## How to Run the Project

Install required libraries:

pip install streamlit pandas plotly numpy

Run the dashboard:

streamlit run app.py

---

## Project Deliverables

Exploratory Data Analysis Notebook  
Interactive Streamlit Dashboard  
Research Paper (EDA insights and logistics recommendations)  
Executive Summary for stakeholders  

---

## Live Dashboard

[https://shipping-route-efficiency-analysis-bnvwzlenqu9zroewtmvdh3.streamlit.app/]

---
