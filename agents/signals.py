from django.dispatch import receiver
from axes.signals import user_locked_out
import logging

# Use the same logger we configured in settings.py
logger = logging.getLogger('axes')

@receiver(user_locked_out)
def on_lockout(sender, request, username, ip_address, **kwargs):
    """
    Triggers immediately when AXES_FAILURE_LIMIT is reached.
    """
    print("\n" + "!"*60)
    print(f"🚨 ALERT: BRUTE FORCE DETECTED")
    print(f"Target Account: {username}")
    print(f"Attacker IP: {ip_address}")
    print("!"*60 + "\n")
    
    # This also sends the alert to your security_audit.log file
    logger.warning(f"Lockout signal triggered for {username} at {ip_address}")