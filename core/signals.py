from django.conf import settings
from django.contrib.gis.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from core.utils.QdrantManager import QdrantManager
from core.utils.text_extractor import extract_text

from .models import Document, Question, Topic

logger = settings.LOGGER


@receiver(post_save, sender=Question)
def post_insert_question(sender, instance, created, **kwargs):
    """Post_save signal from topic inclusion"""

    if not created:
        return

    models.signals.post_save.disconnect(post_insert_question, sender=sender)

    user = instance.topic.user
    if user.query_balance > 0:
        user.query_balance -= 1
        user.save()

    models.signals.post_save.connect(post_insert_question, sender=sender)


@receiver(post_save, sender=Topic)
def post_insert_topic(sender, instance, created, **kwargs):
    """Post_save signal from topic inclusion"""

    if not created:
        return

    models.signals.post_save.disconnect(post_insert_topic, sender=sender)

    # Cria qdrant database
    qdrant = QdrantManager(str(instance.id))
    qdrant.get_collection()

    models.signals.post_save.connect(post_insert_topic, sender=sender)


@receiver(pre_delete, sender=Topic)
def pre_delete_topic(sender, instance, **kwargs):
    models.signals.pre_delete.disconnect(pre_delete_topic, sender=sender)

    # Exclui qdrant collection
    qdrant = QdrantManager(str(instance.id))
    qdrant.delete_collection()

    models.signals.pre_delete.connect(pre_delete_topic, sender=sender)


@receiver(post_save, sender=Document)
def post_insert_document(sender, instance, created, **kwargs):
    """Post_save signal from document inclusion"""

    if not created:
        return

    models.signals.post_save.disconnect(post_insert_document, sender=sender)

    try:
        if instance.file:
            extract_text.delay(instance.file, str(instance.topic.id))
            # instance.base_name = os.path.basename(instance.file.name)
            # instance.save()
            # instance.file.delete()
            user = instance.topic.user
            if user.doc_balance > 0:
                user.doc_balance -= 1
                user.save()

    finally:
        models.signals.post_save.connect(post_insert_document, sender=sender)


@receiver(pre_delete, sender=Document)
def pre_delete_document(sender, instance, **kwargs):
    """Post_save signal from document inclusion"""

    models.signals.pre_delete.disconnect(pre_delete_document, sender=sender)

    # Recria database
    # qdrant = QdrantManagerLocal(str(instance.topic.collection_id))
    # db = qdrant.get_collection()

    models.signals.pre_delete.connect(pre_delete_document, sender=sender)
