from app.models.exercise import Difficulty, Exercise, ExerciseTestCase

EXERCISES = (
    Exercise(
        id="double-number",
        title="Double a Number",
        description="Complete a function that returns twice the number it receives.",
        difficulty=Difficulty.BEGINNER,
        starter_code="""def double_number(number):
    # Return number multiplied by two.
    pass
""",
        expected_behavior="Return the input number multiplied by 2.",
        function_name="double_number",
        concept_tags=("functions", "variables", "arithmetic"),
        test_cases=(
            ExerciseTestCase("positive number", (4,), 8, visible=True),
            ExerciseTestCase("negative number", (-3,), -6),
            ExerciseTestCase("zero", (0,), 0),
        ),
    ),
    Exercise(
        id="sum-even-numbers",
        title="Sum Even Numbers",
        description="Add only the even values in a list of integers.",
        difficulty=Difficulty.BEGINNER,
        starter_code="""def sum_even_numbers(numbers):
    total = 0
    # Inspect each number and add the even values.
    return total
""",
        expected_behavior="Return the sum of every even integer; an empty list returns 0.",
        function_name="sum_even_numbers",
        concept_tags=("loops", "lists", "conditionals"),
        test_cases=(
            ExerciseTestCase("mixed values", ([1, 2, 3, 4],), 6, visible=True),
            ExerciseTestCase("empty list", ([],), 0),
            ExerciseTestCase("repeated evens", ([2, 2, 5],), 4),
        ),
    ),
    Exercise(
        id="word-frequencies",
        title="Count Word Frequencies",
        description="Build a dictionary containing the number of times each word appears.",
        difficulty=Difficulty.INTERMEDIATE,
        starter_code="""def word_frequencies(words):
    counts = {}
    # Update counts as each word is visited.
    return counts
""",
        expected_behavior="Return an exact, case-sensitive count for every distinct word.",
        function_name="word_frequencies",
        concept_tags=("dictionaries", "loops", "counting"),
        test_cases=(
            ExerciseTestCase(
                "repeated words",
                (["red", "blue", "red"],),
                {"red": 2, "blue": 1},
                visible=True,
            ),
            ExerciseTestCase("empty input", ([],), {}),
            ExerciseTestCase("case sensitivity", (["Code", "code"],), {"Code": 1, "code": 1}),
        ),
    ),
    Exercise(
        id="first-duplicate",
        title="Find the First Duplicate",
        description="Return the first value whose second occurrence is encountered.",
        difficulty=Difficulty.INTERMEDIATE,
        starter_code="""def first_duplicate(values):
    seen = set()
    # Return when a value has already been seen.
    return None
""",
        expected_behavior="Return the first repeated value, or None when all values are unique.",
        function_name="first_duplicate",
        concept_tags=("sets", "loops", "algorithms"),
        test_cases=(
            ExerciseTestCase("duplicate order", ([2, 1, 3, 1, 2],), 1, visible=True),
            ExerciseTestCase("no duplicates", ([1, 2, 3],), None),
            ExerciseTestCase("immediate duplicate", ([7, 7],), 7),
        ),
    ),
)
