

class Patients:
    def __init__(self, pNum):
        self.list = []
        self.PATIENT_NUM = pNum
        return


    def addPatients(self, pathToCSV, numOfPatients): # Reads in the csv of the data table from excel
        # Change This here
        PROJECT_NAME = "InpatientCreation"

        file = open(pathToCSV, 'r')
        lines = file.readlines()# Reads each line of the csv in as a string
        keys = lines[0].strip().split(',') # Takes the first row of the csv (the title bar) and sets that as the keys for the dictionary
        counter = 0

        # Reads in the data from excel then adds name from my name generation function
        for line in lines[1:]:
            data = line.strip().split(',') # Spits the line into a list of strings (each string being a specific cell of data)
            patient = {} # Each Row dictionary is a single patient will all of their information
            for i in range(len(data)): # For each cell, set the key of the item as the title of that column
                patient[keys[i]] = data[i]
            self.list.append(patient) # Adds each of the rows (patients) to one big list
            if patient["name"] == "n/a":
                patient["name"] = self.int_to_en(self.PATIENT_NUM)+","+PROJECT_NAME
            self.PATIENT_NUM += 1
            counter += 1
            if counter >= numOfPatients:
                break

        # Copy data of the last patient over and over to create a bunch of patients
        if counter < numOfPatients:
            for i in range(numOfPatients - counter):

                patient = self.list[-1].copy()
                patient["name"] = self.int_to_en(self.PATIENT_NUM) + ",ATP"
                patient["ssn"] = (9 - len(str(self.PATIENT_NUM))) * "5" + str(self.PATIENT_NUM)
                self.list.append(patient)
                self.PATIENT_NUM +=1


        # Fixing the missing commas.  If you insert a field that needs a comma add it in this for loop
        for patient in self.list:
            # ADD ANY FIELD THAT NEEDS A COMMA HERE
            patient["admittingProvider"] = patient["admittingProvider"].replace(" ",",",1)
            patient["pcp"] = patient["pcp"].replace(" ", ",",1)
            patient["contactName"] = patient["contactName"].replace(" ", ",",1)
            patient["name"] = patient["name"].replace(" ",",",1)



    def int_to_en(self, num):
        d = {0: 'Zero', 1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five',
             6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten',
             11: 'Eleven', 12: 'Twelve', 13: 'Thirteen', 14: 'Fourteen',
             15: 'Fifteen', 16: 'Sixteen', 17: 'Seventeen', 18: 'Eighteen',
             19: 'Nineteen', 20: 'Twenty',
             30: 'Thirty', 40: 'Forty', 50: 'Fifty', 60: 'Sixty',
             70: 'Seventy', 80: 'Eighty', 90: 'Ninety'}
        k = 1000
        m = k * 1000
        b = m * 1000
        t = b * 1000

        if num < 20:
            return d[num]

        if num < 100:
            if num % 10 == 0:
                return d[num]
            else:
                return d[num // 10 * 10] + '' + d[num % 10]

        if num < k:
            if num % 100 == 0:
                return d[num // 100] + 'Hundred'
            else:
                return d[num // 100] + 'HundredAnd' + self.int_to_en(num % 100)

        if num < m:
            if num % k == 0:
                return self.int_to_en(num // k) + 'Thousand'
            else:
                return self.int_to_en(num // k) + 'Thousand' + self.int_to_en(num % k)

        if num < b:
            if (num % m) == 0:
                return self.int_to_en(num // m) + 'Million'
            else:
                return self.int_to_en(num // m) + 'Million' + self.int_to_en(num % m)

        if num < t:
            if (num % b) == 0:
                return self.int_to_en(num // b) + 'Billion'
            else:
                return self.int_to_en(num // b) + 'Billion, ' + self.int_to_en(num % b)

        if num % t == 0:
            return self.int_to_en(num // t) + 'Trillion'
        else:
            return self.int_to_en(num // t) + 'Trillion, ' + self.int_to_en(num % t)

