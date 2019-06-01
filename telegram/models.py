from django.db import models

class Members(models.Model):
	id = models.AutoField(primary_key = True)
	group_name = models.CharField(max_length = 256)
	members = models.TextField(default = "")
	no_of_members = models.IntegerField(default = 0)
	slug = models.CharField(max_length = 256)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.group_name + " : " + str(self.no_of_members)