---
title: "PCA, DWT, and XGBoost: A Machine Learning Trading Strategy"
date: 2024-09-03
slug: en/posts/algo/结合主成分分析、离散小波和XGBoost的交易策略
tags: [Factor Investing, Machine Learning, Quantitative Trading]
excerpt: "This paper by Nobre and Neves (2019) combines PCA, DWT, and XGBoost to generate trading signals. The strategy outperforms Buy-and-Hold and benchmarks across multiple financial markets."
lang: en
translation_of: posts/algo/结合主成分分析、离散小波和XGBoost的交易策略
auto_translated: true
source_sha: 737f0142ef071a71f4cef5a0912fa7bbdc9171d5
---

> This is a [paper by Nobre and Neves](https://www.sciencedirect.com/science/article/abs/pii/S0957417419300995?via%3Dihub) published in 2019. It generates a machine learning trading strategy that achieves better returns than a Buy-and-Hold strategy and another benchmark. The main body of this article consists of the original paper’s abstract. In the QuanTide commentary at the end, I provide some critical remarks.

The article introduces an expert system applied to finance, integrating Principal Component Analysis (PCA), Discrete Wavelet Transform (DWT), Extreme Gradient Boosting (XGBoost), and Multi-Objective Optimization Genetic Algorithms (MOO-GA). The system aims to provide optimal buy/sell signals for investors, seeking higher investment returns at lower risk levels.

PCA is used to reduce the dimensionality of the financial input dataset, while DWT denoises each feature. The processed dataset is then fed into an XGBoost binary classifier, whose hyperparameters are optimized by MOO-GA.

The results show that PCA significantly enhances system performance. Applying PCA and DWT jointly allows the system to outperform traditional Buy-and-Hold strategies in three of five financial markets, achieving an average portfolio return of 49.26%, compared to 32.41% for the Buy-and-Hold strategy.

## Related Work

### Principal Component Analysis

In related work, Principal Component Analysis (PCA) is used to reduce the dimensionality of high-dimensional datasets while retaining key features. PCA forms a new set of principal components through linear combinations of the original dataset, maximizing the retention of original data information and exhibiting high variance. By removing dimensions with minimal variation, PCA simplifies the dataset and improves computational efficiency.

### Discrete Wavelet Transform

Discrete Wavelet Transform (DWT) is a powerful tool for handling the time-varying characteristics of time-series data in real-world problems. Unlike traditional Fourier transforms, it is particularly suitable for non-stationary signals, such as stock market prices.

Traditional Fourier transforms assume signals are periodic and defined over the entire time interval, whereas wavelet transforms allow signals to be represented as superpositions of time-localized basis functions. This enables wavelet transforms to capture both time and frequency information simultaneously.

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/09/dwt.jpg)

The foundation of wavelet transform is representing any function as a superposition of wavelets that form the wavelet transform basis. These wavelets are scaled and translated copies of finite-length oscillating waveforms (called mother wavelets), i.e., sub-wavelets. Selecting the optimal wavelet basis depends on the characteristics of the original signal to be analyzed and the intended purpose of the analysis. The final result is a set of time-frequency representations with different resolutions, which is why wavelet transform is called multi-resolution analysis.

In the method proposed in this paper, only Discrete Wavelet Transform (DWT) is used. DWT decomposes signals into a set of orthogonal wavelets. Compared to continuous wavelet transform, it is more suitable for practical applications because it allows for easier discrete processing on digital computers.

The application of wavelet transform in preprocessing financial time-series data is primarily for denoising, thereby helping to improve the prediction accuracy of subsequent models.

### Genetic Algorithms

Genetic Algorithms (GA) are meta-heuristic optimization methods inspired by the biological evolution process in nature, used to solve optimization problems in complex spaces. They find approximate optimal solutions by simulating natural selection and genetic mechanisms.

A genetic algorithm starts with an initial population of randomly generated individuals, representing candidate solutions to the problem. Each individual, or chromosome, contains a series of parameters or variables called genes.

