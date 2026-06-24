import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ======================================================
# Configuração da página
# ======================================================

st.set_page_config(
    page_title="Calculadora PVT",
    page_icon="🧪",
    layout="wide"
)

# ======================================================
# Constantes
# ======================================================

R = 0.08314  # L.bar/(mol.K)

gases = {
    "CO₂": {"a": 3.592, "b": 0.04267},
    "N₂": {"a": 1.390, "b": 0.03913},
    "CH₄": {"a": 2.253, "b": 0.04278}
}

# ======================================================
# Interface
# ======================================================

st.title("🧪 Calculadora PVT")
st.subheader("Equação de Estado de van der Waals")

# ======================================================
# Painel lateral
# ======================================================
with st.sidebar:
    st.markdown("## ⚙️ Configurações")

    gas = st.selectbox(
        "Escolha o gás",
        list(gases.keys())
    )

    T = st.number_input(
        "Temperatura (K)",
        min_value=200.0,
        max_value=1000.0,
        value=350.0,
        step=10.0
    )

    V = st.number_input(
        "Volume molar (L/mol)",
        min_value=0.01,
        value=0.30,
        step=0.01,
        format="%.3f"
    )

    calcular = st.button("Calcular")

    st.divider()
    
    

# ======================================================
# Resultados
# ======================================================

a = gases[gas]["a"]
b = gases[gas]["b"]

if calcular:    

    if V <= b:

        st.error(
            f"O volume molar deve ser maior que b = {b:.5f} L/mol."
        )

    else:

        # Equação de van der Waals
        P = R*T/(V-b) - a/V**2

        st.metric(
            "Pressão calculada",
            f"{P:.2f} bar"
        )

        # ------------------------------------------------

        volumes = np.linspace(
            0.1,
            2.0,
            300
        )

        Pvdw = R*T/(volumes-b) - a/volumes**2
        Pideal = R*T/volumes

        fig, ax = plt.subplots(figsize=(7,5))

        ax.plot(
            volumes,
            Pvdw,
            label="van der Waals",
            linewidth=2
        )

        ax.plot(
            volumes,
            Pideal,
            "--",
            label="Gás ideal"
        )

        ax.scatter(
            V,
            P,
            color="red",
            s=60,
            zorder=5
        )

        ax.set_xlim(0.05,2.0)
        ax.set_ylim(bottom=0)

        ax.set_xlabel("Volume molar (L/mol)")
        ax.set_ylabel("Pressão (bar)")
        ax.set_title(f"{gas}   T = {T:.1f} K")

        ax.grid(True)

        ax.legend()

        st.pyplot(fig)

        st.info(
            f"a = {a:.3f}   |   b = {b:.5f}"
        )
