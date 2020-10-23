class PicturePhoneGameError(RuntimeError):
    pass

class NotEnoughPlayersError(PicturePhoneGameError):
    pass

class PlayerAlreadyJoinedError(PicturePhoneGameError):
    pass