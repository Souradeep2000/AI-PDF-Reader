import re


class TextCleaner:

    @staticmethod
    def clean(text: str) -> str:
        text = re.sub(r"\s+", " ", text)

        text = re.sub(
            r"\n\s*\n",
            "\n",
            text
        )

        return text.strip()