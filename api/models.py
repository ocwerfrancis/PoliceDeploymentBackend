import binascii
import os

from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Avg
from model_utils.models import TimeStampedModel
from rest_framework_jwt.settings import api_settings

ACCOUNT_TYPES = (
    ("admin", "Admin"),
    ("in_charge", "In Charge"),
)

# For admin only we shall add another status of Undeployed 
BATTALLION_TYPES = (
    ("battallion_one", "Battallion 1"),
    ("battallion_two", "Battallion 2"),
    ("battallion_three", "Battallion 3"),
    ("battallion_four", "Battallion 4"),
    ("battallion_five", "Battallion 5"),
    ("battallion_six", "Battallion 6"),
    ("all_battallions", "All Battallions"),
)

GENDER_TYPES = (
    ("Male", "Male"),
    ("Female", "Female"),
)

RANK_TYPES = (
    ("AIGP", "AIGP"),
    ("SCP", "SCP"),
    ("CP", "CP"),
    ("ACP", "ACP"),
    ("SSP", "SSP"),
    ("SP", "SP"),
    ("ASP", "ASP"),
    ("IP", "IP"),
    ("AIP", "AIP"),
    ("SGT", "SGT"),
    ("CPL", "CPL"),
    ("PC", "PC"),
    ("SPC", "SPC"),
)

BATTALLION_TWO_DEPARTMENT_TYPES = (
    ("Embassy", "Embassy"),
    ("Consulate", "Consulate"),
    ("High Commission", "High Commission"),
    ("Other Diplomats", "Other Diplomats"),
    ("Administration", "Administration")
)

BATTALLION_FOUR_DEPARTMENT_TYPES = (
    ("Body guard", "Body guard"),
    ("Crew Commander", "Crew Commander"),
    ("Crew", "Crew")
)

BATTALLION_SIX_DEPARTMENT_TYPES = (
    ("Administration", "Administration"),
    ("Ministry for Presidency", "Ministry for Presidency"),
    ("Ministry of Science, Technology and Innovation", "Ministry of Science, Technology and Innovation"),
    ("Ministry of Water and Environment", "Ministry of Water and Environment"),
    ("Ministry for East African Affairs", "Ministry for East African Affairs"),
    ("Ministry of Internal Affairs", "Ministry of Internal Affairs"),
    ("Ministry of Works and Transport", "Ministry of Works and Transport"),
    ("Office of the Prime Minister", "Office of the Prime Minister"),
    ("Ministry of Finance", "Ministry of Finance"),
    ("Ministry of Health", "Ministry of Health"),
    ("Ministry of Gender, Labor and Social Development", "Ministry of Gender, Labor and Social Development"),
    ("Ministry of Lands, Housing and Urban Development", "Ministry of Lands, Housing and Urban Development"),
    ("Ministry for Kampala", "Ministry for Kampala"),
    ("Ministry of ICT and National Guidance", "Ministry of ICT and National Guidance"),
    ("Ministry of Justice and Constitutional Affairs", "Ministry of Justice and Constitutional Affairs"),
    ("Ministry of Local Government", "Ministry of Local Government"),
    ("Ministry for Foreign Affairs", "Ministry for Foreign Affairs"),
    ("Ministry of Energy", "Ministry of Energy"),
    ("Ministry of Tourism Wildlife and Antiquities", "Ministry of Tourism Wildlife and Antiquities"),
    ("Ministry of Trade Industry and Cooperatives", "Ministry of Trade Industry and Cooperatives"),
    ("Ministry of Education", "Ministry of Education"),
    ("Ministry of Public Service", "Ministry of Public Service"),
    ("Ministry of Agriculture Animal Industry and Fisheries", "Ministry of Agriculture Animal Industry and Fisheries"),
    ("Education Institution", "Education Institution"),
    ("Religious Leaders", "Religious Leaders"),
    ("Senior Citizens", "Senior Citizens"),
    ("Political Leaders", "Political Leaders"),
    ("Members of Parliament", "Members of Parliament"),
    ("Business Parks", "Business Parks"),
    ("UIRI", "UIRI"),
    ("New Vision", "New Vision"),
    ("UBC", "UBC")
)  