In each generation, individuals are selected for reproduction based on their fitness (i.e., their performance score in a given optimization task). Individuals with higher fitness are more likely to be selected and produce new offspring through crossover operations, which exchange gene segments between pairs.

Additionally, random mutation operations are performed on some offspring to introduce new genetic information.

These operations are repeated over multiple generations until predetermined stopping criteria are met, such as reaching the maximum number of iterations or the population converging to a stable state. The ultimate goal is to obtain sufficiently good solutions after a series of evolutionary processes.

### XGBoost

XGBoost (Extreme Gradient Boosting) is an optimized distributed gradient boosting library designed for efficiency, flexibility, and portability. It improves upon traditional gradient boosting decision trees by adding performance-enhancing features. Specifically, XGBoost introduces regularization terms to simplify the model, helping to reduce the likelihood of overfitting, and supports parallel processing, significantly accelerating training speed.

An important feature of XGBoost is that it allows users to define custom loss functions and automatically handles missing data. It improves computational efficiency by constructing multiple trees in parallel, unlike traditional gradient boosting models that typically build trees serially. Furthermore, XGBoost allows customization of objective functions and evaluation metrics, making it suitable for various machine learning tasks, including predicting stock price directions in financial markets.

Research indicates that when applied to predicting stock market price directions, XGBoost as a classifier outperforms non-ensemble methods such as Support Vector Machines (SVM) and Artificial Neural Networks (ANN). Particularly in 60-day and 90-day prediction horizons, XGBoost demonstrates better long-term prediction accuracy.

## Proposed Solution

### System Architecture

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/09/architecture-of-xgboost.jpg)

### Objective Equation

In this paper, the goal is to predict whether the closing price on day $t+1$, denoted as `Close_{t+1}`, will have a positive or negative change relative to the closing price on day $t$, denoted as `Close_t`. Therefore, a supervised learning solution, specifically a binary classifier, is proposed. The target variable `y` to be predicted is the signal of the closing price change from day $t$ to $t+1$, following a binomial probability distribution `y ∈ {0, 1}`, where:
- If the closing price change is positive, `y` takes the value `1`;
- If the closing price change is negative, `y` takes the value `0`.

This objective can be defined mathematically as follows:

\[
y_t = 
\begin{cases} 
1 & \text{if } Close_{t+1} - Close_t \geq 0 \\
0 & \text{if } Close_{t+1} - Close_t < 0 
\end{cases}
\]

Where:
- `Close_{t+1}` is the closing price on day $t+1$.
- `Close_t` is the closing price on day $t$.

The array of all target variables is named `Y`. The financial input dataset `X` is the dataset output by the data preprocessing module, where PCA and DWT techniques are applied to the normalized dataset, which contains original financial data and technical indicators.

### Technical Analysis Module

The technical analysis module receives output from the Financial Data Module and applies multiple technical indicators to it. The main purpose of using technical indicators is that each provides basic information about past original data in different ways. Therefore, combining different technical indicators helps detect patterns in financial data, thereby improving the performance prediction system for financial data.

This module creates a dataset that will serve as input for the data preprocessing module. The dataset consists of combinations of 26 technical indicator sets and 5 original financial data features, producing a dataset with 31 features as shown in the table below. Technical indicator calculations are performed using the Python library TA-Lib.

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/09/ta-moduel-output.jpg)

### Data Preprocessing Module

#### Data Standardization

Omitted.

#### Principal Component Analysis

The PCA module receives a normalized input dataset containing 26 technical indicators and 5 original financial data features, totaling 31 normalized features. To reduce the risk of overfitting and lower the system's computational cost, the PCA module transforms the dataset with 31 features into a lower-dimensional dataset while retaining most of the original dataset's variance.

The PCA first fits its model to the normalized training set to determine components representing the directions of maximum variance. Then, principal components are sorted by the amount of variance they explain, and only those summing to at least 95% of the original training set variance are retained. Finally, the data is projected onto the principal components, resulting in a lower-dimensional dataset because it retains only data samples that better explain the relationships between features. The reduced dataset is then fed into the wavelet module.

