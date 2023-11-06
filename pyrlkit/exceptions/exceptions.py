class StateInitException(Exception):
    def __init__(
        self,
        message="Something went wrong while initialising state, the error is in the get_state() function",
    ):
        self.message = message
        super().__init__(message)


class StateManagementException(Exception):
    def __init__(self, func):
        self.func = func
        self.message = f"Something went wrong file training the model, the error is in the {func}() function"
        super().__init__(self.message)


class TrainingException(Exception):
    def __init__(self, func):
        self.func = func
        self.message = f"Something went wrong file training the model, the error is in the {func}() function"
        super().__init__(self.message)


class ModelCreationException(Exception):
    def __init__(
        self,
        message="Something went wrong whlie creating the model, the error is in the create_model() function",
    ):
        self.message = message
        super().__init__(message)


class EnvCreationException(Exception):
    def __init__(
        self,
        message="Something went wrong whlie creating the model, the error is in the create_env() function",
    ):
        self.message = message
        super().__init__(message)
