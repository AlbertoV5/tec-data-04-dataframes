"""
PyCitySchools Test.

In this tests we want to demonstrate that removing a small amount of data 
won't impact the results enough to be noticeable.

We will load the same dataset and create two dataframes.
The first one will be the unmodified dataset and the second one will be
the dataset with the grades from 9th grade of Thomas High School removed.

We will get the averages and sort the values and compare the results.

This tests can be run with the "pytest" command.
"""

import numpy as np
import pandas as pd
from pathlib import Path
import logging
import pytest


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
STUDENTS_PATH = Path("resources") / "clean_students_complete.csv"
SCHOOLS_PATH = Path("resources") / "schools_complete.csv"
SCHOOL_NAME = "school_name"
STUDENT_NAME = "student_name"
MATH_SCORE = "math_score"
READING_SCORE = "reading_score"


@pytest.fixture
def schools_df():
    schools_df = pd.read_csv(SCHOOLS_PATH, index_col=0)
    schools_df = schools_df.set_index(SCHOOL_NAME)
    return schools_df


@pytest.fixture
def complete_df():
    students_df = pd.read_csv(STUDENTS_PATH, index_col=0)
    schools_df = pd.read_csv(SCHOOLS_PATH, index_col=0)
    complete_df = pd.merge(
        students_df, schools_df, how="left", on=[SCHOOL_NAME, SCHOOL_NAME]
    )
    schools_df = schools_df.set_index(SCHOOL_NAME)
    complete_df = complete_df.set_index(SCHOOL_NAME)
    return complete_df


@pytest.fixture
def modified_df(complete_df: pd.DataFrame):
    complete_df = complete_df.copy()
    criteria = (complete_df["grade"] == "9th") & (
        complete_df.index == "Thomas High School"
    )
    complete_df.loc[criteria, [MATH_SCORE, READING_SCORE]] = np.nan
    complete_df = complete_df.dropna()
    return complete_df


def get_parameters(df: pd.DataFrame):
    """Calculate all the parameters used for the test.
    Average Math Score, Average Reading Score, etc."""
    # Get averages
    per_school_math_average = df.groupby(SCHOOL_NAME)[MATH_SCORE].mean()
    per_school_reading_average = df.groupby(SCHOOL_NAME)[READING_SCORE].mean()
    # Get passing totals
    per_school_passing_math = df.loc[df[MATH_SCORE] >= 70, MATH_SCORE]
    per_school_passing_reading = df.loc[df[READING_SCORE] >= 70, READING_SCORE]
    per_school_passing_overall = df.loc[
        (df[READING_SCORE] >= 70) & (df[MATH_SCORE] >= 70), [READING_SCORE, MATH_SCORE]
    ]
    # Get total
    per_school_total_students = df.groupby(SCHOOL_NAME)[STUDENT_NAME].count()
    # Get passing percentages
    per_school_passing_math_percentage = (
        100
        * per_school_passing_math.groupby(SCHOOL_NAME).count()
        / per_school_total_students
    )
    per_school_passing_reading_percentage = (
        100
        * per_school_passing_reading.groupby(SCHOOL_NAME).count()
        / per_school_total_students
    )
    per_school_passing_overall_percentage = (
        100
        * per_school_passing_overall[READING_SCORE].groupby(SCHOOL_NAME).count()
        / per_school_total_students
    )
    parameters = {
        "Average Math Score": per_school_math_average,
        "Average Reading Score": per_school_reading_average,
        "% Passing Math": per_school_passing_math_percentage,
        "% Passing Reading": per_school_passing_reading_percentage,
        "% Overall Passing": per_school_passing_overall_percentage,
    }
    return parameters


@pytest.fixture
def complete_parameters(complete_df):
    return get_parameters(complete_df)


@pytest.fixture
def modified_parameters(modified_df):
    return get_parameters(modified_df)


def get_schools_average_score_per(
    df: pd.DataFrame, column: str, value: str, score: str
) -> pd.Series:
    """Find a given column's value and return a series of averages grouped by school name."""
    new_df = df.loc[df[column] == value].groupby("school_name").mean()[score]
    new_df.index.name = ""
    return new_df


def get_scores_per_grade(df: pd.DataFrame):
    math_scores = pd.DataFrame(
        {
            grade: get_schools_average_score_per(df, "grade", grade, MATH_SCORE)
            for grade in ("9th", "10th", "11th", "12th")
        }
    )
    reading_scores = pd.DataFrame(
        {
            grade: get_schools_average_score_per(df, "grade", grade, READING_SCORE)
            for grade in ("9th", "10th", "11th", "12th")
        }
    )
    return math_scores.merge(
        reading_scores,
        left_index=True,
        right_index=True,
        suffixes=(f"_{MATH_SCORE}", f"_{READING_SCORE}"),
    )


def group_scores_by(binned_series: pd.Series, parameters) -> pd.DataFrame:
    """Obtains the averages and percentages of scores and groups them
    in bins."""
    new_df = pd.DataFrame({"Series": binned_series, **parameters})
    grouped_df = new_df.groupby("Series").mean()
    grouped_df.index.name = ""
    return grouped_df


def compare_dataframes(original: pd.DataFrame, modified: pd.DataFrame):
    """Substract modified DF from original.
    Check that the values in the difference are smaller than 1%."""
    assert original.size == modified.size
    difference = original - modified
    for col_diff, col in zip(difference, original):
        for val_diff, val in zip(difference[col_diff], original[col]):
            ratio = abs(val_diff / val)
            assert ratio < 0.01
            if ratio != 0:
                msg = f"{col_diff} DIFFERENCE: {100*ratio:.2f}%"
                log.info(msg)
    log.info(difference)


