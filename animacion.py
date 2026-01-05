import os
import time
import itertools

def correr_animacion(stop_event):
    """
    Animación que alterna entre:
    1. Monito bailando solo
    2. Transición (aparece segundo monito)
    3. Monitos enfrentados bailando
    4. Transición (desaparece segundo monito)
    5. Vuelta al inicio
    """
    
    FPS = 10
    
    # ========================================
    # ESTADO 1: Monito bailando solo
    # ========================================
    frames_solo = [
        ["  \\o/", "   | ", "  / \\"],
        ["   o", "  /|\\ ", "  / \\"],
        ["  \\o/ ", "   | ", "  / \\"],
        ["   o ", "  /|\\", "  / \\"],
    ]
    
    # ========================================
    # TRANSICIÓN: Aparece el segundo monito
    # ========================================
    # frames_transicion_entrada = [
    #     ["  \\o/    ", "   |      ", "  / \\    "],           # Solo primero
    #     ["  \\o/  \\", "   |    |", "  / \\  /"],            # Aparece brazo
    #     ["  \\o/  \\o", "   |    |\\", "  / \\  /|"],        # Aparece medio
    #     ["  \\o/  \\o ", "   |    |\\ ", "  / \\  /| "],     # Casi completo
    # ]
    frames_transicion_entrada = [
    ["  \\o/                  ", "   |                    ", "  / \\                  "],
    ["  \\o/              \\o ", "   |                |\\ ", "  / \\              /| "],
    ["  \\o/          \\o     ", "   |            |\\     ", "  / \\          /|     "],
    ["  \\o/      \\o         ", "   |        |\\         ", "  / \\      /|         "],
    ["  \\o/  \\o             ", "   |    |\\             ", "  / \\  /|             "],
]

    
    # ========================================
    # ESTADO 2: Monitos enfrentados bailando
    # ========================================
    frames_enfrentados = [
        ["  o/     \\o ", "  /|       |\\", "   |\\     /| "],
        ["   o/   \\o  ", "   /|     |\\", "    |\\   /|  "],
        ["    o/ \\o   ", "    /|  |\\", "     |\\/|    "],
        ["   o/   \\o  ", "   /|     |\\", "    |\\   /|  "],
    ]
    
    # ========================================
    # TRANSICIÓN: Desaparece el segundo monito
    # ========================================
    frames_transicion_salida = [
        ["  \\o/  \\o ", "   |    |\\ ", "  / \\  /| "],     # Ambos completos
        ["  \\o/  \\o", "   |    |\\", "  / \\  /|"],        # Empieza a irse
        ["  \\o/  \\", "   |    |", "  / \\  /"],            # Solo brazo
        ["  \\o/    ", "   |      ", "  / \\    "],           # Solo primero
    ]
    
    # ========================================
    # CONFIGURACIÓN DE CICLOS
    # ========================================
    ciclos_por_estado = 3  # Cuántos ciclos completos antes de cambiar
    
    # Spinner simple
    spinner = itertools.cycle(['|', '/', '-', '\\'])
    
    frame_idx = 0
    contador_ciclos = 0
    estado_actual = 0  # 0=solo, 1=transición_entrada, 2=enfrentados, 3=transición_salida
    
    # Mapeo de estados a frames
    estados = [
        frames_solo,
        frames_transicion_entrada,
        frames_enfrentados,
        frames_transicion_salida
    ]
    
    frames_actuales = frames_solo
    
    # ========================================
    # LOOP PRINCIPAL
    # ========================================
    while not stop_event.is_set():
        os.system("cls" if os.name == "nt" else "clear")
        
        print("\n" * 3)
        print("  🏃 Procesando cheques...")
        print()
        
        # Mostrar frame actual
        current_frame = frames_actuales[frame_idx % len(frames_actuales)]
        for line in current_frame:
            print("    " + line)
        
        print()
        print(f"    Trabajando... {next(spinner)}")
        
        # Avanzar frame
        frame_idx += 1
        
        # Si completó un ciclo completo de la animación actual
        if frame_idx >= len(frames_actuales):
            frame_idx = 0
            
            # Solo contar ciclos en estados principales (no en transiciones)
            if estado_actual in [0, 2]:  # solo o enfrentados
                contador_ciclos += 1
                
                # Cambiar de estado después de N ciclos
                if contador_ciclos >= ciclos_por_estado:
                    contador_ciclos = 0
                    estado_actual = (estado_actual + 1) % len(estados)
                    frames_actuales = estados[estado_actual]
            else:
                # En transiciones, pasar al siguiente estado automáticamente
                estado_actual = (estado_actual + 1) % len(estados)
                frames_actuales = estados[estado_actual]
        
        time.sleep(1 / FPS)
    
    # ========================================
    # ANIMACIÓN FINAL
    # ========================================
    os.system("cls" if os.name == "nt" else "clear")
    print("\n" * 4)
    print("    ✅ ¡TODO LISTO!")
    print()
    
    # Animación de celebración final
    frames_celebracion = [
        ["   \\o/     \\o/", "    |       | ", "   / \\     / \\"],
        ["    o       o", "   /|\\     /|\\", "   / \\     / \\"],
    ]
    
    for _ in range(3):  # 3 ciclos de celebración
        for frame in frames_celebracion:
            os.system("cls" if os.name == "nt" else "clear")
            print("\n" * 4)
            print("    ✅ ¡TODO LISTO!")
            print()
            for line in frame:
                print("    " + line)
            time.sleep(0.3)
    
    time.sleep(1)