BATTALLION_FIVE_DEPARTMENT_TYPES = (
    ("UCC", "UCC"),
    ("EC", "EC"),
    ("IRA", "IRA"),
    ("URA", "URA"),
    ("UNRA", "UNRA"),
    ("NPA", "NPA"),
    ("ULC", "ULC"),
    ("PSC", "PSC"),
    ("NSSF", "NSSF"),
    ("KCCA", "KCCA"),
    ("SENIOR CITIZENS", "SENIOR CITIZENS"),
    ("JSC", "JSC"),
    ("EOC", "EOC"),
    ("Administration", "Administration")
)

BATTALLION_THREE_DEPARTMENT_TYPES = (
    ("Anti-corruption and War Crime division", "Anti-corruption and War Crime division"),
    ("Buganda Road Court", "Buganda Road Court"),
    ("Commercial Court", "Commercial Court"),
    ("Supreme Court", "Supreme Court"),
    ("High Court Offices Kampala", "High Court Offices Kampala"),
    ("High Court Residence", "High Court Residence"),
    ("Family Court Division Makindye", "Family Court Division Makindye"),
    ("Court of Appeal", "Court of Appeal"),
    ("Residence of Justice of Court Appeal", "Residence of Justice of Court Appeal"),
    ("DPP Office", "DPP Office"),
    ("IGG", "IGG"),
    ("AOG", "AOG"),
    ("Police Establishment", "Police Establishment")
)

BATTALLION_ONE_DEPARTMENT_TYPES = (
    ("UN Agencies", "UN Agencies"),
    ("Administration", "Administration"),
    ("Drivers", "Drivers")
)

TITLE_TYPES = (
    ("Commandant", "Commandant"),
    ("Deputy commandant", "Deputy commandant"),
    ("Staff officer", "Staff officer"),
    ("Head of operations", "Head of operations"),
    ("Head of armoury", "Head of armoury"),
    ("Supervisor", "Supervisor"),
    ("In Charge", "In Charge"),
    ("2nd In Charge", "2nd In Charge"),
    ("Driver", "Driver"),
    ("N/A", "N/A")
)

# For admin only we shall add another status of Undeployed

STATUS_TYPES = (
    ("Active", "Active"),
    ("Absent", "Absent(AWOL)"),
    ("Transfered", "Transfered"),
    ("Sick", "Sick"),
    ("Dead", "Dead"),
    ("Suspended", "Suspended"),
    ("Dismissed", "Dismissed"),
    ("In court", "In court"),
    ("Deserted", "Deserted"),
    ("On course", "On course"),
    ("On mission", "On mission"),
    ("On leave", "On leave"),
    ("Interdiction", "Interdiction"),
    ("Criminal court", "Criminal court(remand / bail)"),
    ("Displinary court", "Displinary court"),
    ("Special duty", "Special duty"),
    ("On police course", "On police course"),
    ("Undeployed", "Undeployed")
)


SHIFT_TYPES = (
    ("Day", "Day"),
    ("Night", "Night"),
    ("Long night", "Long night"),
    ("None", "None(not applicable)"),
)

ARMED_TYPES = (
    ("Yes", "Yes"),
    ("No", "No"),
)

LEAVE_TYPES = (
    ("Pass leave", "Pass leave"),
    ("Maternity leave", "Maternity leave"),
    ("Sick leave", "Sick leave"),
    ("Study leave", "Study leave"),
    ("Annual leave", "Annual leave"),
    ("Not on leave", "Not on leave"),
)

EDUCATION_TYPES = (
    ("PLE", "PLE"),
    ("UCE", "UCE"),
    ("UACE", "UACE"),
    ("Diploma", "DIPLOMA"),
    ("Post Graduate Diploma", "POST GRADUATE DIPLOMA"),
    ("Bachelors", "BACHELORS"),
    ("Masters", "MASTERS"),
    ("Doctorate", "DOCTORATE(PhD)"),
    ("Other", "OTHER")
)

