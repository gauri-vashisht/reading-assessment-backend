class MetricsService:

    def calculate_accuracy(

        self,

        total_words: int,

        correct_words: int,

    ) -> float:

        if total_words == 0:
            return 0.0

        return round(

            (correct_words / total_words) * 100,

            2,

        )

    def calculate_wpm(

        self,

        correct_words: int,

        duration_seconds: float,

    ) -> float:

        if duration_seconds <= 0:
            return 0.0

        minutes = duration_seconds / 60

        return round(

            correct_words / minutes,

            2,

        )

    def build_metrics(

        self,

        comparison: dict,

        duration_seconds: float,

    ) -> dict:

        accuracy = self.calculate_accuracy(

            comparison["total_words"],

            comparison["correct_words"],

        )

        wpm = self.calculate_wpm(

            comparison["correct_words"],

            duration_seconds,

        )

        return {

            **comparison,

            "accuracy_percentage": accuracy,

            "words_per_minute": wpm,

        }


metrics_service = MetricsService()