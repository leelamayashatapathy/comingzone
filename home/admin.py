from django.contrib import admin


from .models import Student,Book,Author,Publisher

admin.site.register(Student)
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Publisher)

# Register your models here.
