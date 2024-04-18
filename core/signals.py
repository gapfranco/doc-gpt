from django.conf import settings
from django.contrib.gis.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from core.utils.text_extractor import extract_body
from core.utils.vectordb_factory import VectorDBFactory

from .models import DocumentBody, Question, Topic

logger = settings.LOGGER


@receiver(post_save, sender=Question)
def post_insert_question(sender, instance, created, **kwargs):
    """Post_save signal from topic inclusion"""

    if not created:
        return

    models.signals.post_save.disconnect(post_insert_question, sender=sender)

    user = instance.user
    if user.query_balance > 0:
        user.query_balance -= 1
        user.save()
    topic_user = instance.topic.user

    if topic_user != user:
        topic_user.query_credits += 1
        topic_user.save()

    models.signals.post_save.connect(post_insert_question, sender=sender)


# @receiver(post_save, sender=Topic)
# def post_insert_topic(sender, instance, created, **kwargs):
#     """Post_save signal from topic inclusion"""
#
#     if not created:
#         return
#
#     models.signals.post_save.disconnect(post_insert_topic, sender=sender)
#
#     # Cria qdrant database
#     qdrant = QdrantManager(str(instance.id))
#     qdrant.get_collection()
#
#     models.signals.post_save.connect(post_insert_topic, sender=sender)


@receiver(pre_delete, sender=Topic)
def pre_delete_topic(sender, instance, **kwargs):
    models.signals.pre_delete.disconnect(pre_delete_topic, sender=sender)

    # Exclui qdrant collection
    vector_db = VectorDBFactory(instance.vector_db).get_vector_db()
    vector_db.collection_name(str(instance.id))
    vector_db.delete_collection()

    models.signals.pre_delete.connect(pre_delete_topic, sender=sender)


@receiver(post_save, sender=DocumentBody)
def post_insert_body(sender, instance, created, **kwargs):
    """Post_save signal from document body inclusion"""

    if not created:
        return

    models.signals.post_save.disconnect(post_insert_body, sender=sender)

    try:
        if instance.doc:
            extract_body.delay(
                instance.id,
                str(instance.document.topic.id),
                instance.document.topic.vector_db,
            )
            # extract_body(
            #     instance.id,
            #     str(instance.document.topic.id),
            #     instance.document.topic.vector_db,
            # )

    finally:
        models.signals.post_save.connect(post_insert_body, sender=sender)
