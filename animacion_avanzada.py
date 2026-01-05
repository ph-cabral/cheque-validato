import os
import time

class AnimacionProceso:
    def __init__(self):
        self.stop_event = None
        self.progreso = 0
        self.mensaje = "Iniciando..."
        
    def actualizar(self, progreso, mensaje=""):
        """Actualizar progreso (0-100) y mensaje"""
        self.progreso = min(progreso, 100)
        if mensaje:
            self.mensaje = mensaje
    
    def correr(self, stop_event):
        """Ejecutar animación"""
        self.stop_event = stop_event
        
        runner = ["  o/", " /| ", " / \\"]
        frame = 0
        
        while not stop_event.is_set():
            os.system("cls" if os.name == "nt" else "clear")
            
            print("\n" * 3)
            
            # Corredor animado
            for line in runner:
                pos = int(self.progreso / 100 * 30)
                print(" " * pos + line)
            
            print("\n")
            
            # Barra de progreso
            bar_length = 40
            filled = int(self.progreso / 100 * bar_length)
            bar = "█" * filled + "░" * (bar_length - filled)
            print(f"[{bar}] {self.progreso:3d}%")
            
            print(f"\n{self.mensaje}")
            
            frame += 1
            time.sleep(0.1)
        
        # Final
        os.system("cls" if os.name == "nt" else "clear")
        print("\n" * 4)
        print("    ✅ ¡TODO LISTO!")
        time.sleep(1)


# Instancia global
animacion = AnimacionProceso()
