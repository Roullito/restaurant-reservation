from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from datetime import time
from django.db.models import Sum

# ============================
# CLIENT — personne qui réserve
# ============================
class Client(models.Model):
    first_name = models.CharField(max_length=50)  # Prénom
    last_name = models.CharField(max_length=50)   # Nom
    email = models.EmailField(unique=True)        # Email unique (sert d'identifiant)
    phone = models.CharField(max_length=20)       # Numéro de téléphone (pas encore vérifié ici)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

# ===================================================
# RESERVATION — chaque ligne représente une réservation
# ===================================================
class Reservation(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE)  # Lien vers le client
    reservation_date = models.DateField()                            # Date de la réservation
    reservation_time = models.TimeField()                            # Heure du créneau réservé
    number_of_people = models.IntegerField(                          # Nombre de couverts
        validators=[MinValueValidator(1), MaxValueValidator(20)]    # entre 1 et 20 personnes max par résa
    )
    comment = models.TextField(blank=True)  # Commentaire optionnel

    def clean(self):
        # ==============================
        # 1. Créneaux horaires autorisés
        # ==============================
        allowed_times_midi = [time(h, m) for h in range(12, 14) for m in (0, 30)]
        allowed_times_soir = [time(h, m) for h in range(19, 21) for m in (0, 30)]

        # ==============================================
        # 2. Interdiction de réserver 2 fois le même jour
        # ==============================================
        doublon = Reservation.objects.filter(
            client=self.client,
            reservation_date=self.reservation_date
        ).exclude(pk=self.pk)  # exclure la réservation elle-même si elle est modifiée

        if doublon.exists():
            raise ValidationError("Ce client a déjà une réservation pour cette date.")

        # ============================
        # 3. Vérification de l'heure
        # ============================
        if self.reservation_time not in allowed_times_midi + allowed_times_soir:
            raise ValidationError("L'heure choisie n'est pas dans les créneaux disponibles.")

        # ==================================================
        # 4. Détermination du service : midi ou soir
        # ==================================================
        if 12 <= self.reservation_time.hour < 14:
            service_start = time(12, 0)
            service_end = time(14, 0)
            service_type = 'midi'
        elif 19 <= self.reservation_time.hour < 21:
            service_start = time(19, 0)
            service_end = time(21, 0)
            service_type = 'soir'
        else:
            raise ValidationError("L'heure ne correspond à aucun service.")

        # ================================================================
        # 5. Calcul du nombre total de couverts déjà réservés ce service
        # ================================================================
        total = Reservation.objects.filter(
            reservation_date=self.reservation_date,
            reservation_time__gte=service_start,
            reservation_time__lt=service_end
        ).exclude(pk=self.pk).aggregate(Sum('number_of_people'))['number_of_people__sum'] or 0

        # ==============================================
        # 6. Recherche de la limite configurée pour ce jour
        # ==============================================
        try:
            settings = ServiceSettings.objects.get(date=self.reservation_date)
        except ServiceSettings.DoesNotExist:
            settings = None  # fallback si aucune limite n’a été fixée

        # On récupère la limite selon le service (midi/soir), sinon on prend 150 par défaut
        if service_type == 'midi':
            limite = settings.midi_limit if settings else 150
        else:
            limite = settings.soir_limit if settings else 150

        # ===================================================
        # 7. Vérification que la limite de couverts n’est pas dépassée
        # ===================================================
        if total + self.number_of_people > limite:
            raise ValidationError(
                f"Ce service est complet ({total} couverts déjà réservés sur {limite})."
            )

    def __str__(self):
        return f"Réservation de {self.client} le {self.reservation_date} à {self.reservation_time}"

# ===============================================================
# SERVICE SETTINGS — limite de couverts pour une date spécifique
# ===============================================================
class ServiceSettings(models.Model):
    date = models.DateField(unique=True)                  # La date concernée
    midi_limit = models.IntegerField(default=150)         # Limite de couverts pour le service du midi
    soir_limit = models.IntegerField(default=150)         # Limite de couverts pour le soir

    def __str__(self):
        return f"Limites du {self.date} — Midi: {self.midi_limit} / Soir: {self.soir_limit}"
