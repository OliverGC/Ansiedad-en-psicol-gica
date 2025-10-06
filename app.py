import streamlit as st
import json
import requests

# URL del archivo JSON alojado en tu GitHub
GITHUB_URL = "https://raw.githubusercontent.com/OliverGC/ansiedad-psicologica/main/preguntas.json"

@st.cache_data
def cargar_preguntas(url):
    response = requests.get(url)
    return response.json()

def main():
    st.title("🧠 Test de Ansiedad Psicológica")
    st.write("Responde cada pregunta. Recibirás retroalimentación inmediata y tu resultado final al terminar.")

    preguntas = cargar_preguntas(GITHUB_URL)

    if "indice" not in st.session_state:
        st.session_state.indice = 0
        st.session_state.puntuacion = 0
        st.session_state.mostrando_feedback = False

    if st.session_state.indice < len(preguntas):
        pregunta_actual = preguntas[st.session_state.indice]
        st.subheader(f"Pregunta {st.session_state.indice + 1} de {len(preguntas)}")
        st.write(pregunta_actual["pregunta"])

        opcion = st.radio("Selecciona una respuesta:", pregunta_actual["opciones"], index=None)

        if st.button("Responder"):
            if opcion is not None:
                correcta = pregunta_actual["opciones"][pregunta_actual["correcta"]]
                if opcion == correcta:
                    st.success("✅ ¡Correcto!")
                    st.session_state.puntuacion += 1
                else:
                    st.error(f"❌ Incorrecto. La respuesta correcta era: **{correcta}**")
                st.info(f"💡 {pregunta_actual['explicacion']}")
                st.session_state.mostrando_feedback = True
            else:
                st.warning("Selecciona una respuesta antes de continuar.")

        if st.session_state.mostrando_feedback:
            if st.button("Siguiente pregunta ➡️"):
                st.session_state.indice += 1
                st.session_state.mostrando_feedback = False
    else:
        st.success("🎯 ¡Has completado el test!")
        st.write(f"**Tu puntuación final es:** {st.session_state.puntuacion} / {len(preguntas)}")
        porcentaje = (st.session_state.puntuacion / len(preguntas)) * 100
        st.progress(int(porcentaje))

        if porcentaje >= 80:
            st.balloons()
            st.info("Excelente comprensión del tema 💪")
        elif porcentaje >= 50:
            st.info("Buen desempeño, pero puedes repasar algunos conceptos 🧩")
        else:
            st.warning("Te convendría repasar el tema de ansiedad psicológica 📘")

        if st.button("🔄 Reiniciar test"):
            st.session_state.indice = 0
            st.session_state.puntuacion = 0
            st.session_state.mostrando_feedback = False

if __name__ == "__main__":
    main()
