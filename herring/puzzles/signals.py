from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from puzzles.models import Puzzle
from django.conf import settings

if not settings.DEBUG:
    # because from oauth2client.client import SignedJwtAssertionCredentials is out of date and I don't know how to fix it.
    from puzzles.tasks import create_puzzle_sheet_and_channel

from puzzles.tasks import post_answer, post_update


if not settings.DEBUG:
    @receiver(post_save, sender=Puzzle)
    def on_puzzle_save(sender, instance, created, **kwargs):
        if created :
            create_puzzle_sheet_and_channel.delay(instance.slug)


@receiver(pre_save, sender=Puzzle)
def before_puzzle_save(sender, instance, **kwargs):
    if instance.answer:
        if instance.answer != instance.tracker.previous('answer'):
            post_answer.delay(instance.slug, instance.answer)

    if instance.tags != instance.tracker.previous('tags') and instance.tracker.previous('tags') is not None:
        post_update.delay(instance.slug, 'tags', instance.tags)

    if instance.note != instance.tracker.previous('note') and instance.tracker.previous('note') is not None:
        post_update.delay(instance.slug, 'notes', instance.note)
