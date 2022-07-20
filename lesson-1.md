|                      |
|--------------------- |
| [<<Back](./readme.md) |

These notes are taken during the class. Using a single Python session for all Python code blocks, simulating a Jupyter Notebook. All the actual activities are done outside emacs in .ipynb files. I normally use `pathlib` instead of `os` but results are the same.


# Working with Data in Python

```python
import pandas as pd
from pathlib import Path

resources = Path.cwd() / "resources"
print(resources)
```

    /Users/albertovaldez/tec-data/04-dataframes/resources


## Creating a Pandas Series

A series is a list with an explicit index, it preserves the index of its values regardless if they are sorted or not.

```python
series = pd.Series(["UCLA", "UC Berkeley", "UC Irvine"])
print(series)
```

    0           UCLA
    1    UC Berkeley
    2      UC Irvine
    dtype: object


# Creating a Pandas DataFrame

Can be created from lists of dictionaries or dictionaries of lists.


## With a List of Dictionaries

As a list of dictionaries, the key of the dictionaries will be the titles of the columns and each row is each dictionary in the list.

```python
movies_dict = [{"Title": "The Godfather", "Year Released": 1972},
               {"Title": "Pulp Fiction", "Year Released":1994}]
print(pd.DataFrame(movies_dict))
```

               Title  Year Released
    0  The Godfather           1972
    1   Pulp Fiction           1994

If you have a key that is not present in the other dictionaries, Pandas will fill the missing data wiht `NaN` types (missing values).

```python
movies_dict.append({"Title": "Minions", "Was it Good?": False})
print(pd.DataFrame(movies_dict))
```

               Title  Year Released Was it Good?
    0  The Godfather         1972.0          NaN
    1   Pulp Fiction         1994.0          NaN
    2        Minions            NaN        False

You can have whatever type of data in the cell of the DataFrame, even dictionaries or more nested structures.


## With a Dictionary of Lists

Each key will represent a column and the lists represent the cells under the column. If we have many columns, the lists must have the same length, because Pandas can&rsquo;t know which value is missing.

```python
movies_dict = {
    "Title": ["The Godfather", "Pulp Fiction", "Minions"],
    "Year Released": [1972, 1994, None],
}
print(pd.DataFrame(movies_dict))
```

               Title  Year Released
    0  The Godfather         1972.0
    1   Pulp Fiction         1994.0
    2        Minions            NaN


# Inspecting Data

`head()` will show the DataFrame headers. `describe()` will print out a summary statistic of the table.

```python
df = pd.DataFrame(movies_dict)
print("Getting the heading:\n")
print(df.head(1))
print("Getting describe:\n")
print(df.describe())
print("Getting one series or df:\n")
print(df["Title"].head())
```

    Getting the heading:
    
               Title  Year Released
    0  The Godfather         1972.0
    Getting describe:
    
           Year Released
    count       2.000000
    mean     1983.000000
    std        15.556349
    min      1972.000000
    25%      1977.500000
    50%      1983.000000
    75%      1988.500000
    max      1994.000000
    Getting one series or df:
    
    0    The Godfather
    1     Pulp Fiction
    2          Minions
    Name: Title, dtype: object


## Operations in Series

Series supports arithmetic operations and they are applied to the whole series.

```python
series = df["Year Released"] + 10
print(series)
```

    0    1982.0
    1    2004.0
    2       NaN
    Name: Year Released, dtype: float64


## Adding Series to DataFrame

```python
df["Year Released plus 10"] = series
print(df)
```

               Title  Year Released  Year Released plus 10
    0  The Godfather         1972.0                 1982.0
    1   Pulp Fiction         1994.0                 2004.0
    2        Minions            NaN                    NaN


# Activity Training Grounds

The following html is the result of the Jupyter Notebook activity.

<embed type="text/html" src="./resources/4-1-Student-Resources/03-Stu_TrainingGrounds-DataFunctions/solved_TrainingGrounds_unsolved.html" width="100%" height="500">

---


# Reading from a CSV file

Pandas takes for granted a few things:

1.  Assumes that the first row is the heading.
2.  Assumes that each line in your file is a row in the dataframe.

