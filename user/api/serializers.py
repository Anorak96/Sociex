from user.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['email', 'username', 'profile_pic', 'cover_pic', 'user_post', 'follower', 'following', 'date_joined', 'password']

    def get_date_joined(self, post):
            return post.date_joined.strftime("%d-%b-%Y")

class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password1 = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']
    
    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields don't match."})
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password1'])
        user.save()
        return user

class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False, validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(read_only=False)
    profile_pic = serializers.ImageField(required=False)
    cover_pic = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = ['email', 'username', 'profile_pic', 'cover_pic']
    
    def update(self, instance, validated_data):
        instance.profile_pic = validated_data['profile_pic']
        instance.cover_pic = validated_data['cover_pic']
        instance.email = validated_data['email']
        instance.username = validated_data['username']
        instance.save()
        return instance