from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
from django.db.models import Avg, Count, Min, Sum
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/default.png', upload_to='profile_pics')
    
    def __str__(self):
        return f'Profile {self.user.username}'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        img = Image.open(self.image.path)
        
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
            
class Mana(models.Model):
    belongs_to = models.ForeignKey(User, on_delete=models.CASCADE)
    power = models.BigIntegerField()
    date_of_assignment = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f'Mana {self.power}'
    
class Rune(models.Model):
    belongs_to = models.ForeignKey(User, on_delete=models.CASCADE)
    power = models.BigIntegerField()
    date_of_assignment = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f'Rune {self.power}'
    
    def clean_fields(self, *args, **kwargs):
        current_user_manas = Mana.objects.filter(belongs_to=self.belongs_to)
        current_user_mana_sum = current_user_manas.aggregate(all_power_sum=Sum('power'))['all_power_sum']
    
        if current_user_mana_sum - self.power < 0:
            raise ValidationError({'power':
                _("You do not have enough mana.")})
        
        #import pdb; pdb.set_trace()
        super().save(*args)