The PCA module uses the Scikit-learn Python library.

#### Wavelet Transform

Although the dataset has been simplified in the PCA module, reducing dimensionality and retaining only data that better explains relationships between features, some irrelevant data samples may still produce negative impacts on system training and prediction performance.

PCA technology removes irrelevant data points from feature subsets, while DWT technology performs denoising in the time domain for each feature in the PCA-reduced dataset. This process reduces the impact of noise in the dataset while preserving the important components of each feature as much as possible.

The wavelet bases tested for each financial market in this system include: Haar wavelet, Daubechies wavelet, and Symlet wavelet. For Daubechies and Symlet wavelets, tested orders are 3, 6, 9, 15, and 20.

Although higher decomposition levels can eliminate more noise, thereby better representing the trend of each feature, this may also eliminate fluctuations containing market characteristics. Therefore, in this system, decomposition levels of 2, 5, and 7 are tested to find the optimal denoising decomposition level for each financial market.

DWT first specifies the wavelet base, order, and decomposition level used. Then, for each feature in the training set, DWT performs multi-level decomposition, which produces one approximation coefficient and $j$ detail coefficients, where $j$ is the selected decomposition level.

To calculate the approximation and detail coefficients for the validation and test sets, one data point is added to the training set at a time, the coefficients of the new signal are calculated, and the coefficients corresponding to the added data point are saved to avoid considering future information. This process is executed until all points in the validation and test sets have their respective coefficients calculated. Then, the obtained detail coefficients are thresholded and the signal is reconstructed, producing a denoised version of each original dataset feature. After applying DWT, the dataset is fed into the XGBoost module.

The PyWavelets and scikit-image libraries are used to develop the DWT module in this system.

### XGBoost Module

The XGBoost binary classifier is responsible for the system's classification process.

#### Binary Classifier

The output $\hat{y}$ of the classifier is the predicted value given the current observation $x$, corresponding to the actual date $t$. The variable $\hat{y}$ ranges in $[0,1]$, and the set of all $\hat{y}$ corresponds to the predicted trading signal, indicating whether the system should hold a long or short position in the next trading day.

Before the XGBoost binary classifier algorithm begins, a set of parameters must be selected. Parameters defining the machine learning system architecture are called hyperparameters. Since each time series has its own characteristics, there is a different set of optimal hyperparameters for each time series analyzed, even if the model has good generalization capabilities, i.e., hyperparameters that achieve good results on out-of-sample data. Therefore, to obtain the best results in each analyzed financial market, the optimal set of hyperparameters must be found. For this, the MOO-GA method is used, as described in the next section.

The preprocessed data output by the data preprocessing module is fed into the XGBoost binary classifier, along with the target variable array $Y$ to be predicted, and both are split into training, validation, and test sets. After defining the dataset and XGBoost hyperparameters, the training phase begins. The system's generalization capability is measured by its performance on unseen data. Therefore, after the training phase ends, an out-of-sample validation set is used to test the model obtained during training to verify the generalization capability of the obtained model.

This validation set is used in the MOO process to help select the best-performing solution using unseen data. After the training and validation phases end, the final model is created, i.e., the model trained with the best hyperparameter set found by MOO-GA, and the generated output is compared with the test set to verify the quality of predictions. As mentioned earlier, the output takes the form of probabilities that a data point belongs to class 0 or 1.

The XGBoost library is used to develop the XGBoost binary classifier in this system.

#### Multi-Objective Optimization Genetic Algorithm

When building machine learning models, there are many design choices for the model architecture. Most of the time, users do not know in advance what the architecture of a given model should look like, so exploring a range of possibilities is desirable.

This is the case with the hyperparameters of the XGBoost binary classifier, which define the classifier's architecture. This process of finding the ideal model architecture is called hyperparameter optimization.

A multi-objective optimization method is adopted instead of a single-objective optimization method because our ultimate goal is to achieve a trading system with high returns and low risk. Therefore, it is natural to use statistical metrics to evaluate the system's performance relative to the predictions made—in this case, Accuracy; but on the other hand, metrics are also needed to evaluate the system's ability to achieve good returns while minimizing losses—in this case, the Sharpe Ratio.

