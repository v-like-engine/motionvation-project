from motionvation.data.models import Challenge, User

from motionvation.perform_challenge import performing_challenge


def accrue_xp(current_user, xp, db):
    user_now = db.query(User).filter(User.id == current_user.id).first()
    user_now.xp += xp
    challenges_to_get_xp = db.query(Challenge).filter(Challenge.user == current_user,
                                                      Challenge.get_xp == True,
                                                      Challenge.is_won == False).all().copy()
    performing_challenge(challenges_to_get_xp, xp)
