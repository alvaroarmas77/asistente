import streamlit as st
import os
from asistente_agenda.crew import AsistenteAgendaCrew

# Page Config
st.set_page_config(page_title="Asistente de Agenda AI", page_icon="📅")
st.title("🤖 Asistente de Agenda")
st.markdown("Escribe tu solicitud de cita abajo y deja que los agentes se encarguen.")

# Sidebar for status
with st.sidebar:
    st.header("Estado del Sistema")
    if os.getenv("GOOGLE_API_KEY"):
        st.success("API Key Conectada")
    else:
        st.error("API Key Faltante")

# Input area
with st.form("appointment_form"):
    user_request = st.text_area(
        "Solicitud de Cita:",
        placeholder="Ej: Quiero una cita para mañana a las 3pm con Juan Perez..."
    )
    submit_button = st.form_submit_button("Agendar Cita")

# Execution logic
if submit_button and user_request:
    with st.status("🚀 Agentes trabajando...", expanded=True) as status:
        try:
            # Prepare inputs
            inputs = {
                'appointment_request': user_request,
                'Nombre': 'Usuario',
                'apellido': 'Web'
            }
            
            # Initialize and Run Crew
            st.write("Interpretando solicitud...")
            crew_instance = AsistenteAgendaCrew()
            result = crew_instance.crew().kickoff(inputs=inputs)
            
            status.update(label="✅ Proceso Completado", state="complete", expanded=False)
            
            # Display Final Result
            st.subheader("Resultado Final:")
            st.info(result)
            
        except Exception as e:
            st.error(f"Hubo un error: {str(e)}")
            status.update(label="❌ Error en la ejecución", state="error")