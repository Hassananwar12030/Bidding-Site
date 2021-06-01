from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
class User(AbstractUser):
    pass

class list_item(models.Model):
	id= models.AutoField(primary_key=True)
	title = models.CharField(max_length=124)
	initiator=models.ForeignKey(User, on_delete=models.CASCADE, name="item_creator")
	bidPrice = models.DecimalField(max_digits=10, decimal_places=2,validators= [MinValueValidator(1)])
	category_choices = [
	("Fashion", "Fashion"),
	("Toys", "Toys"),
	("Electronics", "Electronics"),
	("Home", "Home"),
	("Other", "Other"),
	]
	category = models.CharField(
		max_length= 124,
		choices = category_choices,
		default = "Home",
	)
	picture_item= models.ImageField(upload_to="images/")
	description = models.TextField(default="None")
	closed = models.BooleanField(default=False)
	def __str__(self):
		return f"ItemID: {self.id}, Name: {self.title} & Bid_Price: {self.bidPrice}$"
class bid(models.Model):
	bid_item = models.OneToOneField(list_item, on_delete= models.CASCADE, name="bid", primary_key=True)
	userName = models.ForeignKey(User, on_delete=models.CASCADE, name="bidder")
	def __str__(self):
		return f"Item_Name: {self.bid.title}, Price_Set: {self.bid.bidPrice} & Bidder is: {self.bidder} "

		
class comment(models.Model):
	id = models.AutoField(primary_key=True)
	item_id = models.ForeignKey(list_item, on_delete=models.CASCADE)
	userName = models.ForeignKey(User, on_delete=models.CASCADE, name="commenter")
	comment = models.TextField(default="")
	def __str__(self):
		return f"Item: {self.item_id.title}, Commenter: {self.commenter.username}, & Comment_is: {self.comment}"

class watchlist(models.Model):
	id = models.AutoField(primary_key=True)
	item = models.ForeignKey(list_item, on_delete=models.CASCADE)
	userName = models.ForeignKey(User, on_delete=models.CASCADE)
	def __str__(self):
		return f"ID: {self.id}, Item: {self.item.title}, & UserName: {self.userName.username}"

