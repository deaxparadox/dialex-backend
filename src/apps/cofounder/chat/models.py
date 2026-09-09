from django.conf import settings
from django.db import models


class CofounderSession(models.Model):
    """One chat session with the cofounder agent (spec 0044). No case-type,
    status, or approval concept — unlike Dialex's ConsultationSession, this
    product has no downstream Case/Debate pipeline to approve into."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cofounder_sessions"
    )
    title = models.CharField(default="New chat", max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"CofounderSession #{self.pk} ({self.title})"


class CofounderTurn(models.Model):
    """The user/agent back-and-forth log — same event-log shape as
    ConsultationTurn (spec 0044)."""

    class Speaker(models.TextChoices):
        USER = "user", "User"
        AGENT = "agent", "Agent"

    session = models.ForeignKey(CofounderSession, on_delete=models.CASCADE, related_name="turns")
    turn_number = models.PositiveIntegerField()
    speaker = models.CharField(max_length=20, choices=Speaker.choices)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("session", "turn_number")
        ordering = ["turn_number"]

    def __str__(self):
        return f"Turn {self.turn_number} ({self.speaker}) in session #{self.session_id}"


class CofounderGeneratedImage(models.Model):
    """A generated image's raw bytes (spec 0045), kept in its own table
    rather than in CofounderTurn.content: base64 image data is far too
    large for a Temporal Activity/Update result (a hard payload-size limit,
    hit for real during this spec's own verification) — turn history
    itself flows through Temporal, so it can never carry image bytes, only
    a small reference to a row here. Written directly by the graph node
    that generates the image (already running as one Activity), read back
    only by a plain REST endpoint that never touches Temporal at all."""

    session = models.ForeignKey(CofounderSession, on_delete=models.CASCADE, related_name="generated_images")
    data = models.TextField(help_text="Base64-encoded image bytes.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"CofounderGeneratedImage #{self.pk} (session #{self.session_id})"
