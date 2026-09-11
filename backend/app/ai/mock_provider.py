from app.models.exercise import Exercise


class MockAIProvider:
    @property
    def name(self) -> str:
        return "mock"

    async def generate_hint(self, exercise: Exercise, code: str, level: int) -> str:
        if level not in (1, 2, 3):
            raise ValueError("Hint level must be between 1 and 3")
        if level == 3:
            code_observation = self._code_observation(exercise, code)
            if code_observation:
                return f"{exercise.hints[level - 1]} {code_observation}"
        return exercise.hints[level - 1]

    async def explain_solution(self, exercise: Exercise, code: str) -> str:
        if code.strip():
            return (
                f"{exercise.solution_explanation} Compare that flow with where your function "
                "updates state and returns its result."
            )
        return exercise.solution_explanation

    def _code_observation(self, exercise: Exercise, code: str) -> str | None:
        if not code.strip():
            return "Start by defining the required function before refining the logic."
        if f"def {exercise.function_name}" not in code:
            return f"The evaluator expects a function named `{exercise.function_name}`."
        if "pass" in code:
            return (
                "Your function still contains `pass`, so its main behavior is not implemented "
                "yet."
            )
        if "return" not in code:
            return "Your code has no `return` statement, so the evaluator will receive `None`."
        return None
