# Common Visualizations

Source: https://notes.kodekloud.com/docs/DP-900-Microsoft-Azure-Data-Fundamentals/Analyzing-Data/Common-Visualizations/page

This article discusses various data visualization techniques used in analytics to convey insights effectively.

Data visualization plays a crucial role in turning raw numbers into actionable insights. Depending on the story you want to tell, you can choose from four reporting styles:

* **Descriptive**: Record what happened.
* **Diagnostic**: Explain why it happened.
* **Predictive**: Forecast what will happen next.
* **Prescriptive**: Recommend actions to influence future outcomes.

<Frame>
  ![The image outlines four kinds of reporting: Descriptive, Diagnostic, Predictive, and Prescriptive, each with a brief explanation of its focus.](../../../../images/kodekloud.com/kk-media/image/upload/v1752872825/notes-assets/images/DP-900-Microsoft-Azure-Data-Fundamentals-Common-Visualizations/reporting-types-descriptive-diagnostic-predictive-prescriptive.jpg)
</Frame>

***

## 1. Descriptive Visualization: Tables

A table is the simplest way to display raw data. It lists exact values in rows and columns, making it ideal for descriptive analytics.

<Frame>
  ![The image shows a table listing first names, last names, and order dates, with a note about common visualizations and a button labeled "Descriptive."](../../../../images/kodekloud.com/kk-media/image/upload/v1752872826/notes-assets/images/DP-900-Microsoft-Azure-Data-Fundamentals-Common-Visualizations/names-orders-visualizations-table.jpg)
</Frame>

***

## 2. Diagnostic Visualization: Bar & Column Charts

Bar and column charts excel at comparing categories side by side, helping you spot patterns and outliers quickly.

| Chart Type                | Use Case                                      | Example                         |
| ------------------------- | --------------------------------------------- | ------------------------------- |
| Bar Chart (Horizontal)    | Compare single measure across categories      | Shipping fees by city           |
| Column Chart (Vertical)   | Track changes over time or categories         | Monthly sales                   |
| Clustered Column Chart    | Compare two measures in each category         | Shipping fees vs. taxes by city |
| Stacked Column Chart      | Show part-to-whole across categories          | Expense breakdown by department |
| 100% Stacked Column Chart | Normalize categories to 100% for contribution | Market share by region          |

<Frame>
  ![The image shows four bar and column charts comparing shipping fees and taxes by city, labeled under "Common Visualizations: Bars, Columns." It includes a "Diagnostic" button and the phrase "Compare values."](../../../../images/kodekloud.com/kk-media/image/upload/v1752872827/notes-assets/images/DP-900-Microsoft-Azure-Data-Fundamentals-Common-Visualizations/shipping-fees-taxes-comparison-charts.jpg)
</Frame>

***

## 3. Trends Over Time: Line & Waterfall Charts

* **Line Graph**: Tracks continuous data points over time to reveal trends and seasonality.
* **Waterfall Chart**: Illustrates incremental changes, highlighting contributions to overall growth or decline.

<Frame>
  ![The image shows examples of common visualizations, including a line graph and a waterfall graph, used to observe changes over time. It highlights the concepts of diagnostic and predictive analysis.](../../../../images/kodekloud.com/kk-media/image/upload/v1752872829/notes-assets/images/DP-900-Microsoft-Azure-Data-Fundamentals-Common-Visualizations/visualizations-line-graph-waterfall-analysis.jpg)
</Frame>

***

## 4. Geographic Distribution: Map Visualizations

Map charts combine spatial data with metrics (bubble size or color intensity) to reveal regional patterns. They start as descriptive but can become diagnostic when clusters emerge.

<Frame>
  ![The image shows a map of North America with blue circles indicating the sum of shipping fees by city. It is labeled as a common chart type for geographical distribution, with options for descriptive or diagnostic analysis.](../../../../images/kodekloud.com/kk-media/image/upload/v1752872830/notes-assets/images/DP-900-Microsoft-Azure-Data-Fundamentals-Common-Visualizations/north-america-shipping-fees-map.jpg)
</Frame>

***

## 5. Proportional Analysis: Pie Charts & Tree Maps

* **Pie Chart**: Compares parts to a whole.
* **Tree Map**: Uses nested rectangles to represent hierarchical proportions, making it easier to see smaller segments.

<Callout icon="lightbulb">
  Limit pie charts to 5–7 slices for clarity. Too many segments make the chart hard to read.
</Callout>

<Frame>
  ![The image shows two types of data visualizations: a pie chart and a tree map, both representing the sum of shipping fees by ship city.](../../../../images/kodekloud.com/kk-media/image/upload/v1752872832/notes-assets/images/DP-900-Microsoft-Azure-Data-Fundamentals-Common-Visualizations/data-visualizations-pie-chart-tree-map.jpg)
</Frame>

***

## 6. Relationship Analysis: Scatter Charts

Scatter plots reveal correlations, clusters, and outliers across two measures:

1. **Predictive**: A tight cluster along a trend line enables accurate forecasting.
2. **Diagnostic**: Multiple clusters point to distinct subgroups—compare slopes to understand their behavior.
3. **Prescriptive**: Outliers highlight risks or opportunities that warrant further action.

<Callout icon="triangle-alert">
  Watch out for overplotting when you have many points—consider transparency or binning to preserve insight.
</Callout>

<Frame>
  ![The image shows three scatter charts illustrating different types of data relationships: predictive, diagnostic, and prescriptive, with trend lines and outliers.](../../../../images/kodekloud.com/kk-media/image/upload/v1752872833/notes-assets/images/DP-900-Microsoft-Azure-Data-Fundamentals-Common-Visualizations/scatter-charts-data-relationships-trend-lines.jpg)
</Frame>

***

## Links and References

* [Data Visualization Best Practices](https://www.tableau.com/learn/articles/data-visualization)
* [Understanding Chart Types](https://www.datavizcatalogue.com/)
* [Microsoft Azure Data Fundamentals](https://docs.microsoft.com/learn/certifications/exams/dp-900)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/dp-900-microsoft-azure-data-fundamentals/module/a4f1a604-4743-4a3a-81ac-8210d6f9bb96/lesson/e46c2336-4e92-46bd-b5ac-e8694c351719" />
</CardGroup>
