from django.db import models


class Client(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="First Name")
    last_name = models.CharField(max_length=100, verbose_name="Last Name")
    document = models.IntegerField(verbose_name="Identification", unique=True)
    email = models.EmailField(max_length=100, verbose_name="Email", unique=True)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return self.first_name


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Name")
    description = models.TextField(verbose_name="Description")
    price = models.FloatField(verbose_name="Price")

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name


class Bill(models.Model):
    product = models.ManyToManyField(Product)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Client")
    company_name = models.CharField(max_length=200, verbose_name="Company Name")
    nit = models.IntegerField(verbose_name="NIT", unique=True)
    code = models.IntegerField(verbose_name="Code", unique=True)

    class Meta:
        verbose_name = "Bill"
        verbose_name_plural = "Bills"

    def __str__(self):
        return self.company_name
