import laya


class LayaRunner:
    def __init__(self):
        print("Loading Laya...")
        self.agent = laya.load("convaiinnovations/laya")
        print("Laya loaded.")

    def predict(self, state, questions):
        return self.agent.predict(state, questions)