Therefore, candidate solutions are evaluated based on two selected objective functions: Accuracy and Sharpe Ratio. The set of each solution represents the fitness function to be optimized by MOO-GA, with the goal of maximizing each objective function. Thus, given the XGBoost binary classifier, financial dataset $X$, and target variable array $Y$, MOO-GA searches for and optimizes the XGBoost binary classifier hyperparameter set, aiming to maximize the accuracy and Sharpe ratio of the obtained predictions.

To find the best hyperparameter set aimed at maximizing the two previously mentioned objective functions, the MOO-GA method is based on the Non-dominated Sorting Genetic Algorithm-II (NSGA-II).

Due to the numerous hyperparameters in the XGBoost binary classifier, only those having a significant impact on the classifier's architecture and thus its overall performance are optimized. The hyperparameters selected for optimization also have a significant impact on the bias-variance trade-off: learning rate, maximum tree depth, minimum child weight, and subsample. Each of these hyperparameters constitutes a gene in the chromosome of MOO-GA.

In the proposed MOO-GA, a two-point crossover operator is used, where two points are selected on the parent strings, and everything between the two selected points is exchanged between parents. The selected mutation rate is 0.2, meaning that each new candidate solution generated by the crossover operator has a 20% probability of undergoing mutation.

We also use hypermutation, a method to reintroduce diversity into the population in evolutionary algorithms. In this system, the mutation rate is adjusted during evolution to help the algorithm escape local optima.

The following figure shows the important hyperparameters:

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/09/most-important-hyper-params.jpg)

The DEAP Python library is used to develop the MOO-GA module in this system.

### Trading Module

The trading module is responsible for simulating real financial market trading. Its main functions include:

*   **Receiving Inputs:** Obtaining trading signals and financial data from the XGBoost module.
*   **Simulating Market Orders:** Simulating market orders in the financial market based on the input trading signals.
*   **State Machine Design:** Employing a state machine with long, short, and hold states to execute trades. Specifically, given a trading signal, the state machine executes corresponding actions based on the market orders in the signal. The prediction result $\hat{y}$ of the XGBoost binary classifier represents the predicted probability of class $p(\hat{y})$. Since the two selected classes represent the change in closing price on day $t+1$ relative to day $t$, these predictions can be used to construct trading signals.

The method for constructing trading signals is as follows:

*   If $p(\hat{y}) \geq 0.5$, and the selected class is 1, it means the stock's closing price (close) on day $t+1$ is expected to show a positive change, representing a buying opportunity on day $t$, i.e., a long position is taken. This action is represented by position 1 in the corresponding date in the training signal;
*   Conversely, if $p(\hat{y}) < 0.5$, and the selected class is 0, it means the stock's closing price (close) on day $t+1$ is expected to show a negative change, representing a selling opportunity on day $t$, i.e., a short position is taken. This action is represented by position 0 in the corresponding date in the training signal.

Therefore, the value of the trading signal ranges in $[0,1]$, and the trading module is responsible for interpreting these values and converting them into trading actions.

## Experimental Results

The following figure shows the schematic of the training process.

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/09/xgboost-training-process.jpg)

### Case 1: Effect of Using PCA

In the first case study, the impact of PCA technology on the performance of the implemented system is analyzed.

The benchmark system is divided into two configurations:

*   **Basic System:** The input dataset contains 31 normalized financial features.
*   **Improved System:** The input dataset is processed with PCA (Principal Component Analysis).

In the improved system, PCA technology is applied to reduce the dimensionality of the dataset. Specifically, after applying PCA to the standardized dataset containing 31 financial features, 6 principal components are retained for each financial market. This means the original 31 financial features are reduced to 6 low-dimensional features.

The following figure lists the experimental results for each system as well as the results for the Buy-and-Hold strategy. The best results obtained for each financial market are highlighted in bold.

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/09/influence-with-cpa.png)
