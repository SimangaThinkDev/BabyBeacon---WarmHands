from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import json
import bcrypt
import requests
import base64
import uuid
from datetime import datetime
import os

from .models import User, Driver, Ride

# A basic view for the app's home page

def home(request):
    return HttpResponse(f"Welcome Home")

def sign_in(request):
    print("Sign-in view is touched")

    # For GET requests, just render the login form
    return render(request, 'app/sign_in.html')

def handle_sign_in(request):
    print( "---------------------- HANDLING SIGN IN -----------------------------" )
    if request.method == 'POST':
        # Get data from the form
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')

        print( f"CREDS: email: {username_or_email}, Password: {password}, Role: {role}" )

        try:

            if role == 'passenger':
                # Logic for driver login
                # Find the user by username or email
                # We assume username is the email since that's how it's handled in sign up
                print( User.objects.all() )
                user = User.objects.get(email=username_or_email)
                
                # Convert the stored hashed password and submitted password to bytes
                hashed_pw_from_db = user.password.encode('utf-8')
                password_to_check = str(password).encode('utf-8')

                # Verify the password using bcrypt
                if bcrypt.checkpw(password_to_check, hashed_pw_from_db):
                    # Passwords match!
                    # You would typically set up a session here to log the user in
                    # For example: from django.contrib.auth import login
                    # login(request, user)
                    print( "password match" )

                    return HttpResponse("Login successful!")
                else:
                    # Password does not match
                    return render(request, "app/sign_in.html", {'message': "Invalid credentials"})
        
            elif role == 'driver':
                print( "Signing driver in" )
                user = Driver.objects.get(email=str(username_or_email))
                print( user )
                
                # Convert the stored hashed password and submitted password to bytes
                hashed_pw_from_db = user.password.encode('utf-8')
                password_to_check = str(password).encode('utf-8')

                # Verify the password using bcrypt
                if bcrypt.checkpw(password_to_check, hashed_pw_from_db):
                    # Passwords match!
                    # You would typically set up a session here to log the user in
                    # For example: from django.contrib.auth import login
                    # login(request, user)
                    print( "password match" )
                    
                    return HttpResponse("Login successful!")
                else:
                    # Password does not match
                    return HttpResponse("Invalid credentials")

        except User.DoesNotExist:
            # User with that email/username doesn't exist
            return HttpResponse("Invalid credentials")
        
    return render( request, "app/sign_in.html", {'message': "Invalid Credentials"} )


def sign_up(request):
    return render( request, 'app/sign_up.html' )

def sign_up_driver(request):
    return render( request, 'app/sign_up_driver.html' )

def handle_user_reg(request):

    print( "Handle Reg is touched" )

    if request.method == 'POST':
        # Collect the data from the form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        cell_number = request.POST.get('cell_number')
        momo_id = request.POST.get('momo_id')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Simple validation: Check if passwords match
        if password != confirm_password:
            # You should provide more robust error handling,
            # perhaps by re-rendering the form with an error message.
            return HttpResponse("Error: Passwords do not match!")
        
        byte_passw = str( password ).encode( 'utf-8' )
        hashed_pw = bcrypt.hashpw( byte_passw, bcrypt.gensalt() )

        # Create a new User object and save it to the database
        try:
            new_user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                cell_number=cell_number,
                momo_id=momo_id,
                password=hashed_pw.decode('utf-8')
            )
            # Note: We are not storing the password directly in this model.
            # For a real application, you should use Django's built-in 
            # authentication system which handles password hashing securely.
            # Example: from django.contrib.auth.models import User as AuthUser
            # AuthUser.objects.create_user(username=email, password=password, ...)

            new_user.save()

            # After successful creation, redirect the user
            messages.success(request, 'Your action was successful!')
            message = "Successful Login"
            return render( request, 'app/sign_in.html', {'message': message} )

        except Exception as e:
            # Handle potential database errors (e.g., duplicate email)
            return HttpResponse(f"An error occurred: {e}")

    # If it's a GET request, render the empty form
    return render(request, 'app/sign_up.html')


def handle_driver_reg(request):

    print( "Handle Reg is touched" )

    if request.method == 'POST':
        # Collect the data from the form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        cell_number = request.POST.get('cell_number')
        license_number = request.POST.get('license_number')
        license_plate = request.POST.get('license_plate')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Simple validation: Check if passwords match
        if password != confirm_password:
            return HttpResponse("Error: Passwords do not match!")
        
        byte_passw = str( password ).encode( 'utf-8' )
        hashed_pw = bcrypt.hashpw( byte_passw, bcrypt.gensalt() )

        # Create a new User object and save it to the database
        try:
            new_driver = Driver.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                cell_number = cell_number,
                password=hashed_pw.decode('utf-8'),
                license_number=license_number,
                license_plate=license_plate,
            )
            new_driver.save()

            messages.success(request, 'Your action was successful!')
            message = "Successful Login"
            return render( request, 'app/sign_in.html', {'message': message} )

        except Exception as e:
            # Handle potential database errors (e.g., duplicate email)
            return HttpResponse(f"User Already Exists, Sign-Up Maybe")

    # If it's a GET request, render the empty form
    return render(request, 'app/sign_up.html')

@require_GET
def get_user_info(request, user_id):
    """
    Retrieves and returns information for a specific user.
    Uses user's primary key (id) to retrieve the object.
    
    Args:
        user_id (int): The primary key of the user.
    """
    # get_object_or_404 is a shortcut that raises Http404 if the object doesn't exist.
    user = get_object_or_404(User, pk=user_id)
    
    user_data = {
        'id': user.pk,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'cell_number': user.cell_number,
        'momo_id': user.momo_id,
    }
    return JsonResponse(user_data)

