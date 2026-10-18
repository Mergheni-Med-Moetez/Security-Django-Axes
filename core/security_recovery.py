from axes.utils import reset


def unlock_user(username):
    """Reset lockout state for one username."""
    reset(username=username)


def unlock_ip(ip_address):
    """Reset lockout state for one IP address."""
    reset(ip=ip_address)


def unlock_user_from_ip(username, ip_address):
    """Reset lockout state for a username and source IP pair."""
    reset(username=username, ip=ip_address)
