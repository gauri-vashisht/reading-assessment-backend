class FeedbackService:

    def reading_level(
        self,
        wpm: float,
    ) -> str:

        if wpm >= 120:
            return "Excellent"

        elif wpm >= 100:
            return "Good"

        elif wpm >= 80:
            return "Average"

        return "Needs Improvement"

    def teacher_feedback(
        self,
        accuracy: float,
        skipped: int,
        incorrect: int,
        extra: int,
    ) -> str:

        feedback = []

        if accuracy >= 95:

            feedback.append(
                "Excellent reading accuracy."
            )

        elif accuracy >= 85:

            feedback.append(
                "Good reading accuracy."
            )

        else:

            feedback.append(
                "Needs additional reading practice."
            )

        if skipped:

            feedback.append(
                f"Skipped {skipped} word(s)."
            )

        if incorrect:

            feedback.append(
                f"Misread {incorrect} word(s)."
            )

        if extra:

            feedback.append(
                f"Added {extra} extra word(s)."
            )

        return " ".join(feedback)

    def student_feedback(
        self,
        accuracy: float,
        skipped: int,
        incorrect: int,
    ) -> str:

        feedback = []

        if accuracy >= 95:

            feedback.append(
                "Excellent reading."
            )

        elif accuracy >= 85:

            feedback.append(
                "Good reading."
            )

        else:

            feedback.append(
                "Keep practicing."
            )

        if skipped:

            feedback.append(
                "Avoid skipping words."
            )

        if incorrect:

            feedback.append(
                "Practice difficult words."
            )

        return " ".join(feedback)

    def summary(
        self,
        correct: int,
        total: int,
        wpm: float,
        accuracy: float,
    ) -> str:

        return (
            f"Read {correct}/{total} words "
            f"with {accuracy:.2f}% accuracy "
            f"at {wpm:.2f} WPM."
        )


feedback_service = FeedbackService()