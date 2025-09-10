from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import json
import bcrypt

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

        print( f"CREDS: email: {username_or_email}, Password: {password}" )

        try:

            if role == 'passenger':
                # Logic for driver login
                # Find the user by username or email
                # We assume username is the email since that's how it's handled in sign up
                user = User.objects.get(email=username_or_email)
                
                # Convert the stored hashed password and submitted password to bytes
                hashed_pw_from_db = user.password
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
        
            elif role == 'driver':
                print( "Signing driver in" )
                user = Driver.objects.get(email=username_or_email)
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
                password=hashed_pw
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
                password=hashed_pw,
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