@require_GET
def get_driver_info(request, driver_id):
    """
    Retrieves and returns information for a specific driver.
    
    Args:
        driver_id (int): The primary key of the driver.
    """
    driver = get_object_or_404(Driver, pk=driver_id)
    
    driver_data = {
        'id': driver.pk,
        'first_name': driver.first_name,
        'last_name': driver.last_name,
        'email': driver.email,
        'license_number': driver.license_number,
        'license_plate': driver.license_plate,
    }
    return JsonResponse(driver_data)

@require_GET
def get_ride_history(request, entity_type, entity_id):
    """
    Retrieves the ride history for either a user or a driver.
    
    Args:
        entity_type (str): Specifies 'user' or 'driver'.
        entity_id (int): The primary key of the user or driver.
    """
    if entity_type not in ['user', 'driver']:
        return JsonResponse({'error': 'Invalid entity type. Must be "user" or "driver".'}, status=400)
    
    rides = []
    
    # Filter rides based on the entity type and ID.
    if entity_type == 'user':
        rides_queryset = Ride.objects.filter(user_id=entity_id).order_by('-timestamp')
    else:  # entity_type == 'driver'
        rides_queryset = Ride.objects.filter(driver_id=entity_id).order_by('-timestamp')

    # Serialize the queryset into a list of dictionaries.
    for ride in rides_queryset:
        rides.append({
            'id': ride.pk,
            'user_id': ride.user_id,
            'driver_id': ride.driver_id,
            'amount': str(ride.amount), # Convert DecimalField to string to be JSON serializable
            'timestamp': ride.timestamp.isoformat(),
            'status': ride.status,
        })
    
    return JsonResponse({'rides': rides})

@csrf_exempt  # This decorator is for demonstration. In a real app, use Django's CSRF protection.
@require_POST
def create_ride(request):
    """
    Creates a new ride transaction. Expects a POST request with JSON data.
    
    Expected JSON data:
    {
        "user_id": <int>,
        "driver_id": <int>,
        "amount": <decimal>
    }
    """
    try:
        data = json.loads(request.body)
        user = get_object_or_404(User, pk=data.get('user_id'))
        driver = get_object_or_404(Driver, pk=data.get('driver_id'))
        amount = data.get('amount')
        
        # Create and save the new Ride object
        ride = Ride.objects.create(
            user=user,
            driver=driver,
            amount=amount
        )
        
        return JsonResponse({
            'success': True, 
            'message': f'Ride {ride.pk} created successfully.',
            'ride_id': ride.pk
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON in request body.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

import requests
import uuid
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
import json

# ======== MTN MOMO CONFIGURATION ========
# You should move these to settings.py or environment variables
MOMO_PRIMARY_KEY = getattr(settings, 'MOMO_PRIMARY_KEY', 'your-primary-key')
MOMO_USER_ID = getattr(settings, 'MOMO_USER_ID', 'your-user-id')
MOMO_BASE_URL = "https://sandbox.momodeveloper.mtn.com"  # Use production URL when live

def get_momo_access_token():
    """Request OAuth2 token from MoMo API"""
    url = f"{MOMO_BASE_URL}/collection/token/"
    headers = {
        'Ocp-Apim-Subscription-Key': MOMO_PRIMARY_KEY,
        'Authorization': f'Basic {base64.b64encode(f"{MOMO_USER_ID}:{MOMO_PRIMARY_KEY}".encode()).decode()}'
    }
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        print("MoMo Token Error:", response.text)
        return None

def request_to_pay(request):
    """Initiate MoMo Payment Request"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    data = json.loads(request.body)
    amount = data.get('amount')
    phone_number = data.get('phone_number')
    external_id = str(uuid.uuid4())  # Unique transaction ID

    access_token = get_momo_access_token()
    if not access_token:
        return JsonResponse({'error': 'Failed to authenticate with MoMo'}, status=500)

    url = f"{MOMO_BASE_URL}/collection/v1_0/requesttopay"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'X-Reference-Id': external_id,
        'X-Target-Environment': 'sandbox',  # Change to 'mtnuganda' for production
        'Ocp-Apim-Subscription-Key': MOMO_PRIMARY_KEY,
        'Content-Type': 'application/json'
    }
    payload = {
        "amount": amount,
        "currency": "UGX",  # Change if needed (GHS, XOF, etc.)
        "externalId": external_id,
        "payer": {
            "partyIdType": "MSISDN",
            "partyId": phone_number
        },
        "payerMessage": "Payment for Ride",
        "payeeNote": "MoreMove Ride Payment"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 202:
        # Payment request accepted — poll for status or wait for callback
        return JsonResponse({
            'status': 'pending',
            'reference_id': external_id,
            'message': 'Payment request sent. User will receive prompt on phone.'
        })
    else:
        return JsonResponse({
            'error': 'Payment initiation failed',
            'details': response.json()
        }, status=400)

def handle_driver_dashboard(request):
    return render(request, 'app/driver_dashboard.html')

def landing_page(request):
    return render(request, 'app/landing_page.html')

def dashboard(request):
    return render(request, 'app/dashboard.html')

def check_payment_status(request, reference_id):
    """Check payment status using reference ID"""
    access_token = get_momo_access_token()
    if not access_token:
        return JsonResponse({'error': 'Auth failed'}, status=500)

    url = f"{MOMO_BASE_URL}/collection/v1_0/requesttopay/{reference_id}"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'X-Target-Environment': 'sandbox',
        'Ocp-Apim-Subscription-Key': MOMO_PRIMARY_KEY
    }

    response = requests.get(url, headers=headers)
    return JsonResponse(response.json())

def payment_page(request):
    """Render the payment page"""
    return render(request, 'app/payment.html')