from django.db import models


class User(models.Model):
    """
    Represents a user of the transport payment system.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, help_text="User's unique email address.")
    cell_number = models.CharField(max_length=20)
    momo_id = models.CharField(max_length=100, blank=True, null=True, 
                               help_text="Mobile money account identifier.")
    password = models.TextField(null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['last_name', 'first_name']


class Driver(models.Model):
    """
    Represents a driver in the transport payment system.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, help_text="Driver's unique email address.")
    license_number = models.CharField(max_length=50, unique=True, 
                                      help_text="Driver's unique license number.")
    license_plate = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.license_plate})"

    class Meta:
        verbose_name = "Driver"
        verbose_name_plural = "Drivers"
        ordering = ['last_name', 'first_name']


class Ride(models.Model):
    """
    Represents a single ride transaction between a user and a driver.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rides')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='rides')
    amount = models.DecimalField(max_digits=10, decimal_places=2, 
                                 help_text="The cost of the ride.")
    timestamp = models.DateTimeField(auto_now_add=True, 
                                     help_text="The date and time the ride was initiated.")
    RIDE_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=RIDE_STATUS_CHOICES, default='PENDING')
    
    def __str__(self):
        return f"Ride #{self.id} for {self.user.first_name} with {self.driver.first_name}"

    class Meta:
        verbose_name = "Ride"
        verbose_name_plural = "Rides"
        ordering = ['-timestamp']
