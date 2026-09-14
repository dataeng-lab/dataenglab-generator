# Quiz: DataFrame Operations

## Question 1
- Type: Multiple choice
- Difficulty: Easy
- Related lesson: 03-transformations-actions-lazy-evaluation
- Question: Which of the following is an action, not a transformation?
- Options:
  A. filter()
  B. withColumn()
  C. collect()
  D. select()
- Correct answer: C
- Explanation: collect() triggers real execution of the whole plan and pulls the results to the driver. filter(), withColumn(), and select() are all lazy transformations that just build a plan.

## Question 2
- Type: True/False
- Difficulty: Medium
- Related lesson: 03-transformations-actions-lazy-evaluation
- Question: Calling `df.filter(df.quantity > 0)` immediately removes the invalid rows from the underlying data.
- Options:
  A. True
  B. False
- Correct answer: B
- Explanation: filter() is a transformation. It returns a new DataFrame describing the step, but no data is read or filtered until an action like show(), count(), or collect() is called.

## Question 3
- Type: Multiple choice
- Difficulty: Medium
- Related lesson: 04-selecting-filtering-deriving-columns
- Question: Which expression correctly filters rows where quantity is greater than 0 AND unit_price is greater than 0?
- Options:
  A. df.filter(df.quantity > 0 and df.unit_price > 0)
  B. df.filter((df.quantity > 0) & (df.unit_price > 0))
  C. df.filter(df.quantity > 0 & df.unit_price > 0)
  D. df.filter(df.quantity > 0 | df.unit_price > 0)
- Correct answer: B
- Explanation: Python's `and`/`or` do not work element-wise on Spark columns; use `&`/`|` with each condition wrapped in parentheses due to operator precedence.

## Question 4
- Type: Multiple choice
- Difficulty: Medium
- Related lesson: 05-grouping-and-aggregating-data
- Question: After `df.groupBy("category").agg(F.sum("line_total").alias("total_revenue"))`, what happens if `.alias("total_revenue")` is omitted?
- Options:
  A. The code raises a syntax error.
  B. The result column is still named "total_revenue" by default.
  C. The result column is named something like "sum(line_total)" instead.
  D. The aggregation silently returns zero rows.
- Correct answer: C
- Explanation: Without an explicit alias, Spark names the aggregated column after the expression itself, such as "sum(line_total)", which is awkward to reference or write out as a CSV header.

## Question 5
- Type: Multiple choice
- Difficulty: Medium
- Related lesson: 04-selecting-filtering-deriving-columns
- Question: order_items is stored on disk as a dataset partitioned by order_date (one folder per date, e.g. order_date=2024-01-15/). What does "partition pruning" do when you run df.filter(df.order_date == "2024-01-15")?
- Options:
  A. It converts the DataFrame to a pandas DataFrame before filtering.
  B. It lets Spark skip reading the files in partitions that cannot match the predicate, instead of reading every partition and filtering in memory afterward.
  C. It permanently deletes the non-matching partitions from disk.
  D. It has no effect unless .coalesce(1) is called first.
- Correct answer: B
- Explanation: When a dataset is physically partitioned by a column, Spark's planner can use a filter on that column to skip scanning entire partition directories that cannot contain matching rows, avoiding unnecessary disk I/O. It doesn't move data to pandas, delete anything from disk, or depend on coalesce().
