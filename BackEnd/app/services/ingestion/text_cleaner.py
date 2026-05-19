import re


class TextCleaner:

    @staticmethod
    def clean(text: str) -> str:

        # remove excessive empty lines
        text = re.sub(
            r"\n\s*\n+",
            "\n",
            text
        )

        # normalize spaces/tabs only
        text = re.sub(
            r"[ \t]+",
            " ",
            text
        )

        return text.strip()