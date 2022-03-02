from django.db import models

class PublishStateOptions(models.TextChoices):
    '''state choices'''
    # CONSTANT = DB_VALUE, USER_DISPLAY_VA
    PUBLISH = 'PU', 'Published'
    DRAFT = 'DR', 'Draft'
    # UNLISTED = 'UN', 'Unlisted'
    # PRIAVATE = 'PR', 'Priavate'