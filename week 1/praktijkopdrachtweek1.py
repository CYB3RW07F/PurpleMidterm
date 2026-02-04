import subprocess # hiermee kunnen we systeemcommando's uitvoeren

print("Dit is de Adminuitschakelaarinator.") # ff de gebruiker laten weten dat die cooked is
command = "Get-MpComputerStatus" # Get-MpComputerStatus is een powershell command dat kijkt wat de status is van windows defender
subprocess.run(["powershell", "-Command", command])