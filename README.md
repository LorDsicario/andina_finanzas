# Dashboard Financiero Ejecutivo: Distribuciones Andina Comercial S.A.S.

Aplicación interactiva desarrollada en **Python** con **Streamlit** y **Plotly** para el análisis financiero y estratégico del periodo 2021 – 2025.

---

## 🚀 Acceso Rápido

La aplicación se encuentra ejecutándose en tu equipo:
- **URL Local:** [http://localhost:8501](http://localhost:8501)

Para iniciarla manualmente en cualquier momento desde la terminal:
```powershell
py -m streamlit run app.py
```

---

## 📊 Arquitectura y Módulos del Dashboard

1. **KPIs Vitales Superiores (Executive Vital Signs):**
   - Ingresos Operacionales con comparativo interanual
   - Margen EBITDA y expansión de puntos básicos
   - ROE (Rentabilidad Financiera vía DuPont)
   - Ciclo de Conversión de Efectivo (CCC en días)
   - Flujo de Caja Libre (FCF)

2. **Pestaña 1: Desempeño & Rentabilidad:**
   - Evolución de Ventas vs. Utilidad Neta
   - Expansión de Márgenes (Bruto, EBITDA, Operacional EBIT, Neto)
   - Gráfico de cascada (*Waterfall*) de resultados del ejercicio

3. **Pestaña 2: Capital de Trabajo & Ciclo de Efectivo:**
   - Descomposición del CCC: Días de Cartera (DSO) + Días de Inventario (DIO) - Días de Proveedores (DPO)
   - Capital de Trabajo Neto Operativo (KTNO) y Productividad de Capital (KTNO / Ventas)
   - Explicación de la resolución del dilema "vender sin generar caja"

4. **Pestaña 3: Dinámica del Flujo de Caja & Deuda:**
   - Flujos por Actividad (Operación CFO, Inversión CFI/CAPEX, Financiación CFF)
   - Generación de Flujo de Caja Libre (FCF) y acumulación de efectivo
   - Capacidad de cobertura de intereses (EBIT / Gastos Financieros)
   - Apalancamiento neto (Deuda Neta / EBITDA)

5. **Pestaña 4: Estructura Patrimonial & Solvencia:**
   - Composición Pasivo vs. Patrimonio
   - Razón Corriente y Prueba Ácida con semáforos prudenciales

6. **Pestaña 5: Descomposición DuPont & Creación de Valor:**
   - Rentabilidades comparadas (ROE, ROCE, ROA)
   - Desagregación en 3 factores: Margen Neto × Rotación de Activos × Apalancamiento Financiero

7. **Pestaña 6: Estados Financieros & Diagnóstico Estratégico:**
   - Tablas interactivas del Balance General, Estado de Resultados y Estado de Flujos de Efectivo
   - Diagnóstico del caso de estudio y recomendaciones estratégicas para la Junta Directiva
