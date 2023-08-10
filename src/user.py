class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.phone = None
        self.policy_details=None   
        self.selected_policy_no = None
        self.claim_form = None

    def show_name(self):
        print(self.name)

    def show_age(self):
        print(self.age)
