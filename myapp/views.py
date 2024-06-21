from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout



from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Booking
from django.http import JsonResponse, HttpResponseForbidden
from .models import Ambulance

from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Ambulance

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout



# for the firestore data 
import firebase_admin
from firebase_admin import credentials, firestore


# Initialize Firebase Admin SDK
# cred = credentials.Certificate(r"C:\Users\DELL\Downloads\lifesprint-97ff2-firebase-adminsdk-qj8nj-fdebbc308e.json")

cred = credentials.Certificate(r"C:\Users\DELL\Downloads\firebase api's\mine\ambugo-87a49-firebase-adminsdk-6y9yy-9187bbee22.json")


firebase_admin.initialize_app(cred)
db = firestore.client()


# def count_users(request):
#     # Construct a query to filter users based on certain conditions
#     users_ref = db.collection("users")
#     query = users_ref.where("age", ">", 18)  # Example: Filter users with age greater than 18

#     # Execute the query and count the results
#     query_results = query.stream()
#     user_count = len(list(query_results))

#     return JsonResponse({'user_count': user_count}, status=200)



def view_bookings(request):
    # Fetch all documents from the "bookings" collection in Firestore
    users_ref = db.collection("users")
    # users = users_ref.get()
    #  # Example: Filter users with age greater than 18

#     # Execute the query and count the results
    users = query.stream()

    # Parse booking data from Firestore documents
    users_list = []
    for user in users:
        user_data = user.to_dict()
        users_list.append(user_data)

    return render(request, 'view_users.html', {'users_list': users_list})



def dashboard(request):
    # Fetch users
    users_ref = db.collection("users")
    users = users_ref.stream()
    users_list = [user.to_dict() for user in users]
    user_count = len(users_list)

    # Fetch drivers
    drivers_ref = db.collection("driver")
    drivers = drivers_ref.stream()
    drivers_list = [driver.to_dict() for driver in drivers]
    driver_count = len(drivers_list)

    # fetch emergencies
    emergencies_ref = db.collection("emergencies")
    emergencies = emergencies_ref.stream()
    emergency_list = [emergency.to_dict() for emergency in emergencies]
    emergency_count = len(list(emergency_list))



    if request.method == 'POST':
        if request.method == 'POST':
            report_id = request.POST.get('message')
            driver_id = request.POST.get('driver_address')
        
        # Update the Firebase collection with the new data
        try:
            doc_ref = db.collection('emergencies').document(report_id)
            doc_ref.update({
                'ambulanceDetails': {
                    'driverId': driver_id
                },
                'ambulanceStatus':'assigned',
                'medicalReport': {
                    'nature_of_emergency': 'SAFE'
                }
            })
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})





    return render(request, 'dashboard.html', {
        # users
        'users_list': users_list,
        'user_count': user_count,
        # drivers
        'drivers_list': drivers_list,
        'driver_count': driver_count,
        # emergencies
        'emergency_list': emergency_list,
        'emergency_count': emergency_count

    })




    




def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    form = AuthenticationForm()  # Initialize the form outside the conditional blocks
    
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['user_id'] = user.id  # Set user ID in the session
                return redirect('index')
        # If form is invalid, it will continue to the rendering part below
    
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout


#@login_required(login_url='login')
# vunerable page not using sessions
def index(request):
  #return HttpResponse('hi guys')
  return render(request, 'index.html')
  

def maps(request):
    return render(request, 'maps.html')


@login_required(login_url='login')
def ambulance_registration(request):
    if request.user.id == request.session.get('user_id'):
        if request.method == 'POST':
            ambulance_number = request.POST.get('ambulance_number')
            telephone_number = request.POST.get('telephone_number')
            driver_name = request.POST.get('driver_name')
            ambulance_location = request.POST.get('ambulance_location')

            try:
                Ambulance.objects.create(ambulance_number=ambulance_number,telephone_number=telephone_number,ambulance_location=ambulance_location,driver_name=driver_name)
                messages.success(request, 'Ambulance registered successfully!')
            except Exception as e:
                messages.error(request, f'Error: {e}')

        return render(request, 'ambulance_registration.html')
    else:
        # Return forbidden response for unauthorized access
        return HttpResponseForbidden("Access Forbidden: Unauthorized user or session.")

@login_required(login_url='login')
def booking_page(request):
    if request.user.id == request.session.get('user_id'):

        if request.method == 'POST':
            patient_name = request.POST.get('patient_name')
            tel_number = request.POST.get('tel_number')
            pickup_location = request.POST.get('pickup_location')
            


            try:
                # Retrieve an available ambulance
                available_ambulance = Ambulance.objects.filter(availability=True).first()

                # Create a booking and assign the available ambulance if found
                new_booking = Booking(patient_name=patient_name, pickup_location=pickup_location)
                if available_ambulance:
                    new_booking.ambulance = available_ambulance
                    available_ambulance.availability = False  # Assuming the ambulance is no longer available after assignment
                    available_ambulance.save()
                new_booking.save()

                return JsonResponse({'success': True})
            except Exception as e:
                # Log the error for debugging purposes
                print(f"Error saving booking: {e}")
                return JsonResponse({'success': False, 'error': str(e)})

        # Handle GET request or rendering the form initially
        # Your GET request logic here
        return render(request, 'booking_page.html')
    else:
        # Return forbidden response for unauthorized access
        return HttpResponseForbidden("Access Forbidden: Unauthorized user or session.")




@login_required(login_url='login')
def booking_history(request):
    if request.user.id == request.session.get('user_id'):
        # Your logic for retrieving data (booking history)
        # Ensure you fetch the required data to display in the booking_history.html template
        bookings = Booking.objects.all()  # Example: Fetching booking data from a model
        print(bookings)
        return render(request, 'booking_history.html', {'bookings': bookings})
    else:
        # Return forbidden response for unauthorized access
        return HttpResponseForbidden("Access Forbidden: Unauthorized user or session.")



@login_required(login_url='login')
def confirmation_page(request):

    if request.user.id == request.session.get('user_id'):
        # Fetch multiple bookings (for demonstration, you might adjust the logic)
        bookings = Booking.objects.all()  # Retrieve all bookings or apply filtering as needed
        booking_details_list = []

        for booking in bookings:
            booking_details = {
                'Booking ID': booking.id,
                'Patient Name': booking.patient_name,
                'Pickup Location': booking.pickup_location,
                # Add other details as needed
            }
            booking_details_list.append(booking_details)

        return render(request, 'confirmation_page.html', {'booking_details_list': booking_details_list})
    else:
        # Return forbidden response for unauthorized access
        return HttpResponseForbidden("Access Forbidden: Unauthorized user or session.")