##########
# TESTS
##########


def test_school_grades(complete_df: pd.DataFrame, modified_df: pd.DataFrame):
    """
    Catch the AssertionError that happens when comparing NaN values.

    Result:
        PyCitySchools_test.py::test_school_grades PASSED
    """
    original = get_scores_per_grade(complete_df)
    modified = get_scores_per_grade(modified_df)
    with pytest.raises(AssertionError):
        compare_dataframes(original, modified)


def test_school_spending(
    complete_parameters: dict, modified_parameters: dict, schools_df: pd.DataFrame
):
    """
    Measure differences on spending results.

    Result:
                Average Math Score  Average Reading Score  % Passing Math  % Passing Reading  % Overall Passing

    <$586               0.000000               0.000000         0.00000           0.000000           0.000000
    $586-630            0.000000               0.000000         0.00000           0.000000           0.000000
    $631-645            0.016853              -0.011788         0.02162           0.072532           0.079422
    $646-675            0.000000               0.000000         0.00000           0.000000           0.000000

    We can conclude that the difference is negligent as the data is below one percent (0.01).
    """
    bins = [0, 585, 630, 645, 675]
    labels = ["<$586", "$586-630", "$631-645", "$646-675"]
    binned = pd.cut(schools_df["budget"] / schools_df["size"], bins, labels=labels)
    complete = group_scores_by(binned, complete_parameters)
    modified = group_scores_by(binned, modified_parameters)
    compare_dataframes(complete, modified)


def test_school_sizes(
    complete_parameters: dict, modified_parameters: dict, schools_df: pd.DataFrame
):
    """
    Measure differences on school sizes results.

    Result:
                        Average Math Score  Average Reading Score  % Passing Math  % Passing Reading  % Overall Passing

    Small (<1000)                 0.000000                0.00000        0.000000           0.000000           0.000000
    Medium (1000-1999)            0.013482               -0.00943        0.017296           0.058026           0.063538
    Large (2000-5000)             0.000000                0.00000        0.000000           0.000000           0.000000
    """
    bins = [0, 999, 1999, 5000]
    labels = ["Small (<1000)", "Medium (1000-1999)", "Large (2000-5000)"]
    binned = pd.cut(schools_df["size"], bins, labels=labels)
    complete = group_scores_by(binned, complete_parameters)
    modified = group_scores_by(binned, modified_parameters)
    compare_dataframes(complete, modified)


def test_school_types(
    complete_parameters: dict, modified_parameters: dict, schools_df: pd.DataFrame
):
    """
    Measure differences on school types results.

    Result:
                Average Math Score  Average Reading Score  % Passing Math  % Passing Reading  % Overall Passing

    Charter             0.008426              -0.005894         0.01081           0.036266           0.039711
    District            0.000000               0.000000         0.00000           0.000000           0.000000
    """
    complete = group_scores_by(schools_df["type"], complete_parameters)
    modified = group_scores_by(schools_df["type"], modified_parameters)
    compare_dataframes(complete, modified)


def test_ths_grades(complete_parameters: dict, modified_parameters: dict):
    """
    Find if Thomas High School scores changed dramatically after the change.

    Result:
                        Average Math Score  Average Reading Score  % Passing Math  % Passing Reading  % Overall Passing

    Thomas High School            0.067412              -0.047152        0.086481           0.290129           0.317689
    """
    original_df = pd.DataFrame({**complete_parameters})
    modified_df = pd.DataFrame({**modified_parameters})
    original_ths = original_df.loc[["Thomas High School"]]
    modified_ths = modified_df.loc[["Thomas High School"]]
    original_ths.index.name = ""
    modified_ths.index.name = ""
    compare_dataframes(original_ths, modified_ths)


def test_ths_ranks(complete_parameters: dict, modified_parameters: dict):
    """
    Find if Thomas High School rank amongst other schools changed.

    Result:
        Thomas High School rank moved from 4 to 6 in Average Math Score.
        Thomas High School rank moved from 1 to 3 in % Passing Reading.
                        Average Math Score  Average Reading Score  % Passing Math  % Passing Reading  % Overall Passing

    Thomas High School                  -2                      0               0                 -2                  0

    """
    original_df = pd.DataFrame(complete_parameters)
    modified_df = pd.DataFrame(modified_parameters)
    size = complete_parameters["Average Math Score"].size
    rank_difference = pd.DataFrame()
    for category in complete_parameters:
        original = original_df.sort_values(by=category, ascending=False)
        modified = modified_df.sort_values(by=category, ascending=False)
        original["rank"] = range(1, size + 1)
        modified["rank"] = range(1, size + 1)
        original_rank = original.loc[original.index == "Thomas High School", "rank"]
        modified_rank = modified.loc[modified.index == "Thomas High School", "rank"]
        rank_shift = original_rank - modified_rank
        if rank_shift.values[0] != 0:
            log.info(
f"""Thomas High School rank moved from {original_rank.values[0]} to {modified_rank.values[0]} in {category}."""
            )
        rank_difference[category] = rank_shift

    rank_difference.index.name = ""
    log.info(rank_difference)


def main():
    print(
        """Please run this script with pytest.
$ pip install pytest
$ pytest"""
    )


if __name__ == "__main__":
    main()
