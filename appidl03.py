import streamlit as st
from supabase import create_client, Client

# Cargar variables de entorno
SUPABASE_URL =  "https://pipplgjnsnycifhnrahr.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBpcHBsZ2puc255Y2lmaG5yYWhyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDE3NDU3MTcsImV4cCI6MjA1NzMyMTcxN30.wwUhzhNA8bMknz3rM7pcA0tCUlCz7H663UsZzmlYvhw"

# Conectar con Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

#Titulo de la app
st.title("Registro de comprobantes de pago - SUNAT")

#Solicitar los datos del comprobante de pagos"
st.header("Datos del comprobante de pago")

fecha_emision = st.date_input("Fecha de emisión")
tipo = st.selectbox("Tipo",["Factura","Boleta","ReciboxHonorarios","Otros"])
serie = st.text_input("Serie")
numero = st.text_input("Número")
monto = st.number_input("Monto total")
ruc = st.text_input("RUC", max_chars=11)
concepto = st.text_area("Descripción")

"Subir la información a la tabla en Supabase"
if st.button("Registrar Comprobante"):
    if fecha_emision and tipo and serie and numero and monto and ruc and concepto:
        data = {
            "fecha_emision":fecha_emision.strftime("%Y-%m-%d"), "tipo": tipo, "serie":serie, "numero":numero, "ruc":ruc, "concepto":concepto
        }
        supabase.table("comprobantes").insert(data).execute()
        st.success("Comprobante registrado con éxito")
        st.rerun()
    else:
        st.warning("Todos los campos son obligatorios")
