from src.laya_runner import LayaRunner


runner = LayaRunner()

state = {
    "text": "The customer says they were charged twice."
}

questions = {
    "issue": {
        "type": "choice",
        "instructions": "What is the main issue?",
        "criteria": {
            "billing": "The issue concerns payments or charges.",
            "technical": "The issue concerns a technical problem.",
            "shipping": "The issue concerns delivery."
        }
    }
}

result = runner.predict(state, questions)

print(result)