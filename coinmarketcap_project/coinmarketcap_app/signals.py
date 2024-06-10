# from django.core.signals import request_finished
# from django.dispatch import receiver
# import atexit

# def on_shutdown():
#     print("Django app is shutting down or restarting")

# @receiver(request_finished)
# def on_request_finished(sender, **kwargs):
#     if sender is None:
#         atexit.register(on_shutdown)

# try:
#     # Run the Django development server
#     # or start your Django application here
#     pass
# except KeyboardInterrupt:
#     # Handle keyboard interrupt (Ctrl+C)
#     on_shutdown()
