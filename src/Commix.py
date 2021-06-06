def reverse_dictionary(dictionary):
    return {v: k for k, v in dictionary.items()}


class Commix:

    def __init__(self, actions):
        self.actions = actions
        self.return_to_original = False
