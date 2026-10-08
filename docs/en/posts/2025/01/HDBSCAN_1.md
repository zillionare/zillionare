---
title: "Validating HDBSCAN for Stock Selection via Cointegration"
date: 2025-01-11
slug: en/posts/algo/HDBSCAN_1
tags: []
excerpt: "This article validates HDBSCAN clustering for stock selection by constructing stationary pairs through cointegration tests. It demonstrates how mean-reversion signals derived from these clusters can generate profitable trading strategies. ===TAG=== HDBSCAN, Cointegration, Mean Reversion, Clustering ===BODY=== ![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/01/20250112164819.png)  The previous article discussed using the HDBSCAN algorithm to cluster assets. After clustering, we perform cointegration tests on the results. By calculating hedge ratios, we can construct stationary time series. We know that a stationary time series has constant mean and variance with autocorrelation properties; thus, once it deviates from the mean, it will eventually revert to it. We can leverage this characteristic to generate trading signals.  But how do we prove that the HDBSCAN algorithm is effective for finding cointegrated pairs and the associated trading strategy? Let’s analyze this step by step.  First, as established in previous articles, HDBSCAN is a density-based clustering algorithm that determines cluster assignments by calculating the density of each sample. Its advantages include automatically determining the number of clusters and handling high-dimensional data. Below is the key Python code to implement HDBSCAN. The historical data covers the period from January 1, 2022, to December 31, 2023.  ```python start_date = datetime.date(2022, 1, 1) end_date = datetime.date(2023,12,31) barss = load_bars(start_date, end_date, 2000)   # Fetch historical asset data; selecting 2000 data points here closes = barss[\"close\"].unstack().ffill().dropna(axis=1, how='any') # Handle missing values: convert MultiIndex of 'close' to a 2D DataFrame and fill forward using ffill() clusterer = hdbscan.HDBSCAN(min_cluster_size=3, min_samples=2) # Perform clustering using HDBSCAN; install the 'hdbscan' package directly via Python cluster_labels = clusterer.fit_predict(closes.T)  # Transpose because we are clustering assets (features)  clustered = closes.T.copy() clustered['cluster'] = cluster_labels # Add clustering results to the DataFrame  clustered = clustered[clustered['cluster'] != -1] # Remove points labeled -1, which are noise rather than valid clusters clustered_close = clustered.drop(\"cluster\", axis=1)  unique_clusters = set(cluster_labels) num_clusters = len(unique_clusters) # Get the number of valid clusters print(f\"Number of valid clusters: {num_clusters}\")    tsne = TSNE(n_components=3, random_state=42) tsne_results = tsne.fit_transform(clustered_close)  # Use t-SNE for dimensionality reduction to facilitate cluster visualization reduced_tsne = pd.DataFrame(data=tsne_results, columns=['tsne_1', 'tsne_2', 'tsne_3'], index=clustered_close.index) # Add t-SNE results to the DataFrame reduced_tsne['cluster'] = clustered['cluster']  fig_tsne = px.scatter_3d(     reduced_tsne,      x='tsne_1', y='tsne_2', z='tsne_3',     color='cluster',      title='t-SNE Clustering of Stock Returns',     labels={'tsne_1': 't-SNE Component 1', 'tsne_2': 't-SNE Component 2'} )  # Visualize using a 3D scatter plot fig_tsne.layout.width = 1200 fig_tsne.layout.height = 1100 fig_tsne.show() ```  After importing the necessary libraries and running the code, we obtain the following 3D plot: ![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/01/20250112155220.png)  The 3D plot displays the spatial distribution of stocks in three dimensions, with different colors representing different cluster categories. From the plot, we can observe that the 2,000 stocks during this period were divided into over 40 clusters. Except for Cluster 39, which contains 420 stocks, all other clusters contain fewer than 20 stocks.  Let’s analyze Cluster 35, which contains three stocks. Around October 1, 2022, these three stocks exhibited a continuous upward trend. ![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/01/20250112155727.png)  Can we continue using the HDBSCAN algorithm to cluster data from before October 2022 to see if these three stocks are grouped together again? Using the same code but changing the time range to January 1, 2022, to October 1, 2022, we obtain the following 3D plot: ![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/01/20250112161023.png)  Compared to the previous 3D plot, the stocks (features) grouped into a single category are more similar, resulting in denser clustering. Will the three stocks from Cluster 35 in the previous analysis still be grouped together? We can visualize each cluster (using the same method as in the previous article) to observe which cluster these three stocks fall into during this new classification. Upon observation, we find that these three stocks are indeed grouped together, but this cluster contains approximately 600 stocks. Let’s look at the visualization results for these 600+ stocks: ![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/01/20250112162525.png)  We want to understand what characteristics these three stocks exhibited before their continuous rise. Although the data for this large cluster is substantial, observing the trend charts reveals that their price movements are roughly identical, which is why they are grouped together.  Let’s further cluster these 600+ stocks using HDBSCAN. Will the previous three stocks be grouped together? In other words, we need to verify that the general trends of these three stocks were consistent before their continuous rise. Interested readers can try this themselves. Below are the conclusions from my verification:  When re-clustering these 600 stocks from January 2022 to October 2022, they were divided into three clusters. Two of the original three stocks were grouped into one cluster, while the third was in another. I believe this result sufficiently demonstrates that the trends of these 600 stocks between January 2022 and October 2022 were similar, leading to them being grouped into only three clusters. ![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/01/20250112173612.png)  Therefore, the HDBSCAN algorithm is effective for stock selection. It identifies groups of stocks with similar trends, allowing us to use the stationary series construction method described in the previous article to generate trading signals."
lang: en
translation_of: posts/algo/HDBSCAN_1
auto_translated: true
source_sha: 2718043913db6c00585e7fb56442364f9cce7cf4
cover: "https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/01/quantfan-by-ai.jpg"
---

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/01/20250112164819.png)

