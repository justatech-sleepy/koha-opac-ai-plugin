from app.knowledge.knowledge_base import KNOWLEDGE_BASE

class IntentEngine:

    def detect(self, message: str):

        text = message.lower()

        best = None
        score = 0

        for item in KNOWLEDGE_BASE:

            matches = 0

            for keyword in item["keywords"]:
                if keyword in text:
                    matches += 1

            if matches > score:
                score = matches
                best = item

        if best:

            confidence = score / len(best["keywords"])

            return {
                "intent": best["intent"],
                "confidence": round(confidence,2),
                "response": best["response"]
            }

        return {
            "intent":"UNKNOWN",
            "confidence":0.0,
            "response":"Sorry, I don't know that yet."
        }
