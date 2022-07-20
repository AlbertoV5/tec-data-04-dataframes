|                                                |                          |                          |                                      |
|----------------------------------------------- |------------------------- |------------------------- |------------------------------------- |
| [<<<Home](https://albertov5.github.io/tec-data) | [Lesson-1](./lesson-1.md) | [Lesson-2](./lesson-2.md) | [Challenge>>>](./challenge/readme.md) |


# Overview

Pandas is an open-source library that provides high performance data analysis tools for Python. It&rsquo;s one of the most widely preferred tools for data analysis. It is commonly used alongside Jupyter Notebooks to display datasets and manipulate data easily.


## Series

A one-dimensional, labeled array capable of holding any data type. The data is linear and has an index that acts as a key in a dictionary. For example an Excel file with a single column is an example of a Series, as it has the content of the cell and the cell index.

```python
import pandas as pd

high_schools = ["Huang High School",  "Figueroa High School", "Shelton High School", "Hernandez High School","Griffin High School","Wilson High School", "Cabrera High School", "Bailey High School", "Holden High School", "Pena High School", "Wright High School","Rodriguez High School", "Johnson High School", "Ford High School", "Thomas High School"]
school_series = pd.Series(high_schools)
print(school_series)
```

    0         Huang High School
    1      Figueroa High School
    2       Shelton High School
    3     Hernandez High School
    4       Griffin High School
    5        Wilson High School
    6       Cabrera High School
    7        Bailey High School
    8        Holden High School
    9          Pena High School
    10       Wright High School
    11    Rodriguez High School
    12      Johnson High School
    13         Ford High School
    14       Thomas High School
    dtype: object


## DataFrames

A Pandas DataFrame is a two-dimensional labeled data structure with rows and columns with many possible types of data. An equivalent can be an Excel table.

| School ID | School Name          | Type     |
|--------- |-------------------- |-------- |
| 0         | Huang High School    | District |
| 1         | Figueroa High School | District |
| 2         | Shelton High School  | Charter  |

```python
high_school_dicts = [{"School ID": 0, "school_name": "Huang High    School", "type": "District"},
                   {"School ID": 1, "school_name": "Figueroa High School", "type": "District"},
                    {"School ID": 2, "school_name":"Shelton High School", "type": "Charter"},
                    {"School ID": 3, "school_name":"Hernandez High School", "type": "District"},
                    {"School ID": 4, "school_name":"Griffin High School", "type": "Charter"}]
school_df = pd.DataFrame(high_school_dicts)
print(school_df)
```

       School ID            school_name      type
    0          0   Huang High    School  District
    1          1   Figueroa High School  District
    2          2    Shelton High School   Charter
    3          3  Hernandez High School  District
    4          4    Griffin High School   Charter

Creating a dictionary of information.

```python
school_id = [0, 1, 2, 3, 4]
school_name = ["Huang High School", "Figueroa High School",
"Shelton High School", "Hernandez High School","Griffin High School"]
type_of_school = ["District", "District", "Charter", "District","Charter"]
high_schools_dict = {"School ID": school_id, "school_name": school_name, "type":type_of_school}
school_df = pd.DataFrame(high_schools_dict)
print(high_school_df)
```


## Columns, Index and Values.

The DataFrame elements can be accessed via a few properties.

```python
print("Columns:\n", school_df.columns)
print("Index:\n", school_df.index)
print("Values:\n", school_df.values)
```

    Columns:
     Index(['School ID', 'school_name', 'type'], dtype='object')
    Index:
     RangeIndex(start=0, stop=5, step=1)
    Values:
     [[0 'Huang High School' 'District']
     [1 'Figueroa High School' 'District']
     [2 'Shelton High School' 'Charter']
     [3 'Hernandez High School' 'District']
     [4 'Griffin High School' 'Charter']]


# Loading a Dataset with Pandas

```python
from pathlib import Path

path = Path.cwd() / "resources"
file_name = "schools_complete.csv"


```