The previous article discussed using the HDBSCAN algorithm to cluster assets. After clustering, we perform cointegration tests on the results. By calculating hedge ratios, we can construct stationary time series. We know that a stationary time series has constant mean and variance with autocorrelation properties; thus, once it deviates from the mean, it will eventually revert to it. We can leverage this characteristic to generate trading signals.

But how do we prove that the HDBSCAN algorithm is effective for finding cointegrated pairs and the associated trading strategy? Let’s analyze this step by step.

First, as established in previous articles, HDBSCAN is a density-based clustering algorithm that determines cluster assignments by calculating the density of each sample. Its advantages include automatically determining the number of clusters and handling high-dimensional data. Below is the key Python code to implement HDBSCAN. The historical data covers the period from January 1, 2022, to December 31, 2023.

```python
start_date = datetime.date(2022, 1, 1)
end_date = datetime.date(2023,12,31)
barss = load_bars(start_date, end_date, 2000)   # Fetch historical asset data; selecting 2000 data points here
closes = barss["close"].unstack().ffill().dropna(axis=1, how='any') # Handle missing values: convert MultiIndex of 'close' to a 2D DataFrame and fill forward using ffill()
clusterer = hdbscan.HDBSCAN(min_cluster_size=3, min_samples=2) # Perform clustering using HDBSCAN; install the 'hdbscan' package directly via Python
cluster_labels = clusterer.fit_predict(closes.T)  # Transpose because we are clustering assets (features)

clustered = closes.T.copy()
clustered['cluster'] = cluster_labels # Add clustering results to the DataFrame

clustered = clustered[clustered['cluster'] != -1] # Remove points labeled -1, which are noise rather than valid clusters
clustered_close = clustered.drop("cluster", axis=1)

unique_clusters = set(cluster_labels)
num_clusters = len(unique_clusters) # Get the number of valid clusters
print(f"Number of valid clusters: {num_clusters}")  

tsne = TSNE(n_components=3, random_state=42)
tsne_results = tsne.fit_transform(clustered_close)  # Use t-SNE for dimensionality reduction to facilitate cluster visualization
reduced_tsne = pd.DataFrame(data=tsne_results, columns=['tsne_1', 'tsne_2', 'tsne_3'], index=clustered_close.index) # Add t-SNE results to the DataFrame
reduced_tsne['cluster'] = clustered['cluster']

fig_tsne = px.scatter_3d(
    reduced_tsne, 
    x='tsne_1', y='tsne_2', z='tsne_3',
    color='cluster', 
    title='t-SNE Clustering of Stock Returns',
    labels={'tsne_1': 't-SNE Component 1', 'tsne_2': 't-SNE Component 2'}
)  # Visualize using a 3D scatter plot
fig_tsne.layout.width = 1200
fig_tsne.layout.height = 1100
fig_tsne.show()
```

After importing the necessary libraries and running the code, we obtain the following 3D plot:
![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/01/20250112155220.png)

The 3D plot displays the spatial distribution of stocks in three dimensions, with different colors representing different cluster categories. From the plot, we can observe that the 2,000 stocks during this period were divided into over 40 clusters. Except for Cluster 39, which contains 420 stocks, all other clusters contain fewer than 20 stocks.

Let’s analyze Cluster 35, which contains three stocks. Around October 1, 2022, these three stocks exhibited a continuous upward trend.
![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/01/20250112155727.png)

Can we continue using the HDBSCAN algorithm to cluster data from before October 2022 to see if these three stocks are grouped together again? Using the same code but changing the time range to January 1, 2022, to October 1, 2022, we obtain the following 3D plot:
![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/01/20250112161023.png)

Compared to the previous 3D plot, the stocks (features) grouped into a single category are more similar, resulting in denser clustering. Will the three stocks from Cluster 35 in the previous analysis still be grouped together? We can visualize each cluster (using the same method as in the previous article) to observe which cluster these three stocks fall into during this new classification. Upon observation, we find that these three stocks are indeed grouped together, but this cluster contains approximately 600 stocks. Let’s look at the visualization results for these 600+ stocks:
![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/01/20250112162525.png)

We want to understand what characteristics these three stocks exhibited before their continuous rise. Although the data for this large cluster is substantial, observing the trend charts reveals that their price movements are roughly identical, which is why they are grouped together.

Let’s further cluster these 600+ stocks using HDBSCAN. Will the previous three stocks be grouped together? In other words, we need to verify that the general trends of these three stocks were consistent before their continuous rise. Interested readers can try this themselves. Below are the conclusions from my verification:

When re-clustering these 600 stocks from January 2022 to October 2022, they were divided into three clusters. Two of the original three stocks were grouped into one cluster, while the third was in another. I believe this result sufficiently demonstrates that the trends of these 600 stocks between January 2022 and October 2022 were similar, leading to them being grouped into only three clusters.
![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/01/20250112173612.png)

Therefore, the HDBSCAN algorithm is effective for stock selection. It identifies groups of stocks with similar trends, allowing us to use the stationary series construction method described in the previous article to generate trading signals.
