from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.conf import settings
from .models import Products, Crop, Contact, CropRecommendationLog, AddCropData
import csv
import os

# Create base CSV if it doesn't exist
CSV_PATH = os.path.join(settings.BASE_DIR, 'static', 'Crop_recommendation.csv')
if not os.path.exists(CSV_PATH):
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
    with open(CSV_PATH, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'label'])

# Create your views here.
def index(request):
    return render(request,"index.html")

def contact(request):
    return render(request, "contact.html")

def about(request):
    return render(request,"about.html")

def service(request):
    return render(request,"service.html")

def register(request):
    if request.method=="POST":
        fn=request.POST['fname']
        ln=request.POST['lname']
        un=request.POST['uname']
        em=request.POST['email']
        ps=request.POST['psw']
        ps1=request.POST['psw1']
        if ps==ps1:
            if User.objects.filter(username=un).exists():
                messages.info(request,"Username Exists")
                return render(request,"register.html")
            elif User.objects.filter(email=em).exists():
                messages.info(request,"Email Exists")
                return render(request,"register.html")
            else:
                user=User.objects.create_user(first_name=fn,
                    last_name=ln,username=un,email=em,password=ps1)
                user.save()
                return HttpResponseRedirect('login')
        else:
            messages.info(request,"Password Not Matching")
            return render(request,"register.html")
    else:
        return render(request,"register.html")
    return render(request,"register.html")

def login(request):
    if request.method=="POST":
        un=request.POST['uname']
        ps=request.POST['psw']
        user=auth.authenticate(username=un,password=ps)
        if user is not None:
            auth.login(request,user)
            return HttpResponseRedirect('/farmer/index')
        else:
            messages.info(request,"Invalid Credentials")
            return render(request,"login.html")

    return render(request,"login.html")

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/farmer/index')

def product(request):
    p=Products.objects.all()
    return render(request,"product.html",{"p":p})

