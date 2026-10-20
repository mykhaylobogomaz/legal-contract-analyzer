import re
import random

class Humanizer:
    def __init__(self):
        self.stamps = [
            "delve", "tapestry", "leveraging", "unlocking", "game-changer",
            "comprehensive", "robust", "transformative", "crucial", "essential",
            "multifaceted", "synergy", "seamless", "cutting-edge"
        ]

    def remove_ai_stamps(self, text: str) -> str:
        for stamp in self.stamps:
            text = re.sub(re.escape(stamp), "", text, flags=re.IGNORECASE)
        # Clean up whitespace
        text = " ".join(text.split())
        return text
