from __future__ import unicode_literals

import uuid
import copy

from django.db import models


class VersionManager(models.Manager):
    pass


class Recorder(models.Model):
    STATE_INVALID = 0
    STATE_DRAFT = 100
    STATE_PUBLISHED = 200
    STATE_ARCHIVED = 300
    STATE_CHOICES = (
        (STATE_INVALID, 'Invalid'),
        (STATE_DRAFT, 'Draft'),
        (STATE_PUBLISHED, 'Published'),
        (STATE_ARCHIVED, 'Archived'),
    )

    version_identity = models.UUIDField()
    version_id = models.UUIDField(unique=True)
    version_state = models.PositiveSmallIntegerField(choices=STATE_CHOICES, null=False, default=STATE_INVALID)
    version_created_at = models.DateTimeField(auto_now_add=True, blank=True)
    version_last_updated_at = models.DateTimeField(auto_now_add=True, blank=True)
    version_description = models.CharField(max_length=150)

    @classmethod
    def create_draft_version(cls, selected_version, **kwargs):
        """
        Create a clone of selected version object and save it in draft state
        :type selected_version: HistoryTrail | None
        :return: HistoryTrail
        """

        # Create a new object from class if no object is passed
        # this is done when a new draft object is need.
        if selected_version is None:
            selected_version = cls()
            # Assign a new identity if fresh object is getting created
            selected_version.version_identity = cls.generate_new_identity()
            selected_version.__dict__.update(kwargs)
        elif selected_version.version_state == cls.STATE_DRAFT:
            raise Exception("Can't create draft from draft object")

        # Move it draft state
        selected_version.version_state = cls.STATE_DRAFT
        selected_version.version_created_at = None
        selected_version.version_last_updated_at = None
        selected_version.version_description = "New Draft object created"
        # Create a new version
        selected_version.generate_new_version_id()
        selected_version.save()

    def change_state(self, new_state):
        """
        Performs any validation that are required for an version to do before doing
        state transition
        :param new_state:
        :return:
        """
        if not self.version_state == new_state:
            self.version_state = new_state
            self.save()
        else:
            raise Exception("Version state can't be changed if its already in that state")

    def _clone(self):
        """
        For internal use only.
        :return:
        """
        if self.pk is None:
            raise Exception("Can't clone a copy which is not saved")

        cloned_version = copy.copy(self)
        cloned_version.pk = None

        # Clone m2m relations
        # TODO: Move this code

        return cloned_version

    @classmethod
    def generate_new_identity(cls):
        """
        Generate a new UUID which can be used as an identity
        :return:
        """
        return uuid.uuid4()

    def generate_new_version_id(self):
        """
        Assign a new version id. For now its random. But it can be
        some hash of model-date with version identity.
        :return:
        """
        self.version_id = uuid.uuid4()

    class Meta:
        abstract = False
        unique_together = ('version_identity', 'version_id')
