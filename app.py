import streamlit as st
import pandas as pd

def calculate_growth_rate(P0, PT, T):
    return ((PT/P0)**(1/T)) - 1

def calculate_population(P0, r, t):
    return P0 * (1 + r)**t

def calculate_population_trajectory(Pt, r, t):
    return Pt * (1 + r)

def calculate_absolute_change(Pt, Pt1):
    return Pt1 - Pt
    
def main():
    st.set_page_config(page_title="Calculadora de Crecimiento Poblacional", page_icon="📈", layout="wide")
    
    st.markdown("<h1 style='text-align: center;'>Calculadora de Crecimiento Poblacional</h1>", unsafe_allow_html=True)
    st.latex(r"P_0 = Población Inicial")
    st.latex(r"P_T = Población Final")
    st.latex(r"T = Periodo de Tiempo")

    with st.form("growth_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            P0 = st.number_input("Población Inicial (P0)", min_value=0.0, value=10.0, step=10.0)
        
        with col2:
            T = st.number_input("Periodo (T)", min_value=1.0, value=10.0, step=1.0)
        
        with col3:
            PT = st.number_input("Población Final (PT)", min_value=0.0, value=100.0, step=10.0)
            
        submitted = st.form_submit_button("Calcular")
        
    if submitted:
        if T <= 0:
            st.error("El periodo de tiempo (T) debe ser mayor que 0.")
        elif P0 <= 0:
             st.warning("La Población Inicial (P0) debe ser mayor que 0 para el cálculo del crecimiento.")
        else:
            st.markdown("Calculando la tasa de crecimiento usando la fórmula: ")
            st.latex(r"r = \Big(\frac{P_T}{P_0}\Big)^{\frac{1}{T}}-1")
            r = calculate_growth_rate(P0, PT, T)
            st.success(f"Tasa de Crecimiento Calculada: **{r}**")

            st.markdown("Calculando el crecimiento de la población en el periodo t utilizando la fórmula: ")
            st.latex(r"P_t = P_0 \times (1 + r)^t")
            st.markdown("Calculando la trayectoria de la población en el periodo t utilizando la fórmula: ")
            st.latex(r"P_{t+1} = P_t \times (1 + r)")
            st.markdown("Calculo de cambio absoluto utilizando la fórmula: ")
            st.latex(r"\Delta P = P_{t+1} - P_t")
            population_data = []
            for t_step in range(int(T) + 1):
                Pt_step = calculate_population(P0, r, t_step)
                Pt1_step = calculate_population_trajectory(Pt_step, r, t_step)
                delta_P_step = calculate_absolute_change(Pt_step, Pt1_step)
                population_data.append({"Periodo (t)": t_step, "Población (Pt)": Pt_step, "Población (Pt+1)": Pt1_step, "Cambio Absoluto (ΔP)": delta_P_step})
            
            df_population = pd.DataFrame(population_data)
            st.success("Resultados de la Población por Periodo:")
            st.dataframe(df_population)
            
            st.markdown("### Gráfico de Crecimiento Poblacional")
            st.line_chart(df_population, x="Periodo (t)", y="Población (Pt)")

if __name__ == "__main__":
    main()
