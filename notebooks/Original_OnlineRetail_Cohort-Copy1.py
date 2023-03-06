#!/usr/bin/env python
# coding: utf-8

# # Hands-on 01: Online retail - Cohort Analysis

# ## Concepts
#
#
# One key go-to idea to uncover customer behavior is to spliting them into smaller groups that within each group they are more similar to each other.
# That make the insights is cleared, comparing to doing analysis on the whole population.
#
# You will notice that they have done it by multiple ways in our analytics works: splitting customers by geo, app, level of values, etc.
# In this hands-on, we try 3 techniques, serving that purpose:
#
# 1. Cohort
# 2. RFM segmentation
# 3. KMeans clustering
#
# We start with **Cohort analysis**, we commonly segment customers by the date they onboard with the app/products,
# with the assumption that each snapshot of time, we acquire a group of customers (as a cohort).
# The product offerings and marketing strategies are the same, so we expect customers in the same cohort are more or less comparable.
#
# In fact, cohorts is not necessarily defined as the time of acquiring customers, but other given factors that make the group of customers more similar.
# The cohort by the starting time of customers give a view of how the product evolve over time, and how the customer base shift over time.
#
#
# ### What's cohort?
# - *A cohort*: Individuals have some common in characteristics
# 	- For example, users acquired through a same marketing campaign at the same date
# 	- First batch of students of an online course
# - Cohort analysis is a useful way to compare groups of entities over time
# 	- Provide a framework to **detect correlations between cohort characteristics and long-term trends** -> Hypotheses about the causal drivers.
# 	- Compare new cohorts of customers and compare to previous cohorts -> Alerts when something has gone wrong
#
#
# ### Components of Cohort Analysis
#
# Cohort analyses have three components
#
# 1. `Cohort grouping`: often based on the start date (customer's first purchase, subscription date, the date a student started school, etc.)
# 2. Time series of data over which a cohort is observed:
#     - A series of purchases, logins, interactions, Active Time Spent day-by-day after the start date
#     - A series should cover the the entire life span (mature)
#     - A series should be long enough to complete the action of interest -> For example, if customers tend to purchase once a month, a time series of several months is needed. If, on the other hand, purchases happen only once a year, a time series of several years would be preferable.
#     - Period is relative to the start date (for example, day0, day1, day2, etc.)
# 3. Aggregate metrics that we want to measures: Retention, Revenue along the life-cycle. Any metrics that matters to the health of the business -> Aggregate `sum`, `count`, `average`

# Go through the notebook and fill in TODO part (Google might help you along the way).
# **There are 09 in total**.

# In[1]:


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# # TODO: INGESTING
# df = pd.read_excel("../data/01_raw/online_retail.xlsx", dtype={"CustomerID": str})


# # TODO: PROCESSING
# # TODO: Convert to function, take col for remove null (parameterize)
# df2 = df[~df.CustomerID.isnull()].copy()

# # TODO: Parameterize / convert to function (DRY, winsorize)
# # Parameters
# quantity_cap = 40
# order_value_cap = 60
# order_value_flr = 0

# df2 = df[
#     (df.Quantity <= quantity_cap)
#     & (df.order_value <= order_value_cap)
#     & (df.order_value > order_value_flr)
# ]
# df2.dropna(inplace=True)

df["order_value"] = df.Quantity * df.UnitPrice


# ## Prepare the Data for Cohort Analysis
# ### Step 1. `invoice_period`
# Generate the invoice_period by extracting Year-Month of InvoiceDate. By this, we change the frequency from Daily to Monthly.
# TODO: Function to convert date to %Y-%, (DRY, Parameterize)
df2["invoice_period"] = df["InvoiceDate"].apply(lambda x: x.strftime("%Y-%m"))
df2.set_index("CustomerID", inplace=True)
df2["cohort_group"] = (
    df2.groupby(level=0)["InvoiceDate"]
    .min()
    .apply(lambda x: x.strftime("%Y-%m"))
)
df2.reset_index(inplace=True)


# TODO: AGGREGATING

# ### Step 3. Aggregate Metrics
g = df2.groupby(["cohort_group", "invoice_period"])
cohorts = g.agg(
    {
        "CustomerID": pd.Series.nunique,
        "Description": pd.Series.nunique,
        "Quantity": np.sum,
        "order_value": np.sum,
    }
)
cohorts.rename(
    columns={
        "CustomerID": "cust_cnt",
        "Description": "product_item_cnt",
        "Quantity": "total_quant",
        "order_value": "total_value",
    },
    inplace=True,
)


# ### Step 4. `cohort_period`
def cohort_period(df):
    df["cohort_period"] = np.arange(len(df)) + 1
    return df


cohorts = cohorts.groupby(level=0).apply(
    cohort_period
)  # level 0: cohort_group, apply for each row (invoice_periods)
cohorts.reset_index(inplace=True)
cohorts.set_index(["cohort_period", "cohort_group"], inplace=True)


# ## Cohort Analysis
# TODO: Convert to function, creating analysis (beside total_value)
cohorts["total_value"].unstack(0)
unstacked_value = cohorts["total_value"].unstack(0)


# TODO: REPORTING
plt.figure(figsize=(20, 5))
ax = sns.heatmap(
    unstacked_value,
    annot=True,
    cmap="YlGn",
    fmt=",.2f",
    linewidths=1,
    cbar_kws={"shrink": 0.8},
)
ax.set_ylabel("Cohort Groups")
ax.set_xlabel("Cohort Periods")
ax.set_title("Monthly Total Sales Across Cohorts")


# TODO_07: Comments and highlight any insights from the charts


# ### Retention
#
# > Retention of each cohort over time (periods) is the number of active users at each period, divide for the cohort size (= user count in first periods)
# - Size of cohort (`denomiator`)
# - Spread the `cust_cnt` - active users over periods of each cohorts
# - Divide for the **retention rate**: `cust_retention.divide(cohorts_size, axis=0)`


# TODO: AGGREGATING
# TODO: Convert to function, creating retention by different definition (beside cust_cnt)
cohorts_size = cohorts.groupby(level=1)["cust_cnt"].first()
cust_retention = cohorts["cust_cnt"].unstack(0)
cust_retention = cust_retention.divide(cohorts_size, axis=0)


# TODO: REPORTING
plt.figure(figsize=(20, 9))
cmap = sns.diverging_palette(0, 230, 90, 60, as_cmap=True)
ax = sns.heatmap(
    cust_retention,
    annot=True,
    cmap=cmap,
    fmt=".2f",
    linewidths=1,
    cbar_kws={"shrink": 0.8},
)
ax.set_ylabel("Cohort Groups")
ax.set_xlabel("Cohort Periods")
ax.set_title("Cohorts Monhtly Retention")
