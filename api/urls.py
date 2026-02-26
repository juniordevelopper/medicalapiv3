from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from accounts.views import *
from locations.views import *
from hospitals.views import *
from admins.views import *
from directors.views import *
from doctors.views import *
from receptions.views import *
from bemors.views import *
from navbats.views import *

router = DefaultRouter()
# admin-routes
router.register(r'regions', RegionViewSet, basename='region')
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'hospitals', HospitalViewSet, basename='hospital')
router.register(r'director/manage-receptions', DirectorReceptionManagementViewSet, basename='director-receptions')
router.register(r'director/manage-doctors', DirectorDoctorManagementViewSet, basename='director-doctors')
router.register(r'doctor/queues', DoctorQueueViewSet, basename='doctor-queues')
router.register(r'reception/bookings', ReceptionBookingViewSet, basename='reception-bookings')
router.register(r'patient/my-bookings', PatientBookingViewSet, basename='patient-bookings')

# director-routes

urlpatterns = [
    # Register & Login
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'), # Email & Username login (backend orqali)
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Email Verify
    path('auth/verify-email/<uidb64>/<token>/', VerifyEmailView.as_view(), name='verify_email'),
    
    # Password Reset
    path('auth/password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    
    # Parolni qayta tiklash
    path('auth/password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    # Admin Profile
    path('admin/profile/', AdminProfileView.as_view(), name='admin_profile'),
    
    # Director Profile
    path('director/profile/', DirectorProfileView.as_view(), name='director_profile'),
    
    # Doctor Profile
    path('doctor/profile/', DoctorSelfProfileView.as_view(), name='doctor-self-profile'),
    
    # Reception Profile
    path('reception/profile/', ReceptionSelfProfileView.as_view({'get': 'retrieve', 'patch': 'partial_update'}), name='reception-profile'),
    
    # Bemor Profile
    path('patient/profile/', PatientProfileView.as_view(), name='patient-profile'),

    # 1. Bemor uchun: Hudud bo'yicha shifoxonalar va shifokorlar
    path('patient/hospitals/', HospitalListView.as_view(), name='patient-hospitals'),
    path('patient/doctors/', DoctorListView.as_view(), name='patient-doctors'),

    # 2. Admin va Director uchun: Bo'sh foydalanuvchilar (nomzodlar) ro'yxati
    # Admin shifoxona yaratganda, Director xodim tayinlaganda ishlatadi
    path('staff/candidates/', CandidateUserListView.as_view(), name='user-candidates'),

    # 3. Reception uchun: O'z shifoxonasidagi shifokorlar ro'yxati
    # Bemorni navbatga qo'yayotganida shifokorni tanlash uchun
    path('reception/my-hospital-doctors/', ReceptionDoctorListView.as_view(), name='reception-doctors'),

    # Reception bemorni qidirib topishi uchun endpoint
    path('reception/search-patient/', ReceptionPatientSearchView.as_view(), name='reception-patient-search'),

    # Bemor uchun
    path('patient/delete-request/', PatientDeleteRequestView.as_view(), name='p-delete-req'),
    
    # Admin uchun (ID orqali boshqarish)
    path('admin/handle-delete/<int:pk>/', AdminHandleDeleteRequestView.as_view(), name='a-handle-delete'),

    path('', include(router.urls)),
]
