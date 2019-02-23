import action

class device:
    def __init__(self, n_element, name, id, num_pad, action_type):
        self.name = name
        self.id = id
        self.num_pad = num_pad
        self.action_type = action_type
        self.n_element = n_element
