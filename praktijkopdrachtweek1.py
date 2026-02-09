# Importeer benodigde modules
import os    # Voor het uitvoeren van systeemcommando's (zoals clear screen)
import subprocess  # Voor het uitvoeren van PowerShell commando's
import ctypes      # Voor het controleren van administrator rechten
import sys         # Voor het afsluiten van het programma
from art import *  # Voor het maken van ASCII art

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def is_admin():
    try:
        # Gebruik Windows API om admin status te checken
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        # Als er een fout optreedt, ga uit van geen admin rechten
        return False
    
def schakel_defender_uit():
    """
    Functie om Windows Defender uit te schakelen.
    Gebruikt Set-MpPreference PowerShell cmdlet.
    Vereist administrator rechten!
    """
    # STAP 1: Controleer of we admin rechten hebben
    if not is_admin():
        print("\n[!] FOUT: Dit script vereist administrator rechten!")
        print("[!] Klik rechts op het script en kies 'Als administrator uitvoeren'")
        sys.exit(1)  # Stop het programma met foutcode 1
    
    # STAP 2: Probeer Defender uit te schakelen
    try:
        print("\n[*] Windows Defender uitschakelen...")
        
        # Gebruik Set-MpPreference om Real-time monitoring uit te zetten
        # -DisableRealtimeMonitoring $true betekent: zet real-time scanning uit
        subprocess.run(
            ['powershell', '-Command', 'Set-MpPreference -DisableRealtimeMonitoring $true'],
            check=True,           # Gooi fout als commando faalt
            capture_output=True   # Vang eventuele foutmeldingen op
        )
        
        # Als we hier komen, is het gelukt
        print("[+] Windows Defender Real-time monitoring uitgeschakeld!")
        input("\nDruk op Enter om terug te gaan naar het menu...")
        clear()
        return True  # Geef True terug = succes
        
    except subprocess.CalledProcessError as e:
        # Deze fout gebeurt als PowerShell het commando niet kon uitvoeren
        print(f"\n[!] Fout bij het uitschakelen van Defender: {e}")
        print("[!] Mogelijk heeft Windows de wijziging geblokkeerd.")
        return False  # Geef False terug = mislukt
        
    except Exception as e:
        # Vang alle andere fouten op
        print(f"\n[!] Onverwachte fout opgetreden: {e}")
        return False

def schakel_defender_in():
    """
    Functie om Windows Defender weer in te schakelen.
    Gebruikt Set-MpPreference PowerShell cmdlet.
    """
    try:
        print("\n[*] Windows Defender inschakelen...")
        
        # Gebruik Set-MpPreference om Real-time monitoring aan te zetten
        # -DisableRealtimeMonitoring $false betekent: zet real-time scanning aan
        subprocess.run(
            ['powershell', '-Command', 'Set-MpPreference -DisableRealtimeMonitoring $false'],
            check=True,           # Gooi fout als commando faalt
            capture_output=True   # Vang eventuele foutmeldingen op
        )
        
        # Als we hier komen, is het gelukt
        print("[+] Windows Defender Real-time monitoring ingeschakeld!")
        input("\nDruk op Enter om terug te gaan naar het menu...")
        clear()
        return True  # Geef True terug = succes
        
    except subprocess.CalledProcessError as e:
        # Deze fout gebeurt als PowerShell het commando niet kon uitvoeren
        print(f"\n[!] Fout bij het inschakelen van Defender: {e}")
        return False  # Geef False terug = mislukt
        
    except Exception as e:
        # Vang alle andere fouten op
        print(f"\n[!] Onverwachte fout opgetreden: {e}")
        return False

def controleer_defender_status():
    try:
        # Print een bericht dat we bezig zijn
        print("\n[*] Windows Defender status controleren...")
        
        # Voer PowerShell commando uit om Defender status op te halen
        # Get-MpPreference haalt alle Defender instellingen op
        result = subprocess.run(
            ['powershell', '-Command', 'Get-MpPreference | Select-Object DisableRealtimeMonitoring'],
            capture_output=True,  # Vang de output op
            text=True,            # Geef output als tekst terug
            check=True            # Gooi een fout als het commando faalt
        )
        
        # Laat de huidige status zien aan de gebruiker
        print("\nHuidige Windows Defender status:")
        print(result.stdout)
        print("False = Defender is ingeschakeld")
        print("True = Defender is uitgeschakeld")
        input("\nDruk op Enter om terug te gaan naar het menu...")
        clear()
        return True  # Geef True terug als alles goed ging
        
    except subprocess.CalledProcessError as e:
        # Deze fout treedt op als PowerShell een fout geeft
        print(f"[!] Fout bij het controleren van de status: {e}")
        return False
        
    except Exception as e:
        # Vang alle andere onverwachte fouten op
        print(f"[!] Onverwachte fout: {e}")
        return False

def main():
    """
    Hoofdfunctie - dit is waar het programma start.
    Toont een menu en verwerkt de keuze van de gebruiker.
    """
    while True:
        # Print een mooie header
        border = "=" * 65
        print(border,'\n')
        Art=text2art("W1ND0WS")
        print(Art)
        Art=text2art("0FF3ND3R")
        print(Art)
        print(border)

        # Toon het menu met opties
        print("\nMenu:")
        print("1. Windows Defender uitschakelen")
        print("2. Windows Defender inschakelen")
        print("3. Status opnieuw controleren")
        print("4. Afsluiten")
        # Probeer de gebruikersinput te verwerken
        try:
            # Vraag de gebruiker om een keuze
            keuze = input("\nMaak een keuze (1-4): ").strip()
            
            # Verwerk de keuze met if/elif statements
            if keuze == "1":
                clear()
                # Optie 1: Defender uitschakelen
                schakel_defender_uit()
                
            elif keuze == "2":
                clear()
                # Optie 2: Defender inschakelen
                schakel_defender_in()
                
            elif keuze == "3":
                clear()
                # Optie 3: Alleen status controleren
                controleer_defender_status()
                
            elif keuze == "4":
                clear()
                # Optie 4: Programma afsluiten
                print("[*] Script wordt afgesloten...")
                break
                
            else:
                # De gebruiker heeft een ongeldige keuze ingevoerd
                print("\n[!] Ongeldige keuze. Probeer opnieuw.")
                
        except KeyboardInterrupt:
            # Als de gebruiker Ctrl+C drukt
            print("\n\n[!] Script onderbroken door gebruiker")
            sys.exit(0)
            
        except Exception as e:
            # Vang alle andere fouten op
            print(f"\n[!] Fout in hoofdmenu: {e}")

# Dit is het startpunt van het programma
# __name__ == "__main__" is alleen True als we dit bestand direct uitvoeren
if __name__ == "__main__":
    clear()
    main()  # Roep de main functie aan