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
        hints=(
            "Think about the arithmetic relationship between the input and the requested output.",
            "Use the multiplication operator with the function parameter and the value 2.",
            "Return the multiplication expression from the function instead of only computing it.",
        ),
        solution_explanation=(
            "The function needs one expression: multiply `number` by 2 and return that value. "
            "Returning matters because a calculation that is not returned is lost to the caller."
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
        hints=(
            "Visit every value while maintaining a running total.",
            "A number is even when its remainder after division by 2 is zero.",
            "Inside the loop, add only values matching `number % 2 == 0`, then return the total.",
        ),
        solution_explanation=(
            "Initialize a total at zero, iterate over the list, and add a number only when its "
            "remainder modulo 2 is zero. Return the total after the loop so empty input naturally "
            "produces zero."
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
        hints=(
            "Use each word as a dictionary key and store its count as the value.",
            "For each word, read its existing count with a default of zero before adding one.",
            "Update `counts[word]` inside the loop, then return the dictionary after every word.",
        ),
        solution_explanation=(
            "Start with an empty dictionary. For each word, retrieve the current value with "
            "`counts.get(word, 0)`, add one, and store it back. Returning after the loop preserves "
            "the exact case-sensitive keys from the input."
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
        hints=(
            "Track values already visited while scanning from left to right.",
            "A set gives fast membership checks and can record each first occurrence.",
            "Before adding a value to `seen`, return it if it is already present.",
        ),
        solution_explanation=(
            "Create an empty set and scan the list in order. If the current value is already in "
            "the set, return it immediately; otherwise add it. Return `None` only after the entire "
            "list is processed."
        ),
    ),
)
