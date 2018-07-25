
from lackey import *
from Patients import Patients
import sys


USERNAME = "ADTADM"
DEPARTMENT = "SMH Admitting"


def main():
    patients = Patients(13)
    patients.addPatients("patientsData.csv", 1)  # Number specifies how many patients you would like
    login()
    # --------------------------------------
    # Patient Lookup and Navigation to Reg
    # -------------------------------------
    for patient in patients.list:

        createPatient(patient)  # Function that goes to patient station and creates a new patient
        newAdmission(patient)  # Function that hits the admission button and fills out and submits the popup
        addDemographics(patient)
        addPCP(patient)
        addPatientContacts(patient)
        addEmployment(patient)

        click("Admission.png")
        wait("AdmissionsProfilePhoto.png", 30)  # Waits for the Admission page to load
        wait(2)

        addEncounterInfo(patient)
        addHospitalAccount(patient)

        wait(2)
        click("Admit.png")
        if exists("ContinueConfirm.png"):
            click("ContinueConfirm.png")
        wait(1)
        click("X2.png")


def login():
    App.focus("Hyperspace - URMC POC")
    click("UserNameField.png") # Username text field
    type(USERNAME+Key.TAB)
    type("model"+Key.ENTER) # Password
    type(Key.TAB, KeyModifier.SHIFT)
    type(DEPARTMENT+Key.ENTER*3)
    wait(4)
    popup("Please ensure the Epic Theme is set to default \n press ok to proceed")


def createPatient(patient):
    click("PatientStation.png")
    wait(1)
    type(patient["name"] + Key.TAB)
    type(Key.TAB)
    type(patient["sex"] + Key.TAB)
    type(patient["dob"])
    click("FindPatient.png")
    wait(2)
    if exists("GoBack.png"):  # Catches the situation where epic finds similar patient to yours
        click("GoBack.png")
        click("New.png")
        wait(1)
        if exists("New.png"):
            click("New.png")
            wait(1)
            type("1" + Key.ENTER)
        else:
            popup("The patient you are trying to create already exists. \n Change the number in the Patients() call at the top of your script")
            sys.exit("Program ended due to patient already existing")

    else:  # Normal path for creating patients
        click("Continue.png")
        wait(1)
        click("New.png")
    wait(3)


def newAdmission(patient):
    click("NewAdmission.png")
    wait(1)
    type(patient["expectedDate"] + Key.TAB)
    type(patient["unit"] + Key.TAB + Key.ENTER)
    type(patient["patientClass"] + Key.TAB + Key.ENTER)
    type(patient["admittingProvider"] + Key.TAB + Key.ENTER)
    wait(1)
    type(patient["service"])
    click("New.png")


def addDemographics(patient):
    wait("Address.png", 30)
    wait(2)
    click("AddressText.png")
    wait(2)
    type(patient["address"] + Key.TAB)
    type(patient["zip"] + Key.TAB * 2)
    type(patient["homePhone"])
    if exists("maritalStatus.png"):
        click("maritalStatus.png")  # Marital status
    else:
        click("maritalStatusFilled.png")
    type(patient["maritalStatus"] + Key.TAB * 2)
    type(patient["interpreter"] + Key.TAB)
    type(patient["preferredLanguage"] + Key.TAB)
    type(patient["patientRace"] + Key.TAB * 2)
    type(patient["ethnicBackground"] + Key.TAB * 2)
    type(patient["religion"] + Key.ENTER * 2 + Key.TAB)
    type(Key.ENTER)


def addPCP(patient):
    wait(3)  # Patient Care Team
    click("addPCP.png")
    wait(1)
    type(patient["pcp"] + Key.ENTER)
    wait("SearchPCP.png", 30)  # Wait until search is completed
    wait(3)
    type(Key.ENTER)
    wait("Accept.png", 20)
    wait(1)
    type(Key.TAB * 2)
    type("T-2")
    click("Accept.png")
    wait(2)
    click("GrandCentralLabel.png")
    wait(1)


def addPatientContacts(patient):
    click("add.png")
    wait(3)
    type(patient["contactName"] + Key.TAB * 7)
    type(patient["contactRel"] + Key.TAB * 8)
    type(patient["nextKin"] + Key.TAB)
    type(patient["contactPhone"])
    doubleClick("acceptWizard.png")  # accept
    wait(2)  # Needs to wait for the conformation


def addEmployment(patient):
    click("Employer.png")
    type(patient["employer"] + Key.TAB)
    type(patient["employmentStatus"])


def addEncounterInfo(patient):
    click("EncounterInfo.png")
    wait(3)
    type(Key.TAB * 2)
    type(patient["admissionDate"]) # Used to tab to room, but HH and SMH tabbing seems to work differently
    click(Pattern("RoomLabel.png").targetOffset(100, 0))
    if patient["room"] != "n/a":
        type(patient["room"] + Key.TAB)
        type(patient["bed"] + Key.TAB * 4)
    else:
        type(Key.TAB * 3)
    type(patient["WCTPLMVA"] + Key.TAB)
    type(patient["admissionType"] + Key.TAB * 2)
    type(patient["pointOfOrigin"] + Key.TAB )
    click(Pattern("FreeTextDiagnoses.png").targetOffset(0, 25))
    type(patient["freeTextDiagnoses"] + Key.TAB)
    wait(2)
    click("Accept2.png")
    wait(1)
    type(patient["freeTextDiagnoses"])
    if patient["room"] == "n/a":
        popup("Please room the patient once you are finished hit ok to precede")
    click("Next.png")
    click("ReferralText.png")
    type("pcp" + Key.ENTER)
    wait("RecordSelect.png", 30)
    type(Key.ENTER)
    wait(3)

def addHospitalAccount(patient):
    click("Next.png")

    # -------------------------------------
    # Hospital Account
    # -------------------------------------
    if not exists("SelectAccountID.png"):
        click("AddGuarantor.png")
        type(Key.TAB + Key.ENTER)
        wait(2)
        click("CreateNewAccount.png")
        click("Finish.png")

    click("SelectAccountID.png")
    click("CreateNewAccount.png")
    wait(2)
    click("Next.png")
    wait(2)
    click("SelfPay.png")
    click("UseDefault.png")
    wait(1)
    type(Key.ENTER)
    wait(3)

main()