```python
csv_df = pd.read_csv(resources / "schools_complete.csv")
print(csv_df.head())
```

       School ID            school_name      type  size   budget
    0          0      Huang High School  District  2917  1910635
    1          1   Figueroa High School  District  2949  1884411
    2          2    Shelton High School   Charter  1761  1056600
    3          3  Hernandez High School  District  4635  3022020
    4          4    Griffin High School   Charter  1468   917500

Getting the columns.

```python
csv_df.columns
#https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rename.html
renamed_df = csv_df.rename(columns={"school_name": "School Name"})
view = renamed_df[["School Name", "School ID"]]
print(view.head())
```

                 School Name  School ID
    0      Huang High School          0
    1   Figueroa High School          1
    2    Shelton High School          2
    3  Hernandez High School          3
    4    Griffin High School          4

Whenever we access a DataFrame by slicing, we get a view of that DataFrame, so in order to work with a new version of that view as a DataFrame, we need to copy it.

```python
new_df = renamed_df[["School Name"]].copy()
print(new_df.head())
```

                 School Name
    0      Huang High School
    1   Figueroa High School
    2    Shelton High School
    3  Hernandez High School
    4    Griffin High School


# Activity Good Reads

The following is the result of the Good Reads Jupyter Notebook.

<embed type="text/html" src="./resources/4-1-Student-Resources/05-Stu_GoodReadsCSV/Solved_GoodReads_unsolved.html" width="100%" height="500">

---


# Merging DataFrames

When merging data frames, the type of join determines what data to keep.

1.  Left Outer Join. Keeps all rows from table A, even in they don&rsquo;t exists in B.
    
    |      |    |
    |----- |--- |
    | **A** | B |
2.  Inner Join. This is the default DataFrame means of combining data. We only keep ids that are in both.
    
    |      |      |
    |----- |----- |
    | **A** | **B** |
3.  Right Outer Join. Keep all rows from table B.
    
    |    |      |
    |--- |----- |
    | A | **B** |

Pandas Defaults to inner join, which will use only columns that exist in both DataFrames.

Outer join will use columns from both DataFrames and fill in the missing values with `NaN`.


# Activity Merging DataFrames

The following is the result of the Merging DataFrames Activity.

<embed type="text/html" src="./resources/4-1-Student-Resources/06-Ins_MergingDataFrames/Solved_Merging_unsolved.html" width="100%" height="500">

---


# Formatting Syntax

We can use the map function to apply an operation to each element of a Series and converts them into strings.

```python
file_df = pd.DataFrame({"avg_cost": [0,1,2,3]})
file_df["avg_cost"] = file_df["avg_cost"].map("${:.2f}".format)
print(file_df)
```

      avg_cost
    0    $0.00
    1    $1.00
    2    $2.00
    3    $3.00

We can&rsquo;t apply a format to an existing string, it has to be a number type.


# Activity Formatting Numbers

The following is the result of the Format Mapping activity.

<embed type="text/html" src="./resources/4-1-Student-Resources/08-Evr_FormatMapping/Solved_Format_Mapping_unsolved.html" width="100%" height="500">

---


# Storing DataFrames

```python
file_df.to_csv(resources / "result.csv")
file_df.to_excel(resources / "result.xlsx")

for file_name in resources.glob("*.[.csv .xlsx]*"):
    print(file_name)
```

    /Users/albertovaldez/tec-data/04-dataframes/resources/students_complete.csv
    /Users/albertovaldez/tec-data/04-dataframes/resources/result.csv
    /Users/albertovaldez/tec-data/04-dataframes/resources/schools_complete.csv
    /Users/albertovaldez/tec-data/04-dataframes/resources/result.xlsx


# Pandas documentation

The Pandas documentation is a great resource to learn how to use the library properly <sup><a id="fnr.1" class="footref" href="#fn.1" role="doc-backlink">1</a></sup>.


# Office Hours

It is good idea to invest time in Readme files and repository organization!

## Footnotes

<sup><a id="fn.1" class="footnum" href="#fnr.1">1</a></sup> <https://pandas.pydata.org/docs/>
