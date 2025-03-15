import streamlit as st
from supabase import create_client, Client
import time 

# Cargar variables de entorno
SUPABASE_URL =  "https://pipplgjnsnycifhnrahr.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBpcHBsZ2puc255Y2lmaG5yYWhyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDE3NDU3MTcsImV4cCI6MjA1NzMyMTcxN30.wwUhzhNA8bMknz3rM7pcA0tCUlCz7H663UsZzmlYvhw"

# Conectar con Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

#Titulo de la app y logo
st.image("Logo Sunat.png", width=150)
st.markdown("<h1 style='color: #2511bc; text-align: center;'>📄 Registro de Comprobantes de Pago - SUNAT</h1>", unsafe_allow_html=True)

#CREATE
#Solicitar los datos del comprobante de pagos" 
st.header("Datos del comprobante de pago")

fecha_emision = st.date_input("📆Fecha de emisión")
tipo = st.selectbox("🧾Tipo",["Factura","Boleta","Recibo","Otros"])
serie = st.text_input("🔠Serie")
numero = st.text_input("🔢Número")
monto = st.number_input("💵Monto total", min_value=0.01)
ruc = st.text_input("🏪RUC", max_chars=11)
concepto = st.text_area("🖊️Descripción")

#Subir la información a la tabla en Supabase
if st.button("✍️Registrar Comprobante"):
    if fecha_emision and tipo and serie and numero and monto and ruc and concepto:
        data = {
            "fecha_emision": fecha_emision.isoformat(), 
            "tipo": tipo, 
            "serie":serie, 
            "numero":numero,
            "monto":float(monto), 
            "ruc":ruc.strip(), 
            "concepto":concepto
        }
        supabase.table("comprobantes").insert(data).execute()
        st.success("✅Comprobante registrado con éxito")
        time.sleep(2)
        st.rerun()
    else:
        st.warning("⚠️Todos los campos son obligatorios")

#READ
# MOSTRAR COMPROBANTES REGISTRADO

st.header("Mostrar los comprobantes de pago registrados")
comprobantes = supabase.table("comprobantes").select("*").execute()

if comprobantes.data:
    for cdp in comprobantes.data:
        with st.expander(f"🗂️ {cdp['tipo']} {cdp['serie']} - {cdp['numero']} "):
            st.write(f"📆Fecha: {cdp['fecha_emision']}")
            st.write(f"💵Monto: S/{cdp['monto']}")
            st.write(f"🏪RUC: {cdp['ruc']}")
            st.write(f"🖊️Descripción: {cdp['concepto']}")

            #DELETE
            # Botón para eliminar comprobante
            if st.button(f"❌ Eliminar comprobante", key=f"del_{cdp['id']}"):
                supabase.table("comprobantes").delete().eq("id", cdp['id']).execute()
                st.success(f"✅Comprobante {cdp['serie']}-{cdp['numero']} eliminado correctamente")
                time.sleep(2)
                st.rerun()

            #UPDATE
            # Formulario para actualizar datos del comprobante
            st.subheader("🔄Actualizar datos del comprobante")
            nuevo_tipo = st.selectbox("Nuevo Tipo", ["Factura", "Boleta", "Recibo", "Otros"], index=["Factura", "Boleta", "Recibo", "Otros"].index(cdp["tipo"]), key=f"tipo_{cdp['id']}")
            nuevo_monto = st.number_input("Nuevo Monto", value=cdp["monto"], key=f"monto_{cdp['id']}")
            nuevo_concepto = st.text_area("Nuevo Concepto", value=cdp["concepto"], key=f"concepto_{cdp['id']}")
            
            # Botón para guardar cambios
            if st.button("💾Guardar Cambios", key=f"upd_{cdp['id']}"):
                supabase.table("comprobantes").update({
                    "tipo": nuevo_tipo,
                    "monto": nuevo_monto,
                    "concepto": nuevo_concepto
                }).eq("id", cdp["id"]).execute()
                st.success(" ✅Comprobante actualizado")
                time.sleep(2)
                st.rerun()
else:
    st.info("🚫No hay comprobantes registrados aún")