from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
import json

from .models import User, Driver, Ride

# A basic view for the app's home page
def home(request):
    """
    A simple home page view.
    """
    # return JsonResponse({'message': 'Welcome to the Transport Payment System API!'})
    return render( request, 'app/sign_in.html' )

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
        'vehicle_make': driver.vehicle_make,
        'vehicle_model': driver.vehicle_model,
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
