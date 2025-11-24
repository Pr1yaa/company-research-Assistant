import re

class Critic:

    def evaluate(self, task_id, records):

        validated = []
        for r in records:
            text = str(r).strip()

            if len(text) < 3:
                continue

            # Remove noise
            if any(x in text.lower() for x in [
                "cookie", "policy", "subscribe", "sign up"
            ]):
                continue

            validated.append(text)

        confidence = 0.4 if len(validated) == 0 else 0.85

        return {
            "task_id": task_id,
            "validated_records": validated,
            "overall_confidence": confidence
        }
