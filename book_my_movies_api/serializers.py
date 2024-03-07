from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from book_my_movies_admin.models import Movies,Shows,Bookings


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password')
        
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class ShowListSerializer(serializers.ModelSerializer):
    movie_name=serializers.CharField(source='movie.movie_name')
    movie_image=serializers.ImageField(source='movie.movie_image')
    class Meta:
        model = Shows
        fields = ['id', 'movie_name', 'movie_image', 'show_date', 'show_time','is_disabled']

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    movie_name=serializers.CharField(source='show.movie.movie_name')
    movie_image=serializers.ImageField(source='show.movie.movie_image')
    username=serializers.CharField(source='user.username')
    show_date=serializers.DateField(source='show.show_date')
    show_time=serializers.TimeField(source='show.show_time')
    class Meta:
        model = Bookings
        fields = ['id', 'no_of_tickets', 'booking_date', 'booking_id', 'is_confirmed', 'user', 'show_date','show_time', 'movie_name', 'movie_image', 'username']