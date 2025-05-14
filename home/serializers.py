from rest_framework import serializers

from . models import Student,Book,Author,Publisher
from datetime import datetime,date
from.validator import no_digit
from django.contrib.auth.models import User

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, validators = [no_digit])
    password = serializers.CharField(max_length=255)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length = 255)


    def validate_useername(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username already Exists")
        return username
    
    def create(self, validated_data):
        username=validated_data['username']
        password=validated_data['password']
        first_name=validated_data['first_name']
        last_name=validated_data['last_name']
        
        user = User.objects.create_user(username=username,password=password,first_name=first_name,last_name=last_name)
        
        return user
    
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, validators = [no_digit])
    password = serializers.CharField(max_length=255)
















class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"
        
    def generate_id(self,student_id):
        return (f"STU-{str(student_id).zfill(5)}")
    
    def calculate_age(self, dob_str):
        dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age
    
#clean or transform the name field before saving it        
    def to_internal_value(self, data):
        internal = super().to_internal_value(data)

        name = data.get('name')
        if name:
            internal['name'] = name.title()

        return internal
        
    def create(self, validated_data):
        student = Student.objects.create(**validated_data)
        student_id = student.id
        student.stu_id = self.generate_id(student_id)
        student.save()
        return student
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['age'] = self.calculate_age(data['dob'])
        return data
        
 
#Following DRF SERIALIZER 
class BookSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    author = serializers.CharField(max_length=100)
    price = serializers.FloatField()
    pages = serializers.IntegerField() 
    
    #unique validator  
    
    def calculate_gst(self,price):
        gst_amnt = (price*18)//100
        final_price = price+gst_amnt
        return final_price
    
    def to_representation(self, instance):
        return{
        "name" : instance.name,
        "author" : instance.author,
        "price" : self.calculate_gst(instance.price),
        "pages": instance.pages 
        }
        
        
    
    
    def create(self, validated_data):
        book_instanse = Book.objects.create(**validated_data)
        return book_instanse
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.author = validated_data.get('author',instance.author)
        instance.price = validated_data.get('price',instance.price)
        instance.pages = validated_data.get('pages',instance.pages)
        
        instance.save()
        return instance
    
    
    
    
class UserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, validators = [no_digit])
    email = serializers.EmailField()
    age = serializers.IntegerField()
    phone = serializers.RegexField(regex=r'^[6-9]\d{9}$',error_messages={'invalid':'phone number must be entered correctly'})
    
    def validate_age(self, value):
        if value < 18 or value > 30:
            raise serializers.ValidationError("Student must be at least 18 years old and less than 30 years old.")
        return value
    
    
    
    
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"
        
class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = "__all__"
        
class NewBookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    publishers = PublisherSerializer(many=True)
    
    class Meta:
        model = Book
        fields = "__all__"
        
        
class CrteateBookSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset = Author.objects.all() )
    publishers = serializers.PrimaryKeyRelatedField(queryset = Publisher.objects.all(),many=True)
    class Meta:
        model = Book
        filds = "__all__"