# Used in Battalion 3
DEPARTMENT_TYPES = (
    # Battalion 3
    ("Anti-corruption and War Crime division", "Anti-corruption and War Crime division"),
    ("Buganda Road Court", "Buganda Road Court"),
    ("Commercial court", "Commercial court"),
    ("Supreme Court", "Supreme Court"),
    ("High Court Offices Kampala", "High Court Offices Kampala"),
    ("High Court Residence", "High Court Residence"),
    ("Family Court Division Makindye", "Family Court Division Makindye"),
    ("Court of Appeal", "Court of Appeal"),
    ("Residence of Justice of Court Appeal", "Residence of Justice of Court Appeal"),
    ("DPP Office", "DPP Office"),
    ("IGG", "IGG"),
    ("AOG", "AOG"),
    ("Police Establishment", "Police Establishment"),

    # Battalion 4
    ("Body guard", "Body guard"),
    ("Crew Commander", "Crew Commander"),
    ("Crew", "Crew"),

    # Battalion 5
    ("UCC", "UCC"),
    ("EC", "EC"),
    ("IRA", "IRA"),
    ("URA", "URA"),
    ("UNRA", "UNRA"),
    ("NPA", "NPA"),
    ("ULC", "ULC"),
    ("PSC", "PSC"),
    ("NSSF", "NSSF"),
    ("KCCA", "KCCA"),
    ("SENIOR CITIZENS", "SENIOR CITIZENS"),
    ("JSC", "JSC"),
    ("EOC", "EOC"),
    ("Administration", "Administration"),

    # Battalion 6 
    ("Administration", "Administration"),
    ("Ministry for Presidency", "Ministry for Presidency"),
    ("Ministry of Science, Technology and Innovation", "Ministry of Science, Technology and Innovation"),
    ("Ministry of Water and Environment", "Ministry of Water and Environment"),
    ("Ministry for East African Affairs", "Ministry for East African Affairs"),
    ("Ministry of Internal Affairs", "Ministry of Internal Affairs"),
    ("Ministry of Works and Transport", "Ministry of Works and Transport"),
    ("Office of the Prime Minister", "Office of the Prime Minister"),
    ("Ministry of Finance", "Ministry of Finance"),
    ("Ministry of Health", "Ministry of Health"),
    ("Ministry of Gender, Labor and Social Development", "Ministry of Gender, Labor and Social Development"),
    ("Ministry of Lands, Housing and Urban Development", "Ministry of Lands, Housing and Urban Development"),
    ("Ministry for Kampala", "Ministry for Kampala"),
    ("Ministry of ICT and National Guidance", "Ministry of ICT and National Guidance"),
    ("Ministry of Justice and Constitutional Affairs", "Ministry of Justice and Constitutional Affairs"),
    ("Ministry of Local Government", "Ministry of Local Government"),
    ("Ministry for Foreign Affairs", "Ministry for Foreign Affairs"),
    ("Ministry of Energy", "Ministry of Energy"),
    ("Ministry of Tourism Wildlife and Antiquities", "Ministry of Tourism Wildlife and Antiquities"),
    ("Ministry of Trade Industry and Cooperatives", "Ministry of Trade Industry and Cooperatives"),
    ("Ministry of Education", "Ministry of Education"),
    ("Ministry of Public Service", "Ministry of Public Service"),
    ("Ministry of Agriculture Animal Industry and Fisheries", "Ministry of Agriculture Animal Industry and Fisheries"),
    ("Education Institution", "Education Institution"),
    ("Religious Leaders", "Religious Leaders"),
    ("Senior Citizens", "Senior Citizens"),
    ("Political Leaders", "Political Leaders"),
    ("Members of Parliament", "Members of Parliament"),
    ("Business Parks", "Business Parks"),
    ("UIRI", "UIRI"),
    ("New Vision", "New Vision"),
    ("UBC", "UBC")

)












# Used in Battalion 1
SECTION_TYPES = (
    ("UNDP Head Office", "UNDP Head Office"),
    ("UN Women", "UN Women"),
    ("IFAD office", "IFAD office"),
    ("UNDSS office", "UNDSS office"),
    ("WFP", "WFP"),

    ("WHO", "WHO"),
    ("World bank", "World bank"),
    ("FAO office", "FAO office"),
    ("SPGS office", "SPGS office"),
    ("UNHCR new offices", "UNHCR new offices"),

    ("UNHCR Extension", "UNHCR Extension"),
    ("I.C.C field offices", "IFAD office"),
    ("UNFPA", "UNFPA"),
    ("I.O.M head office", "I.O.M head office"),
    ("I.O.M Transit Centre", "I.O.M Transit Centre"),

    ("UNOHCHR office", "UNOHCHR office"),
    ("EADB", "EADB"),
    ("UNDP", "UNDP"),
    ("UNDP Gulu", "UNDP Gulu"),
    ("UNDP Moroto", "UNDP Moroto"),

    ("UNICEF office", "UNICEF office"),
    ("UNDP Arua", "UNDP Arua"),
)

