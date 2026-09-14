# Curriculum: Apache Spark for Beginners: DataFrames and Spark SQL

## Course > Topic > Lessons > Quizzes

### Topic 1: Spark Architecture and Getting Started

| # | Item | Type | Duration |
|---|------|------|----------|
| 1.1 | Why Data Engineers Use Spark | Lesson | 10 min |
| 1.2 | Your First PySpark Program | Lesson | 18 min (8 lecture + 10 practical) |
| 1.3 | Quiz: Spark Architecture | Quiz (4 questions) | 5 min |

### Topic 2: DataFrames: Transformations and Actions

| # | Item | Type | Duration |
|---|------|------|----------|
| 2.1 | Transformations, Actions, and Lazy Evaluation | Lesson | 15 min (8 lecture + 7 practical) |
| 2.2 | Selecting, Filtering, and Deriving Columns | Lesson | 20 min (8 lecture + 12 practical) |
| 2.3 | Grouping and Aggregating Data | Lesson | 20 min (8 lecture + 12 practical) |
| 2.4 | Quiz: DataFrame Operations | Quiz (4 questions) | 5 min |

### Topic 3: Spark SQL

| # | Item | Type | Duration |
|---|------|------|----------|
| 3.1 | Running SQL Queries on DataFrames | Lesson | 18 min (8 lecture + 10 practical) |
| 3.2 | Joining Datasets with Spark SQL and the DataFrame API | Lesson | 22 min (10 lecture + 12 practical) |
| 3.3 | Quiz: Spark SQL | Quiz (5 questions) | 5 min |

### Topic 4: Building and Validating a Spark Pipeline

| # | Item | Type | Duration |
|---|------|------|----------|
| 4.1 | Writing Output and Structuring a Spark Job | Lesson | 18 min (8 lecture + 10 practical) |
| 4.2 | Testing a PySpark Pipeline Locally | Lesson | 22 min (10 lecture + 12 practical) |
| 4.3 | Quiz: Building and Testing Pipelines | Quiz (4 questions) | 5 min |
| 4.4 | Practical Lab: Analyze NorthWind Retail Orders | Lab | 60 min |

## Files

```text
tutor-lms/
├── course-overview.md
├── curriculum.md
├── lessons/
│   ├── 01-why-data-engineers-use-spark.md
│   ├── 02-your-first-pyspark-program.md
│   ├── 03-transformations-actions-lazy-evaluation.md
│   ├── 04-selecting-filtering-deriving-columns.md
│   ├── 05-grouping-and-aggregating-data.md
│   ├── 06-running-sql-queries-on-dataframes.md
│   ├── 07-joining-datasets-with-spark-sql.md
│   ├── 08-writing-output-and-structuring-a-job.md
│   └── 09-testing-a-pyspark-pipeline-locally.md
└── quizzes/
    ├── quiz-01-spark-architecture.md
    ├── quiz-02-dataframe-operations.md
    ├── quiz-03-spark-sql.md
    └── quiz-04-building-and-testing-pipelines.md
```

## Sequencing notes
- Topic 1 builds the mental model (driver/executor/cluster-manager architecture, why Spark exists) before any code, then gets a SparkSession running and a CSV loaded.
- Topic 2 covers the core DataFrame API — the lazy transformation/action model, then select/filter/withColumn, then groupBy/agg — each lesson's mini exercise reuses the orders/order_items shape from the final lab.
- Topic 3 introduces Spark SQL as an equivalent way to express the same logic, then joins, which the lab requires to connect order_items to orders.
- Topic 4 assembles everything into a structured, testable script and shows how to validate it with pytest in local mode — directly rehearsing what the lab grades.
- The lab (4.4) is the practical deliverable and, combined with each lesson's mini exercise, keeps the course at roughly 65% practical time, in line with the 50%+ practical-time requirement.
