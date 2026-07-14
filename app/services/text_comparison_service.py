import re
from difflib import SequenceMatcher

class TextComparisonService:

    @staticmethod
    def normalize(
        text: str,
    ) -> list[str]:

        text = text.lower()

        text = re.sub(
            r"[^\w\s]",
            "",
            text,
        )

        return text.split()

    def compare(
        self,
        expected_text: str,
        transcript: str,
    ):

        expected = self.normalize(
            expected_text,
        )

        spoken = self.normalize(
            transcript,
        )

        matcher = SequenceMatcher(
            None,
            expected,
            spoken,
        )

        correct = 0

        skipped = 0

        incorrect = 0

        extra = 0

        incorrect_words = []

        skipped_words = []

        extra_words = []

        word_results = []

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():

            if tag == "equal":

                correct += i2 - i1

                for word in expected[i1:i2]:
                    word_results.append(
                        self.build_word_result(
                            word,
                            "correct",
                        )
                    )

            elif tag == "replace":

                incorrect += max(
                    i2 - i1,
                    j2 - j1,
                )

                incorrect_words.extend(
                    expected[i1:i2]
                )
                for word in expected[i1:i2]:
                    word_results.append(
                        self.build_word_result(
                            word,
                            "incorrect",
                        )
                    )

            elif tag == "delete":

                skipped += i2 - i1

                skipped_words.extend(
                    expected[i1:i2]
                )
                for word in expected[i1:i2]:
                    word_results.append(
                        self.build_word_result(
                            word,
                            "skipped",
                        )
                    )

            elif tag == "insert":

                extra += j2 - j1

                extra_words.extend(
                    spoken[j1:j2]
                )

        return {

            "total_words": len(expected),

            "correct_words": correct,

            "incorrect_words": incorrect,

            "skipped_words": skipped,

            "extra_words": extra,

            "incorrect_word_list":
                incorrect_words,

            "skipped_word_list":
                skipped_words,

            "extra_word_list":
                extra_words,
            
            "word_results": word_results,

        }
    
    def build_word_result(
        self,
        word: str,
        status: str,
    ):

        return {
            "word": word,
            "status": status,
        }


text_comparison_service = (
    TextComparisonService()
)