BATTALLION_ACCESS_TYPES = (
    ("battallion_one", "Battallion 1"),
    ("battallion_two", "Battallion 2"),
    ("battallion_three", "Battallion 3"),
    ("battallion_four", "Battallion 4"),
    ("battallion_five", "Battallion 5"),
    ("battallion_six", "Battallion 6"),
)

class UserManager(BaseUserManager):
    def _create_user(self, username, password, is_staff, is_superuser, **extra_fields):
        if not username:
            raise ValueError("The given username must be set")
        # email = self.normalize_email(email)
        is_active = extra_fields.pop("is_active", True)
        user = self.model(
            username=username,
            is_staff=is_staff,
            is_active=is_active,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        is_staff = extra_fields.pop("is_staff", False)
        return self._create_user(username, password, is_staff, False, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        return self._create_user(username, password, True, True, **extra_fields)


class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True) # db_index=True
    email = models.EmailField(
        "email address", max_length=255, unique=False, blank=True, null=True
    )
    first_name = models.CharField(max_length=32, blank=True, null=True)
    last_name = models.CharField(max_length=32, blank=True, null=True)

    account_type = models.CharField(max_length=32, choices=ACCOUNT_TYPES)
    battallion = models.CharField(max_length=32, choices=BATTALLION_TYPES)
    top_level_incharge = models.BooleanField(default=False) # Has access to the entire Battallion
    lower_level_incharge = models.BooleanField(default=False, help_text="Please don't forget to assign this user a Departement or Section if he or she is an In Charge ") # Has access to either Department or section in the Battallion they belong to
    department = models.CharField(max_length=150, choices=DEPARTMENT_TYPES, blank=True, null=True) # Choice field
    section = models.CharField(max_length=150, choices=SECTION_TYPES, blank=True, null=True) # Very Long choise field

    phone_number = models.CharField(max_length=50, blank=True) # null=True
    admin_request_access = models.BooleanField("admin request access", default=False, blank=True, null=True)
    admin_request_battalion = models.CharField(max_length=32, choices=BATTALLION_ACCESS_TYPES, blank=True, null=True)
    is_staff = models.BooleanField("staff status", default=False)
    is_active = models.BooleanField("active", default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "username" # Making username the required field
    REQUIRED_FIELDS = []

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(self)
        token = jwt_encode_handler(payload)

        return token

def generate_password_reset_code():
    return binascii.hexlify(os.urandom(20)).decode("utf-8")


# BATTALLION 6 TABLE MODEL 
class Battallion_six(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    nin = models.CharField(max_length=32)
    ipps = models.CharField(max_length=32)
    file_number = models.CharField(max_length=32, unique=True) #, blank=True, null=True
    battallion = models.CharField(max_length=32)
    account_number = models.CharField(max_length=32, blank=True, null=True)
    contact = models.CharField(max_length=32, blank=True, null=True)
    tin_number = models.CharField(max_length=32, blank=True, null=True)
    sex = models.CharField(max_length=32, choices=GENDER_TYPES)
    rank = models.CharField(max_length=32, choices=RANK_TYPES)
    education_level = models.CharField(max_length=32, choices=EDUCATION_TYPES)
    other_education_level = models.CharField(max_length=32, blank=True, null=True) # Gives us an extra field incase of OTHER
    bank = models.CharField(max_length=32, blank=True, null=True)
    branch = models.CharField(max_length=32, blank=True, null=True)
    department = models.CharField(max_length=150, choices=BATTALLION_SIX_DEPARTMENT_TYPES)
    title = models.CharField(max_length=32, choices=TITLE_TYPES)
    status = models.CharField(max_length=32, choices=STATUS_TYPES)
    shift = models.CharField(max_length=32, choices=SHIFT_TYPES)
    date_of_enlistment = models.DateField(blank=True, null=True)
    date_of_transfer = models.DateField(blank=True, null=True)
    date_of_promotion = models.DateField(blank=True, null=True)
    date_of_birth = models.DateField(blank=False, null=False)
    armed = models.CharField(max_length=32, choices=ARMED_TYPES)
    section = models.CharField(max_length=150)
    location = models.CharField(max_length=150)
    on_leave = models.CharField(max_length=32, choices=LEAVE_TYPES)
    notify_leave = models.BooleanField(default=False)
    notify_special_duty = models.BooleanField(default=False)
    special_duty_start_date = models.DateField(blank=True, null=True) 
    special_duty_end_date = models.DateField(blank=True, null=True) 
    leave_start_date = models.DateField(blank=True, null=True) # Gives us an extra field 
    leave_end_date = models.DateField(blank=True, null=True) # Gives us an extra field 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Battallion Six"
        verbose_name_plural = "Battallion Six"

    def __str__(self):
        return '{}, {}'.format(self.first_name, self.file_number)


# BATTALLION 5 TABLE MODEL 
class Battallion_five(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    nin = models.CharField(max_length=32)
    ipps = models.CharField(max_length=32)
    file_number = models.CharField(max_length=32, unique=True) #, blank=True, null=True
    battallion = models.CharField(max_length=32)
    account_number = models.CharField(max_length=32, blank=True, null=True)
    contact = models.CharField(max_length=32, blank=True, null=True)
    tin_number = models.CharField(max_length=32, blank=True, null=True)
    sex = models.CharField(max_length=32, choices=GENDER_TYPES)
    rank = models.CharField(max_length=32, choices=RANK_TYPES)
    education_level = models.CharField(max_length=32, choices=EDUCATION_TYPES)
    other_education_level = models.CharField(max_length=32, blank=True, null=True) # Gives us an extra field incase of OTHER
    bank = models.CharField(max_length=32, blank=True, null=True)
    branch = models.CharField(max_length=32, blank=True, null=True)
    department = models.CharField(max_length=150, choices=BATTALLION_FIVE_DEPARTMENT_TYPES)
    title = models.CharField(max_length=32, choices=TITLE_TYPES)
    status = models.CharField(max_length=32, choices=STATUS_TYPES)
    shift = models.CharField(max_length=32, choices=SHIFT_TYPES)
    date_of_enlistment = models.DateField(blank=True, null=True)
    date_of_transfer = models.DateField(blank=True, null=True)
    date_of_promotion = models.DateField(blank=True, null=True)
    date_of_birth = models.DateField(blank=False, null=False)
    armed = models.CharField(max_length=32, choices=ARMED_TYPES)
    section = models.CharField(max_length=150)
    location = models.CharField(max_length=150)
    on_leave = models.CharField(max_length=32, choices=LEAVE_TYPES)
    notify_leave = models.BooleanField(default=False)
    notify_special_duty = models.BooleanField(default=False)
    special_duty_start_date = models.DateField(blank=True, null=True) 
    special_duty_end_date = models.DateField(blank=True, null=True) 
    leave_start_date = models.DateField(blank=True, null=True) # Gives us an extra field 
    leave_end_date = models.DateField(blank=True, null=True) # Gives us an extra field 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Battallion Five"
        verbose_name_plural = "Battallion Five"

    def __str__(self):
        return '{}, {}'.format(self.first_name, self.file_number)

# BATTALLION 4 TABLE MODEL 
class Battallion_four(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    nin = models.CharField(max_length=32)
    ipps = models.CharField(max_length=32)
    file_number = models.CharField(max_length=32, unique=True) #, blank=True, null=True
    battallion = models.CharField(max_length=32)
    account_number = models.CharField(max_length=32, blank=True, null=True)
    contact = models.CharField(max_length=32, blank=True, null=True)
    tin_number = models.CharField(max_length=32, blank=True, null=True)
    sex = models.CharField(max_length=32, choices=GENDER_TYPES)
    rank = models.CharField(max_length=32, choices=RANK_TYPES)
    education_level = models.CharField(max_length=32, choices=EDUCATION_TYPES)
    other_education_level = models.CharField(max_length=32, blank=True, null=True) # Gives us an extra field incase of OTHER
    bank = models.CharField(max_length=32, blank=True, null=True)
    branch = models.CharField(max_length=32, blank=True, null=True)
    department = models.CharField(max_length=150, choices=BATTALLION_FOUR_DEPARTMENT_TYPES)
    title = models.CharField(max_length=32, choices=TITLE_TYPES)
    status = models.CharField(max_length=32, choices=STATUS_TYPES)
    shift = models.CharField(max_length=32, choices=SHIFT_TYPES)
    date_of_enlistment = models.DateField(blank=True, null=True)
    date_of_transfer = models.DateField(blank=True, null=True)
    date_of_promotion = models.DateField(blank=True, null=True)
    date_of_birth = models.DateField(blank=False, null=False)
    armed = models.CharField(max_length=32, choices=ARMED_TYPES)
    section = models.CharField(max_length=150)
    location = models.CharField(max_length=150)
    on_leave = models.CharField(max_length=32, choices=LEAVE_TYPES)
    notify_leave = models.BooleanField(default=False)
    notify_special_duty = models.BooleanField(default=False)
    special_duty_start_date = models.DateField(blank=True, null=True) 
    special_duty_end_date = models.DateField(blank=True, null=True) 
    leave_start_date = models.DateField(blank=True, null=True) # Gives us an extra field 
    leave_end_date = models.DateField(blank=True, null=True) # Gives us an extra field 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Battallion Four"
        verbose_name_plural = "Battallion Four"

    def __str__(self):
        return '{}, {}'.format(self.first_name, self.file_number)

# BATTALLION 3 TABLE MODEL 
class Battallion_three(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    nin = models.CharField(max_length=32)
    ipps = models.CharField(max_length=32)
    file_number = models.CharField(max_length=32, unique=True) #, blank=True, null=True
    battallion = models.CharField(max_length=32)
    account_number = models.CharField(max_length=32, blank=True, null=True)
    contact = models.CharField(max_length=32, blank=True, null=True)
    tin_number = models.CharField(max_length=32, blank=True, null=True)
    sex = models.CharField(max_length=32, choices=GENDER_TYPES)
    rank = models.CharField(max_length=32, choices=RANK_TYPES)
    education_level = models.CharField(max_length=32, choices=EDUCATION_TYPES)
    other_education_level = models.CharField(max_length=32, blank=True, null=True) # Gives us an extra field incase of OTHER
    bank = models.CharField(max_length=32, blank=True, null=True)
    branch = models.CharField(max_length=32, blank=True, null=True)
    department = models.CharField(max_length=150, choices=BATTALLION_THREE_DEPARTMENT_TYPES)
    title = models.CharField(max_length=32, choices=TITLE_TYPES)
    status = models.CharField(max_length=32, choices=STATUS_TYPES)
    shift = models.CharField(max_length=32, choices=SHIFT_TYPES)
    date_of_enlistment = models.DateField(blank=True, null=True)
    date_of_transfer = models.DateField(blank=True, null=True)
    date_of_promotion = models.DateField(blank=True, null=True)
    date_of_birth = models.DateField(blank=False, null=False)
    armed = models.CharField(max_length=32, choices=ARMED_TYPES)
    section = models.CharField(max_length=150)
    location = models.CharField(max_length=150)
    on_leave = models.CharField(max_length=32, choices=LEAVE_TYPES)
    notify_leave = models.BooleanField(default=False)
    notify_special_duty = models.BooleanField(default=False)
    special_duty_start_date = models.DateField(blank=True, null=True) 
    special_duty_end_date = models.DateField(blank=True, null=True) 
    leave_start_date = models.DateField(blank=True, null=True) # Gives us an extra field 
    leave_end_date = models.DateField(blank=True, null=True) # Gives us an extra field 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Battallion Three"
        verbose_name_plural = "Battallion Three"

    def __str__(self):
        return '{}, {}'.format(self.first_name, self.file_number)

# BATTALLION 2 TABLE MODEL 
class Battallion_two(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    nin = models.CharField(max_length=32)
    ipps = models.CharField(max_length=32)
    file_number = models.CharField(max_length=32, unique=True) #, blank=True, null=True
    battallion = models.CharField(max_length=32)
    account_number = models.CharField(max_length=32, blank=True, null=True)
    contact = models.CharField(max_length=32, blank=True, null=True)
    tin_number = models.CharField(max_length=32, blank=True, null=True)
    sex = models.CharField(max_length=32, choices=GENDER_TYPES)
    rank = models.CharField(max_length=32, choices=RANK_TYPES)
    education_level = models.CharField(max_length=32, choices=EDUCATION_TYPES)
    other_education_level = models.CharField(max_length=32, blank=True, null=True) # Gives us an extra field incase of OTHER
    bank = models.CharField(max_length=32, blank=True, null=True)
    branch = models.CharField(max_length=32, blank=True, null=True)
    department = models.CharField(max_length=32, choices=BATTALLION_TWO_DEPARTMENT_TYPES)
    title = models.CharField(max_length=32, choices=TITLE_TYPES)
    status = models.CharField(max_length=32, choices=STATUS_TYPES)
    shift = models.CharField(max_length=32, choices=SHIFT_TYPES)
    date_of_enlistment = models.DateField(blank=True, null=True)
    date_of_transfer = models.DateField(blank=True, null=True)
    date_of_promotion = models.DateField(blank=True, null=True)
    date_of_birth = models.DateField(blank=False, null=False)
    armed = models.CharField(max_length=32, choices=ARMED_TYPES)
    section = models.CharField(max_length=150)
    location = models.CharField(max_length=150)
    on_leave = models.CharField(max_length=32, choices=LEAVE_TYPES)
    notify_leave = models.BooleanField(default=False)
    notify_special_duty = models.BooleanField(default=False)
    special_duty_start_date = models.DateField(blank=True, null=True) 
    special_duty_end_date = models.DateField(blank=True, null=True) 
    leave_start_date = models.DateField(blank=True, null=True) # Gives us an extra field 
    leave_end_date = models.DateField(blank=True, null=True) # Gives us an extra field 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Battallion Two"
        verbose_name_plural = "Battallion Two"

    def __str__(self):
        return '{}, {}'.format(self.first_name, self.file_number)


# BATTALLION 1 TABLE MODEL 
class Battallion_one(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    nin = models.CharField(max_length=32)
    ipps = models.CharField(max_length=32)
    file_number = models.CharField(max_length=32, unique=True) #, blank=True, null=True
    battallion = models.CharField(max_length=32)
    account_number = models.CharField(max_length=32, blank=True, null=True)
    contact = models.CharField(max_length=32, blank=True, null=True)
    tin_number = models.CharField(max_length=32, blank=True, null=True)
    sex = models.CharField(max_length=32, choices=GENDER_TYPES)
    rank = models.CharField(max_length=32, choices=RANK_TYPES)
    education_level = models.CharField(max_length=32, choices=EDUCATION_TYPES)
    other_education_level = models.CharField(max_length=32, blank=True, null=True) # Gives us an extra field incase of OTHER
    bank = models.CharField(max_length=32, blank=True, null=True)
    branch = models.CharField(max_length=32, blank=True, null=True)
    title = models.CharField(max_length=32, choices=TITLE_TYPES)
    status = models.CharField(max_length=32, choices=STATUS_TYPES)
    shift = models.CharField(max_length=32, choices=SHIFT_TYPES)
    date_of_enlistment = models.DateField(blank=True, null=True)
    date_of_transfer = models.DateField(blank=True, null=True)
    date_of_promotion = models.DateField(blank=True, null=True)
    date_of_birth = models.DateField(blank=False, null=False)
    armed = models.CharField(max_length=32, choices=ARMED_TYPES)
    section = models.CharField(max_length=150)
    location = models.CharField(max_length=150)
    on_leave = models.CharField(max_length=32, choices=LEAVE_TYPES)
    notify_leave = models.BooleanField(default=False)
    notify_special_duty = models.BooleanField(default=False)
    special_duty_start_date = models.DateField(blank=True, null=True) 
    special_duty_end_date = models.DateField(blank=True, null=True) 
    leave_start_date = models.DateField(blank=True, null=True) # Gives us an extra field 
    leave_end_date = models.DateField(blank=True, null=True) # Gives us an extra field 

    department = models.CharField(max_length=32, choices=BATTALLION_ONE_DEPARTMENT_TYPES)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Battallion One"
        verbose_name_plural = "Battallion One"

    def __str__(self):
        return '{}, {}'.format(self.first_name, self.file_number)


class Deleted_Employee(models.Model):
    reason = models.CharField(max_length=200)
    deletor_name = models.CharField(max_length=32)
    deletor_file_number = models.CharField(max_length=32)
    deleted_name = models.CharField(max_length=32)
    deleted_file_number = models.CharField(max_length=32)
    battalion = models.CharField(max_length=32, default=None)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Deleted Employee"
        verbose_name_plural = "Deleted Employees"

    def __str__(self):
        return '{}, {}'.format(self.deletor_name, self.deleted_name)