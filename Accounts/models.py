from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CityChoices(models.TextChoices):
   CHENNAI = "CHN", "Chennai"
   TRICHY = "TRI", "Tiruchirappalli"
   COIMBATORE = "CBE", "Coimbatore"
   MADURAI = "MDU", "Madurai"
   SALEM = "SLM", "Salem"
   TIRUNELVELI = "TNV", "Tirunelveli"
   THANJAVUR = "TNJ", "Thanjavur"
   VELLORE = "VLR", "Vellore"
   ERODE = "ERD", "Erode"
   THOOTHUKUDI = "TTK", "Thoothukudi"
   KANYAKUMARI = "KNY", "Kanyakumari"
   DINDIGUL = "DGL", "Dindigul"
   TIRUVANNAMALAI = "TVM", "Tiruvannamalai"
   KARUR = "KRR", "Karur"
   NAGERCOIL = "NGK", "Nagercoil"
   TIRUPPUR = "TPR", "Tiruppur"
   CUDDALORE = "CDL", "Cuddalore"
   KRISHNAGIRI = "KGI", "Krishnagiri"
   NAMAKKAL = "NMK", "Namakkal"
   RAMANATHAPURAM = "RMD", "Ramanathapuram"
   SIVAGANGA = "SVG", "Sivaganga"
   THENI = "THN", "Theni"
   VIRUDHUNAGAR = "VNR", "Virudhunagar"
   NILGIRIS = "NLG", "Nilgiris"
   PERAMBALUR = "PBL", "Perambalur"
   ARIYALUR = "ARL", "Ariyalur"
   TIRUVARUR = "TVR", "Tiruvarur"
   PUDUKKOTTAI = "PDK", "Pudukkottai"


class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    contact = models.CharField(max_length=10, null=True, blank=True)
    city = models.CharField(
        max_length=3,  # Use appropriate max_length based on the code length
        choices=CityChoices.choices,
        default=CityChoices.CHENNAI,
        null=True,
        blank=True
    )


    