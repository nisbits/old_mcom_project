from django.db.models.signals import pre_delete,post_delete
from .models import DPR_file, DPR_table1
from django.dispatch import receiver

import os

# @receiver(pre_delete, sender=DPR_file)
# def pre_delete_profile(sender, **kwargs):
#     print("You are about to delete something!")

@receiver(post_delete, sender=DPR_file)
def delete_profile(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.dpr_file:
        if os.path.isfile(instance.dpr_file.path):
            os.remove(instance.dpr_file.path)
            print("File deleted")
            # print("You have just deleted a student!!!")


@receiver(post_delete, sender=DPR_table1)
def delete_profile(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.SOFT_AT_ACCEPTANCE_MAIL:
        if os.path.isfile(instance.SOFT_AT_ACCEPTANCE_MAIL.path):
            os.remove(instance.SOFT_AT_ACCEPTANCE_MAIL.path)
            print(instance.SITE_ID,"Soft at acceptance mail deleted")
            # print("You have just deleted a student!!!")
    if instance.PHYSICAL_AT_ACCEPTANCE_MAIL:
        if os.path.isfile(instance.PHYSICAL_AT_ACCEPTANCE_MAIL.path):
            os.remove(instance.PHYSICAL_AT_ACCEPTANCE_MAIL.path)
            print(instance.SITE_ID,"Physical at acceptance mail deleted")
            # print("You have just deleted a student!!!")
    # if instance.PERFORMANCE_AT_ACCEPTANCE_MAIL:
    #     if os.path.isfile(instance.PERFORMANCE_AT_ACCEPTANCE_MAIL.path):
    #         os.remove(instance.PERFORMANCE_AT_ACCEPTANCE_MAIL.path)
    #         print(instance.SITE_ID,"Performance at acceptance mail deleted")
    #         # print("You have just deleted a student!!!")

