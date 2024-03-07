from django.contrib.auth import authenticate
from django.contrib.auth import logout
from .serializers import RegisterSerializer, ShowListSerializer,BookingSerializer,MovieSerializer
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_401_UNAUTHORIZED,
)
from django.shortcuts import get_object_or_404
from book_my_movies_admin.models import Movies,Shows,Bookings
from django.utils import timezone
import uuid
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import datetime
from django.http import HttpResponse
from reportlab.pdfgen import canvas
import io
import qrcode
from django.shortcuts import get_object_or_404

# Create your views here.

@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def register(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("account created successfully", status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_401_UNAUTHORIZED)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},status=HTTP_200_OK)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return Response("You are logged out successfully", status=HTTP_200_OK)
    

@api_view(['GET'])
@permission_classes((AllowAny,))
def movieList(request):
    movie=Movies.objects.all()
    serializer=MovieSerializer(movie, many=True)
    return Response(serializer.data)



@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def showList(request, movie_id):
        current_datetime = timezone.now()
        shows = Shows.objects.filter(
            movie__id=movie_id,
            is_disabled=False,
            show_date__gte=current_datetime.date(),
            )
        valid_shows = [
            show for show in shows
            if timezone.make_aware(datetime.combine(show.show_date, show.show_time)) >= current_datetime
        ]
        serializer = ShowListSerializer(valid_shows, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def myBookings(request):
    booking = Bookings.objects.filter(user=request.user)
    serializer = BookingSerializer(booking, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bookShow(request, pk):
    show =get_object_or_404(Shows,pk=pk)
    if show.is_disabled:
        return Response({'error': 'This show is disabled.'}, status=HTTP_400_BAD_REQUEST)

    # To prevent booking for past shows
    curr_datetime = datetime.now()
    show_datetime = datetime.combine(show.show_date, show.show_time)
    if curr_datetime > show_datetime:
        return Response({'error': 'Cannot book for past shows.'}, status=HTTP_400_BAD_REQUEST)

    booking_id = str(uuid.uuid4())[:8]
    number_of_tickets = request.data.get('number_of_tickets',1)

    # Save Booking
    booking = Bookings.objects.create(
        user=request.user, 
        show=show, 
        booking_id=booking_id,
        no_of_tickets=number_of_tickets,
        is_confirmed=True
        )
    
    subject = 'Movie Ticket Booking Confirmation'
    message = render_to_string('booking_confirmation_email.html', {'booking': booking})
    plain_message = strip_tags(message)
    from_email = 'abinjoseph90@gmail.com'
    to_email = [request.user.email]

    send_mail(subject, plain_message, from_email, to_email, html_message=message)

    
    serializer = BookingSerializer(booking)
    return Response(serializer.data, status=HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def confirmation(request,id):
    booking = Bookings.objects.get(id=id)
    serializer = BookingSerializer(booking)
    return Response(serializer.data, status=HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_pdf(request, id):
    booking = get_object_or_404(Bookings, id=id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="booking_{booking.booking_id}.pdf"'

    # Create PDF content using ReportLab
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    # Your PDF content generation logic here
    p.drawString(100, 800, f"Booking ID: {booking.booking_id}")
    p.drawString(100, 780, f"Movie Name: {booking.show.movie.movie_name}")
    p.drawString(100, 760, f"Show Date: {booking.show.show_date}")
    p.drawString(100, 740, f"Show Time: {booking.show.show_time.strftime('%H:%M %p')}")
    p.drawString(100, 720, f"Number of Tickets: {booking.no_of_tickets}")

    # Generate QR code based on booking ID
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f"Booking ID: {booking.booking_id}")
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img_path = f"media/qr_codes/booking_{booking.booking_id}.png"
    img.save(img_path)

    # Draw QR code image in the PDF
    p.drawInlineImage(img_path, 350, 720, width=100, height=100)

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()

    response.write(pdf)

    return response