def crop(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please login to get crop recommendations.")
        return redirect('login')
        
    if request.method=="POST":
        try:
            nitro=int(request.POST['Nitrogen'])
        except ValueError:
            nitro = 0
        try:
            phos=int(request.POST['Phosphorous'])
        except ValueError:
            phos = 0
        try:
            potas=int(request.POST['Potassium'])
        except ValueError:
            potas = 0
        try:
            temp=float(request.POST['Temperature'])
        except ValueError:
            temp = 0.0
        try:
            humid=float(request.POST['Humidity'])
        except ValueError:
            humid = 0.0
        try:
            ph=float(request.POST['Ph'])
        except ValueError:
            ph = 0.0
        try:
            rain=float(request.POST['Rainfall'])
        except ValueError:
            rain = 0.0
        soil=request.POST.get('soil', None)
        from sklearn.preprocessing import LabelEncoder
        l=LabelEncoder()
        soil1=l.fit_transform([soil])
        import pandas as pd
        df=pd.read_csv(CSV_PATH)
        X=df.drop("label",axis=1)
        y=df["label"]

        from sklearn.linear_model import LogisticRegression
        log=LogisticRegression()
        log.fit(X,y)
        import numpy as np
        crop_data=np.array([[nitro,phos,potas,temp,humid,ph,rain]],dtype=object)
        pred_crop=log.predict(crop_data)
        
        # Save to Crop model
        crop=Crop.objects.create(Nitrogen=nitro,Phosphorous=phos,Potassium=potas,
                                Temperature=temp,Rainfall=rain,PH=ph,
                                Humidity=humid,Recommend_Crop=pred_crop)
        crop.save()
        
        # Log the recommendation
        log = CropRecommendationLog.objects.create(
            n=nitro,
            p=phos,
            k=potas,
            temperature=temp,
            humidity=humid,
            ph=ph,
            rainfall=rain,
            recommended_crop=pred_crop[0]
        )
        log.save()
        return render(request,"predict.html",{"nitro":nitro,
            "phos":phos,"potas":potas,"temp":temp,"humid":humid,
            "ph":ph,"rain":rain,"prediction":pred_crop})

    return render(request,"crop.html")

def predict(request):
    return render(request,"predict.html")

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Products, Crop, Contact, CropRecommendationLog, AddCropData, Feedback

@login_required
def history(request):
    logs = CropRecommendationLog.objects.all()
    unique_crops = logs.values_list('recommended_crop', flat=True).distinct()
    return render(request, "history.html", {
        "logs": logs,
        "unique_crops": unique_crops
    })

@login_required
def delete_log(request, log_id):
    if request.method == "POST":
        log = CropRecommendationLog.objects.get(id=log_id)
        log.delete()
        messages.success(request, "Log entry deleted successfully.")
    return redirect('history')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_data(request):
    if request.method == "POST":
        try:
            # Create new entry
            new_entry = AddCropData(
                n=int(request.POST['n']),
                p=int(request.POST['p']),
                k=int(request.POST['k']),
                temperature=float(request.POST['temperature']),
                humidity=float(request.POST['humidity']),
                ph=float(request.POST['ph']),
                rainfall=float(request.POST['rainfall']),
                label=request.POST['label']
            )
            new_entry.save()

            # Append to CSV
            with open(CSV_PATH, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    new_entry.n, new_entry.p, new_entry.k,
                    new_entry.temperature, new_entry.humidity,
                    new_entry.ph, new_entry.rainfall, new_entry.label
                ])
            
            messages.success(request, f"Data for {new_entry.label} has been added successfully!")
        except Exception as e:
            messages.error(request, f"Error adding data: {str(e)}")

    # Get recent entries for display
    recent_entries = AddCropData.objects.order_by('-added_at')[:10]
    return render(request, "add_data.html", {"recent_entries": recent_entries})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_data(request, entry_id):
    try:
        entry = AddCropData.objects.get(id=entry_id)
        if request.method == "POST":
            # Update entry
            entry.n = int(request.POST['n'])
            entry.p = int(request.POST['p'])
            entry.k = int(request.POST['k'])
            entry.temperature = float(request.POST['temperature'])
            entry.humidity = float(request.POST['humidity'])
            entry.ph = float(request.POST['ph'])
            entry.rainfall = float(request.POST['rainfall'])
            entry.label = request.POST['label']
            entry.save()

            # Update CSV
            with open(CSV_PATH, 'r', newline='') as file:
                rows = list(csv.reader(file))
            
            # Find and update the matching row
            for row in rows[1:]:  # Skip header
                if row[7] == entry.label:  # Match by label
                    row[0] = entry.n
                    row[1] = entry.p
                    row[2] = entry.k
                    row[3] = entry.temperature
                    row[4] = entry.humidity
                    row[5] = entry.ph
                    row[6] = entry.rainfall
            
            # Write back to CSV
            with open(CSV_PATH, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)
            
            messages.success(request, f"Entry for {entry.label} updated successfully!")
        return redirect('add_data')
    except Exception as e:
        messages.error(request, f"Error updating entry: {str(e)}")
        return redirect('add_data')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_data(request, entry_id):
    try:
        entry = AddCropData.objects.get(id=entry_id)
        entry_label = entry.label
        entry.delete()

        # Update CSV
        with open(CSV_PATH, 'r', newline='') as file:
            rows = list(csv.reader(file))
        
        # Remove matching row
        rows = [row for row in rows if row[7] != entry_label]  # Filter out the deleted entry
        
        # Write back to CSV
        with open(CSV_PATH, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        
        messages.success(request, f"Entry for {entry_label} deleted successfully!")
    except Exception as e:
        messages.error(request, f"Error deleting entry: {str(e)}")
    
    return redirect('add_data')

@login_required
@login_required
def delete_feedback(request, feedback_id):
    try:
        feedback = Feedback.objects.get(id=feedback_id)
        # Only superusers can delete any feedback, users can only delete their own
        if request.user.is_superuser or feedback.user == request.user:
            feedback.delete()
            messages.success(request, "Feedback deleted successfully!")
        else:
            messages.error(request, "You don't have permission to delete this feedback.")
    except Feedback.DoesNotExist:
        messages.error(request, "Feedback not found.")
    return redirect('feedback')

@login_required
def edit_feedback(request, feedback_id):
    try:
        feedback = Feedback.objects.get(id=feedback_id)
        # Only allow users to edit their own feedback
        if feedback.user != request.user:
            messages.error(request, "You can only edit your own feedback.")
            return redirect('feedback')

        if request.method == "POST":
            feedback.rating = int(request.POST['rating'])
            feedback.comment = request.POST['comment']
            feedback.save()
            messages.success(request, "Your feedback has been updated!")
            return redirect('feedback')

        return render(request, 'feedback.html', {
            'rating_choices': Feedback.RATING_CHOICES,
            'edit_feedback': feedback,
            'recent_feedback': Feedback.objects.all()[:6]
        })

    except Feedback.DoesNotExist:
        messages.error(request, "Feedback not found.")
        return redirect('feedback')

@login_required
def feedback(request):
    if request.method == "POST":
        try:
            feedback = Feedback(
                user=request.user,
                rating=int(request.POST['rating']),
                comment=request.POST['comment']
            )
            feedback.save()
            messages.success(request, "Thank you for your feedback!")
            return redirect('feedback')
        except Exception as e:
            messages.error(request, f"Error submitting feedback: {str(e)}")
    
    # Get rating choices from model
    rating_choices = Feedback.RATING_CHOICES
    # Get recent feedback, limited to last 6
    recent_feedback = Feedback.objects.all()[:6]
    
    return render(request, "feedback.html", {
        'rating_choices': rating_choices,
        'recent_feedback': recent_feedback
    })

def profile(request):
    if request.method == "POST":
        user = request.user
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        
        # Handle password change
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if current_password and new_password and confirm_password:
            if user.check_password(current_password):
                if new_password == confirm_password:
                    user.set_password(new_password)
                    messages.success(request, "Password updated successfully!")
                else:
                    messages.error(request, "New passwords don't match!")
                    return redirect('profile')
            else:
                messages.error(request, "Current password is incorrect!")
                return redirect('profile')
        
        user.save()
        messages.success(request, "Profile updated successfully!")
        
        if current_password and new_password and confirm_password and new_password == confirm_password:
            auth.login(request, user)
            
        return redirect('profile')
    return render(request, "profile.html")
