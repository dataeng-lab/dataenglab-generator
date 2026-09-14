# Quiz: Spark SQL

## Question 1
- Type: Multiple choice
- Difficulty: Easy
- Related lesson: 06-running-sql-queries-on-dataframes
- Question: What must happen before `spark.sql("SELECT * FROM order_items")` will succeed?
- Options:
  A. The DataFrame must be converted to a pandas DataFrame first.
  B. order_items.csv must be re-read from disk inside the SQL string.
  C. The DataFrame must be registered with createOrReplaceTempView("order_items").
  D. Nothing — spark.sql() can query any variable name directly.
- Correct answer: C
- Explanation: spark.sql() can only query names registered as temporary views (or tables). Calling it before createOrReplaceTempView() raises a "table or view not found" error.

## Question 2
- Type: True/False
- Difficulty: Medium
- Related lesson: 06-running-sql-queries-on-dataframes
- Question: A temporary view created with createOrReplaceTempView() writes data to disk so it can be queried again the next time the script runs.
- Options:
  A. True
  B. False
- Correct answer: B
- Explanation: A temp view is an in-memory alias tied to the current SparkSession. It disappears when the program ends and never writes anything to disk.

## Question 3
- Type: Multiple choice
- Difficulty: Medium
- Related lesson: 07-joining-datasets-with-spark-sql
- Question: order_items has order_id values ["A", "B", "X"]. orders has order_id values ["A", "B", "C"]. After an inner join on order_id, which order_id appears in the result?
- Options:
  A. A, B, C, X
  B. A, B only
  C. X only
  D. A, B, C
- Correct answer: B
- Explanation: An inner join keeps only rows whose key exists on both sides. "X" has no match in orders and is dropped; "C" never appears because it has no matching order_items row to join from.

## Question 4
- Type: Multiple choice
- Difficulty: Medium
- Related lesson: 07-joining-datasets-with-spark-sql
- Question: Why would using how="left" instead of how="inner" be a mistake when the goal is to exclude order_items rows whose order_id does not exist in orders?
- Options:
  A. A left join is slower and produces no output at all.
  B. A left join keeps every row from order_items and fills missing order columns with null instead of dropping the unmatched rows.
  C. A left join is only valid in SQL, not the DataFrame API.
  D. There is no difference between "left" and "inner" for this data.
- Correct answer: B
- Explanation: how="left" preserves every row on the left side (order_items) regardless of a match, which is the opposite of the intended behavior — it would keep orphaned line items instead of excluding them.

## Question 5
- Type: Multiple choice
- Difficulty: Hard
- Related lesson: 06-running-sql-queries-on-dataframes
- Question: A dataset is stored on disk as Parquet files partitioned by `order_date` (one subdirectory per date), and a query runs `SELECT * FROM orders WHERE order_date = '2024-01-15'`. What does Spark's "partition pruning" do for this query?
- Options:
  A. It compresses the files in the matching partition to save disk space.
  B. It skips reading the subdirectories for every order_date other than '2024-01-15' entirely, instead of reading all the data and filtering it afterward.
  C. It splits the '2024-01-15' partition into smaller partitions so more executors can work on it in parallel.
  D. It merges every date's files into one file before applying the WHERE clause.
- Correct answer: B
- Explanation: When data is physically laid out in partitions on disk (for example, one directory per order_date), Spark's optimizer can push a filter on that same column down to the scan step and skip reading partitions that cannot match — rather than reading everything and discarding non-matching rows afterward. This is called "partition pruning," and it only kicks in when the filter is on the column the data is actually partitioned by on disk; it is a read-time optimization, distinct from the in-memory processing partitions covered in Lesson 1.
