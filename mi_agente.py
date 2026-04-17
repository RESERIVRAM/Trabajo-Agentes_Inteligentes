"""
mi_agente.py — Aquí defines tu agente.
╔══════════════════════════════════════════════╗
║  ✏️  EDITA ESTE ARCHIVO                      ║
╚══════════════════════════════════════════════╝

Tu agente debe:
    1. Heredar de la clase Agente
    2. Implementar el método decidir(percepcion)
    3. Retornar: 'arriba', 'abajo', 'izquierda' o 'derecha'

Lo que recibes en 'percepcion':
───────────────────────────────
percepcion = {
    'posicion':       (3, 5),          # Tu fila y columna actual
    'arriba':         'libre',         # Qué hay arriba
    'abajo':          'pared',         # Qué hay abajo
    'izquierda':      'libre',         # Qué hay a la izquierda
    'derecha':        None,            # None = fuera del mapa

    # OPCIONAL — brújula hacia la meta.
    # No es percepción real del entorno, es información global.
    # Usarla hace el ejercicio más fácil. No usarla es más realista.
    'direccion_meta': ('abajo', 'derecha'),
}

Valores posibles de cada dirección:
    'libre'  → puedes moverte ahí
    'pared'  → bloqueado
    'meta'   → ¡la meta! ve hacia allá
    None     → borde del mapa, no puedes ir

Si tu agente retorna un movimiento inválido (hacia pared o
fuera del mapa), simplemente se queda en su lugar.
"""

from entorno import Agente

class MiAgente(Agente):
    """
    Agente basado en utilidad final. 
    Usa un historial para minimizar pasos y evitar entrar en bucles ("loops").
    """

    def __init__(self):
        super().__init__(nombre="Explorador de Utilidad Avanzado")
        # Diccionario para contar cuántas veces pasamos por cada coordenada
        self.historial_visitas = {}

    def al_iniciar(self):
        """Llamado por el entorno al inicio de la corrida."""
        self.historial_visitas = {}

    def decidir(self, percepcion):
        pos_actual = percepcion['posicion']
        # Guardamos la visita de la posición actual sumándole 1
        self.historial_visitas[pos_actual] = self.historial_visitas.get(pos_actual, 0) + 1
        
        direcciones_meta = percepcion['direccion_meta']
        mejores_acciones = []
        max_utilidad = float('-inf')

        for accion in self.ACCIONES:
            estado_celda = percepcion[accion]
            
            if estado_celda is None or estado_celda == 'pared':
                continue

            if estado_celda == 'meta':
                return accion

            futura_pos = self._predecir_posicion(pos_actual, accion)
            num_visitas = self.historial_visitas.get(futura_pos, 0)

            # --- MEDIDA DE UTILIDAD (MINIMIZAR PASOS) ---
            utilidad = 100 
            
            if accion in direcciones_meta:
                utilidad += 50
            
            # Costo: Restar puntos a la utilidad si esa celda ya fue muy visitada.
            # Esto fuerza al agente a explorar zonas nuevas en vez de estancarse.
            utilidad -= (num_visitas * 30)

            if utilidad > max_utilidad:
                max_utilidad = utilidad
                mejores_acciones = [accion]

        return mejores_acciones[0] if mejores_acciones else 'abajo'

    def _predecir_posicion(self, pos, accion):
        """Función auxiliar para saber a qué coordenada nos llevará un movimiento."""
        f, c = pos
        if accion == 'arriba': return (f - 1, c)
        if accion == 'abajo': return (f + 1, c)
        if accion == 'izquierda': return (f, c - 1)
        if accion == 'derecha': return (f, c + 1)
        return pos


        # return 'abajo'
        print('Hola decidir')
        for direccion in self.ACCIONES:
            celda = percepcion[direccion]
            if celda == 'meta':
                return direccion
            if celda == 'libre':
                return direccion

        return 'abajo'  # ← Reemplazar con tu lógica