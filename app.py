import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page config
st.set_page_config(
    page_title="Andina Comercial S.A.S. | Executive Financial Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Corporate Navy, Slate, Gold & Emerald)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #0F2027 0%, #203A43 50%, #2C5364 100%);
        padding: 24px 30px;
        border-radius: 14px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.12);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.1rem;
        font-weight: 700;
        color: #F8FAFC;
        letter-spacing: -0.5px;
    }
    
    .main-header p {
        margin: 6px 0 0 0;
        font-size: 0.95rem;
        color: #94A3B8;
    }
    
    .badge-pill {
        display: inline-block;
        padding: 4px 12px;
        background: rgba(56, 189, 248, 0.15);
        color: #38BDF8;
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-right: 8px;
    }
    
    .kpi-card {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.08);
    }
    
    .kpi-title {
        color: #64748B;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }
    
    .kpi-value {
        color: #0F172A;
        font-size: 1.7rem;
        font-weight: 700;
        line-height: 1.2;
    }
    
    .kpi-delta-pos {
        color: #059669;
        font-size: 0.82rem;
        font-weight: 600;
        margin-top: 6px;
    }
    
    .kpi-delta-neg {
        color: #DC2626;
        font-size: 0.82rem;
        font-weight: 600;
        margin-top: 6px;
    }
    
    .kpi-sub {
        color: #94A3B8;
        font-size: 0.75rem;
    }
    
    .insight-box {
        background-color: #F8FAFC;
        border-left: 4px solid #2563EB;
        padding: 16px 20px;
        border-radius: 0 10px 10px 0;
        margin: 15px 0 25px 0;
        font-size: 0.92rem;
        color: #334155;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 48px;
        white-space: pre-wrap;
        background-color: #F1F5F9;
        border-radius: 8px 8px 0px 0px;
        padding-top: 10px;
        padding-bottom: 10px;
        font-weight: 600;
        color: #475569;
    }

    .stTabs [aria-selected="true"] {
        background-color: #2563EB !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Load Financial Datasets
@st.cache_data
def load_data():
    bal = pd.read_excel('archivos/balance_general.xlsx')
    er = pd.read_excel('archivos/estado_de_resultados.xlsx')
    efe = pd.read_excel('archivos/estado_flujo_efectivo.xlsx')
    
    # Clean and index
    bal_clean = bal.dropna(subset=['Cuenta']).copy()
    bal_clean['Cuenta'] = bal_clean['Cuenta'].astype(str).str.strip()
    if 'PUC' in bal_clean.columns:
        bal_clean['PUC'] = bal_clean['PUC'].astype(str).replace('nan', '')
    bal_clean.columns = [str(c) for c in bal_clean.columns]
    bal_indexed = bal_clean.set_index('Cuenta')
    
    er_clean = er.dropna(subset=['Cuenta']).copy()
    er_clean['Cuenta'] = er_clean['Cuenta'].astype(str).str.strip()
    if 'PUC' in er_clean.columns:
        er_clean['PUC'] = er_clean['PUC'].astype(str).replace('nan', '')
    er_clean.columns = [str(c) for c in er_clean.columns]
    er_indexed = er_clean.set_index('Cuenta')
    
    efe_clean = efe.dropna(subset=['Concepto']).copy()
    efe_clean['Concepto'] = efe_clean['Concepto'].astype(str).str.strip()
    efe_clean.columns = [str(c) for c in efe_clean.columns]
    efe_indexed = efe_clean.set_index('Concepto')
    
    years = [2021, 2022, 2023, 2024, 2025]
    return bal_indexed, er_indexed, efe_indexed, years

bal_df, er_df, efe_df, years = load_data()

# Compute Financial Metrics and Ratios
def compute_metrics(bal, er, efe, yrs):
    df = pd.DataFrame(index=yrs)
    str_yrs = [str(y) for y in yrs]
    
    # 1. Base statement figures
    df['Ventas'] = [er.loc['Ingresos operacionales (ventas netas)', str(y)] for y in yrs]
    df['CostoVentas'] = [er.loc['Costo de ventas (mercancía vendida)', str(y)] for y in yrs]
    df['UtilidadBruta'] = [er.loc['Utilidad bruta', str(y)] for y in yrs]
    df['GastosAdmin'] = [er.loc['Gastos de administración', str(y)] for y in yrs]
    df['GastosVentas'] = [er.loc['Gastos de ventas', str(y)] for y in yrs]
    df['Deprec'] = [er.loc['Depreciaciones y amortizaciones', str(y)] for y in yrs]
    df['EBIT'] = [er.loc['Utilidad operacional (EBIT)', str(y)] for y in yrs]
    df['Intereses'] = [er.loc['Gastos financieros (intereses)', str(y)] for y in yrs]
    df['UtilidadNeta'] = [er.loc['Utilidad neta del ejercicio', str(y)] for y in yrs]
    df['EBITDA'] = df['EBIT'] + df['Deprec']
    
    # Balance Sheet Items
    df['Efectivo'] = [bal.loc['Efectivo y equivalentes', str(y)] for y in yrs]
    df['Clientes'] = [bal.loc['Deudores (cuentas por cobrar clientes)', str(y)] for y in yrs]
    df['Inventarios'] = [bal.loc['Inventarios', str(y)] for y in yrs]
    df['OtrosActCorr'] = [bal.loc['Otros activos corrientes', str(y)] for y in yrs]
    df['ActivoCorriente'] = [bal.loc['Total activo corriente', str(y)] for y in yrs]
    df['PPE'] = [bal.loc['Propiedad, planta y equipo (neto)', str(y)] for y in yrs]
    df['Intangibles'] = [bal.loc['Intangibles (neto)', str(y)] for y in yrs]
    df['ActivoTotal'] = [bal.loc['Total activos', str(y)] for y in yrs]
    
    df['ObligCP'] = [bal.loc['Obligaciones financieras - corto plazo', str(y)] for y in yrs]
    df['Proveedores'] = [bal.loc['Proveedores', str(y)] for y in yrs]
    df['CuentasPagar'] = [bal.loc['Cuentas por pagar y otros pasivos', str(y)] for y in yrs]
    df['ImpuestosPagar'] = [bal.loc['Impuestos por pagar', str(y)] for y in yrs]
    df['PasivoCorriente'] = [bal.loc['Total pasivo corriente', str(y)] for y in yrs]
    df['ObligLP'] = [bal.loc['Obligaciones financieras - largo plazo', str(y)] for y in yrs]
    df['PasivoTotal'] = [bal.loc['Total pasivos', str(y)] for y in yrs]
    df['Patrimonio'] = [bal.loc['Total patrimonio', str(y)] for y in yrs]
    df['DeudaFinancieraTotal'] = df['ObligCP'] + df['ObligLP']
    df['DeudaNeta'] = df['DeudaFinancieraTotal'] - df['Efectivo']
    
    # Cash Flow Statement Items
    df['CFO'] = [efe.loc['Flujo neto de efectivo de operación (CFO)', str(y)] for y in yrs]
    df['CAPEX'] = [abs(efe.loc['(-) Compras de propiedad, planta y equipo (CAPEX)', str(y)]) for y in yrs]
    df['CFI'] = [efe.loc['Flujo neto de efectivo de inversión (CFI)', str(y)] for y in yrs]
    df['Dividendos'] = [abs(efe.loc['(-) Dividendos pagados', str(y)]) for y in yrs]
    df['CFF'] = [efe.loc['Flujo neto de efectivo de financiación (CFF)', str(y)] for y in yrs]
    df['FCF'] = df['CFO'] - df['CAPEX']  # Free Cash Flow to Firm
    
    # 2. Profitability Margins (%)
    df['MargenBruto'] = (df['UtilidadBruta'] / df['Ventas']) * 100
    df['MargenEBITDA'] = (df['EBITDA'] / df['Ventas']) * 100
    df['MargenOperacional'] = (df['EBIT'] / df['Ventas']) * 100
    df['MargenNeto'] = (df['UtilidadNeta'] / df['Ventas']) * 100
    
    # 3. Returns (%)
    df['ROA'] = (df['UtilidadNeta'] / df['ActivoTotal']) * 100
    df['ROE'] = (df['UtilidadNeta'] / df['Patrimonio']) * 100
    # ROCE = EBIT / (Total Activos - Pasivo Corriente)
    df['CapitalEmpleada'] = df['ActivoTotal'] - df['PasivoCorriente']
    df['ROCE'] = (df['EBIT'] / df['CapitalEmpleada']) * 100
    
    # 4. DuPont 3-Step Decomposition
    # ROE = Margen Neto * Rotación de Activos * Apalancamiento Financiero
    df['RotacionActivos'] = df['Ventas'] / df['ActivoTotal']
    df['ApalancamientoDupont'] = df['ActivoTotal'] / df['Patrimonio']
    df['DuPont_ROE'] = (df['MargenNeto'] / 100) * df['RotacionActivos'] * df['ApalancamientoDupont'] * 100
    
    # 5. Liquidity & Working Capital
    df['RazonCorriente'] = df['ActivoCorriente'] / df['PasivoCorriente']
    df['PruebaAcida'] = (df['ActivoCorriente'] - df['Inventarios']) / df['PasivoCorriente']
    df['CapitalTrabajoNeto'] = df['ActivoCorriente'] - df['PasivoCorriente']
    # KTNO = (Clientes + Inventarios) - Proveedores
    df['KTNO'] = (df['Clientes'] + df['Inventarios']) - df['Proveedores']
    df['KTNO_sobre_Ventas'] = (df['KTNO'] / df['Ventas']) * 100
    
    # 6. Operational Efficiency (Days)
    # DSO (Días de Cartera) = (Clientes / Ventas) * 365
    df['DSO'] = (df['Clientes'] / df['Ventas']) * 365
    # DIO (Días de Inventario) = (Inventarios / CostoVentas) * 365
    df['DIO'] = (df['Inventarios'] / df['CostoVentas']) * 365
    # DPO (Días de Proveedores) = (Proveedores / CostoVentas) * 365
    df['DPO'] = (df['Proveedores'] / df['CostoVentas']) * 365
    # Ciclo de Conversión de Efectivo (CCC) = DSO + DIO - DPO
    df['CCC'] = df['DSO'] + df['DIO'] - df['DPO']
    
    # 7. Solvency & Debt Health
    df['EndeudamientoTotal'] = (df['PasivoTotal'] / df['ActivoTotal']) * 100
    df['Deuda_Patrimonio'] = df['PasivoTotal'] / df['Patrimonio']
    df['CoberturaIntereses'] = df['EBIT'] / df['Intereses']
    df['DeudaNeta_EBITDA'] = df['DeudaNeta'] / df['EBITDA']
    df['DeudaFinanciera_EBITDA'] = df['DeudaFinancieraTotal'] / df['EBITDA']
    
    # Growth Rates (YoY %)
    df['CrecimientoVentas'] = df['Ventas'].pct_change() * 100
    df['CrecimientoEBIT'] = df['EBIT'].pct_change() * 100
    df['CrecimientoUtilidadNeta'] = df['UtilidadNeta'].pct_change() * 100
    df['CrecimientoCFO'] = df['CFO'].pct_change() * 100
    
    return df

metrics_df = compute_metrics(bal_df, er_df, efe_df, years)

# Sidebar Controls & Case Info
st.sidebar.image("https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=600&q=80", use_container_width=True)
st.sidebar.title("Configuración de Análisis")
st.sidebar.markdown("**Distribuciones Andina Comercial S.A.S.**  \n*NIT: 900.548.120-4 | Sector B2B*")

selected_year = st.sidebar.selectbox("Seleccionar Año de Referencia:", years, index=len(years)-1)
comp_year = st.sidebar.selectbox("Comparar contra:", years, index=len(years)-2)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🏢 Modelo de Negocio")
st.sidebar.info("""
**Propuesta de Valor:**
Distribuidor B2B de seguridad electrónica, redes y herramientas. Competencia diferenciada en disponibilidad inmediata, cumplimiento logístico y soporte técnico preventa/posventa.
""")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📥 Exportar Reportes")
csv_data = metrics_df.to_csv().encode('utf-8')
st.sidebar.download_button(
    label="Descargar Indicadores (CSV)",
    data=csv_data,
    file_name=f"indicadores_financieros_andina_2021_2025.csv",
    mime="text/csv"
)

# Main Title & Subtitle Banner
st.markdown("""
<div class="main-header">
    <div>
        <span class="badge-pill">DIAGNÓSTICO ESTRATÉGICO 2021 - 2025</span>
        <span class="badge-pill">ANÁLISIS FINANCIERO INTEGRAL</span>
        <span class="badge-pill">CREACIÓN DE VALOR</span>
    </div>
    <h1>Dashboard Financiero Ejecutivo: Andina Comercial S.A.S.</h1>
    <p>Monitoreo de Liquidez, Eficiencia de Capital de Trabajo (KTNO/CCC), Rentabilidad Operativa y Desempeño del Flujo de Caja.</p>
</div>
""", unsafe_allow_html=True)

# Helper function for KPI cards
def render_kpi(col, title, val_str, delta_val=None, delta_suffix="%", inverse_delta=False, subtext=""):
    delta_html = ""
    if delta_val is not None and not np.isnan(delta_val):
        is_pos = delta_val >= 0
        if inverse_delta:
            color_class = "kpi-delta-neg" if is_pos else "kpi-delta-pos"
            arrow = "▲" if is_pos else "▼"
        else:
            color_class = "kpi-delta-pos" if is_pos else "kpi-delta-neg"
            arrow = "▲" if is_pos else "▼"
        delta_html = f'<div class="{color_class}">{arrow} {abs(delta_val):.2f}{delta_suffix} vs ant.</div>'
    
    col.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{val_str}</div>
        {delta_html}
        <div class="kpi-sub">{subtext}</div>
    </div>
    """, unsafe_allow_html=True)

# Executive KPI Header (Top 5 Vital Signs for Selected Year)
row_curr = metrics_df.loc[selected_year]
row_prev = metrics_df.loc[comp_year]

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    v_change = ((row_curr['Ventas'] - row_prev['Ventas']) / row_prev['Ventas']) * 100
    render_kpi(c1, "Ingresos Operacionales", f"${row_curr['Ventas']:,.0f}M", v_change, "%", False, f"Año {selected_year}")
with c2:
    render_kpi(c2, "Margen EBITDA", f"{row_curr['MargenEBITDA']:.1f}%", row_curr['MargenEBITDA'] - row_prev['MargenEBITDA'], " pp", False, f"EBITDA: ${row_curr['EBITDA']:,.0f}M")
with c3:
    render_kpi(c3, "ROE (DuPont)", f"{row_curr['ROE']:.1f}%", row_curr['ROE'] - row_prev['ROE'], " pp", False, f"ROA: {row_curr['ROA']:.1f}%")
with c4:
    ccc_delta = row_curr['CCC'] - row_prev['CCC']
    render_kpi(c4, "Ciclo Conv. Efectivo", f"{row_curr['CCC']:.0f} Días", ccc_delta, " días", True, f"DSO: {row_curr['DSO']:.0f}d | DIO: {row_curr['DIO']:.0f}d")
with c5:
    render_kpi(c5, "Flujo Caja Libre (FCF)", f"${row_curr['FCF']:,.0f}M", ((row_curr['FCF'] - row_prev['FCF'])/abs(row_prev['FCF']))*100, "%", False, f"CFO: ${row_curr['CFO']:,.0f}M")

st.markdown("<br>", unsafe_allow_html=True)

# 6 Analytical Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 1. Desempeño & Rentabilidad",
    "🔄 2. Capital de Trabajo & Ciclo de Efectivo",
    "💰 3. Dinámica del Flujo de Caja & Deuda",
    "⚖️ 4. Estructura Patrimonial & Solvencia",
    "🔬 5. Descomposición DuPont & Creación de Valor",
    "📋 6. Estados Financieros & Diagnóstico Estratégico"
])

# ==============================================================================
# TAB 1: DESEMPEÑO Y RENTABILIDAD
# ==============================================================================
with tab1:
    st.subheader("Desempeño Operativo y Rentabilidad (2021 - 2025)")
    st.markdown("""
    Analiza la evolución de los ingresos operacionales, la estructura de costos y la expansión de márgenes a lo largo del quinquenio.
    """)
    
    col_t1_1, col_t1_2 = st.columns(2)
    
    with col_t1_1:
        # Evolution of Sales and Net Income
        fig_rev = go.Figure()
        fig_rev.add_trace(go.Bar(
            x=years,
            y=metrics_df['Ventas'],
            name='Ingresos Operacionales',
            marker_color='#2563EB',
            text=[f"${x:,.0f}M" for x in metrics_df['Ventas']],
            textposition='auto'
        ))
        fig_rev.add_trace(go.Scatter(
            x=years,
            y=metrics_df['UtilidadNeta'],
            name='Utilidad Neta',
            yaxis='y2',
            mode='lines+markers+text',
            line=dict(color='#10B981', width=3),
            marker=dict(size=8),
            text=[f"${x:,.0f}M" for x in metrics_df['UtilidadNeta']],
            textposition='top center'
        ))
        fig_rev.update_layout(
            title="<b>Ingresos Operacionales vs. Utilidad Neta (Millones COP)</b>",
            xaxis=dict(title="Año"),
            yaxis=dict(title="Ventas (COP)", showgrid=True, gridcolor='#F1F5F9'),
            yaxis2=dict(title="Utilidad Neta (COP)", overlaying='y', side='right', showgrid=False),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=400,
            margin=dict(l=40, r=40, t=50, b=40)
        )
        st.plotly_chart(fig_rev, use_container_width=True)
        
    with col_t1_2:
        # Margin Expansion
        fig_marg = go.Figure()
        fig_marg.add_trace(go.Scatter(
            x=years, y=metrics_df['MargenBruto'], name='Margen Bruto',
            line=dict(color='#6366F1', width=2.5, dash='dot'), mode='lines+markers'
        ))
        fig_marg.add_trace(go.Scatter(
            x=years, y=metrics_df['MargenEBITDA'], name='Margen EBITDA',
            line=dict(color='#F59E0B', width=3), mode='lines+markers+text',
            text=[f"{v:.1f}%" for v in metrics_df['MargenEBITDA']], textposition='top center'
        ))
        fig_marg.add_trace(go.Scatter(
            x=years, y=metrics_df['MargenOperacional'], name='Margen Operacional (EBIT)',
            line=dict(color='#0284C7', width=2.5), mode='lines+markers'
        ))
        fig_marg.add_trace(go.Scatter(
            x=years, y=metrics_df['MargenNeto'], name='Margen Neto',
            line=dict(color='#10B981', width=2.5), mode='lines+markers+text',
            text=[f"{v:.1f}%" for v in metrics_df['MargenNeto']], textposition='bottom center'
        ))
        fig_marg.update_layout(
            title="<b>Evolución de Márgenes de Rentabilidad (%)</b>",
            xaxis=dict(title="Año"),
            yaxis=dict(title="Margen (%)", range=[0, 32], showgrid=True, gridcolor='#F1F5F9'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=400,
            margin=dict(l=40, r=40, t=50, b=40)
        )
        st.plotly_chart(fig_marg, use_container_width=True)
        
    st.markdown("""
    <div class="insight-box">
        💡 <b>Hallazgo Analítico:</b> Las ventas de Andina crecieron de <b>$80,000M a $120,000M</b> (+50.0% acumulado, TCAC +10.67%). La compañía mantuvo un margen bruto estrictamente disciplinado en el <b>25.0%</b> gracias a su valor agregado y marcas propias, mientras que el <b>Margen EBITDA se expandió en 180 puntos básicos (de 8.70% a 10.50%)</b>, demostrando un fuerte apalancamiento operativo con dilución de costos de administración y ventas a medida que escala la plataforma digital.
    </div>
    """, unsafe_allow_html=True)
    
    # Waterfall for Selected Year
    st.markdown(f"#### Desglose de Cascada de Resultados Operacionales ({selected_year})")
    wf_year = selected_year
    impuesto_val = er_df.loc['Impuesto de renta', str(wf_year)]
    fig_wf = go.Figure(go.Waterfall(
        name="Resultados",
        orientation="v",
        measure=["relative", "relative", "total", "relative", "relative", "relative", "total", "relative", "total"],
        x=[
            "Ingresos Ventas", "Costo Ventas", "Utilidad Bruta",
            "Gastos Admin", "Gastos Ventas", "Depreciación",
            "EBIT (Operacional)", "Intereses e Impuestos", "Utilidad Neta"
        ],
        textposition="outside",
        text=[
            f"+${metrics_df.loc[wf_year, 'Ventas']:,.0f}M",
            f"-${metrics_df.loc[wf_year, 'CostoVentas']:,.0f}M",
            f"${metrics_df.loc[wf_year, 'UtilidadBruta']:,.0f}M",
            f"-${metrics_df.loc[wf_year, 'GastosAdmin']:,.0f}M",
            f"-${metrics_df.loc[wf_year, 'GastosVentas']:,.0f}M",
            f"-${metrics_df.loc[wf_year, 'Deprec']:,.0f}M",
            f"${metrics_df.loc[wf_year, 'EBIT']:,.0f}M",
            f"-${(metrics_df.loc[wf_year, 'Intereses'] + impuesto_val):,.0f}M",
            f"${metrics_df.loc[wf_year, 'UtilidadNeta']:,.0f}M"
        ],
        y=[
            metrics_df.loc[wf_year, 'Ventas'],
            -metrics_df.loc[wf_year, 'CostoVentas'],
            metrics_df.loc[wf_year, 'UtilidadBruta'],
            -metrics_df.loc[wf_year, 'GastosAdmin'],
            -metrics_df.loc[wf_year, 'GastosVentas'],
            -metrics_df.loc[wf_year, 'Deprec'],
            metrics_df.loc[wf_year, 'EBIT'],
            -(metrics_df.loc[wf_year, 'Intereses'] + impuesto_val),
            metrics_df.loc[wf_year, 'UtilidadNeta']
        ],
        connector={"line": {"color": "#94A3B8"}},
        decreasing={"marker": {"color": "#EF4444"}},
        increasing={"marker": {"color": "#10B981"}},
        totals={"marker": {"color": "#1E293B"}}
    ))
    fig_wf.update_layout(
        height=380,
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=40, r=40, t=20, b=40)
    )
    st.plotly_chart(fig_wf, use_container_width=True)

# ==============================================================================
# TAB 2: CAPITAL DE TRABAJO & CICLO DE EFECTIVO
# ==============================================================================
with tab2:
    st.subheader("Gestión de Capital de Trabajo y Eficiencia Operativa")
    st.markdown("""
    En el modelo B2B de Andina, donde la disponibilidad y el crédito comercial son determinantes de la propuesta de valor, la gestión del **KTNO** y los **Días de Conversión de Efectivo (CCC)** marca la diferencia entre rentabilidad teórica y liquidez real.
    """)
    
    col_t2_1, col_t2_2 = st.columns(2)
    
    with col_t2_1:
        # CCC Components
        fig_ccc = go.Figure()
        fig_ccc.add_trace(go.Bar(x=years, y=metrics_df['DSO'], name='Días Cartera (DSO)', marker_color='#3B82F6'))
        fig_ccc.add_trace(go.Bar(x=years, y=metrics_df['DIO'], name='Días Inventario (DIO)', marker_color='#F59E0B'))
        fig_ccc.add_trace(go.Bar(x=years, y=-metrics_df['DPO'], name='(-) Días Proveedores (DPO)', marker_color='#EF4444'))
        fig_ccc.add_trace(go.Scatter(
            x=years, y=metrics_df['CCC'], name='Ciclo Neto Efectivo (CCC)',
            mode='lines+markers+text', line=dict(color='#0F172A', width=3),
            marker=dict(size=8), text=[f"{x:.1f}d" for x in metrics_df['CCC']],
            textposition='top center'
        ))
        fig_ccc.update_layout(
            barmode='relative',
            title="<b>Ciclo de Conversión de Efectivo (DSO + DIO - DPO)</b>",
            xaxis=dict(title="Año"),
            yaxis=dict(title="Días de Operación", showgrid=True, gridcolor='#F1F5F9'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=420,
            margin=dict(l=40, r=40, t=50, b=40)
        )
        st.plotly_chart(fig_ccc, use_container_width=True)
        
    with col_t2_2:
        # KTNO and KTNO / Sales
        fig_ktno = go.Figure()
        fig_ktno.add_trace(go.Bar(
            x=years, y=metrics_df['KTNO'], name='KTNO ($ Millones)',
            marker_color='#8B5CF6', text=[f"${x:,.0f}M" for x in metrics_df['KTNO']],
            textposition='auto'
        ))
        fig_ktno.add_trace(go.Scatter(
            x=years, y=metrics_df['KTNO_sobre_Ventas'], name='KTNO / Ventas (%)',
            yaxis='y2', mode='lines+markers+text',
            line=dict(color='#DC2626', width=2.5),
            marker=dict(size=8), text=[f"{x:.1f}%" for x in metrics_df['KTNO_sobre_Ventas']],
            textposition='bottom center'
        ))
        fig_ktno.update_layout(
            title="<b>Capital de Trabajo Neto Operativo (KTNO) y Productividad</b>",
            xaxis=dict(title="Año"),
            yaxis=dict(title="KTNO (Millones COP)", showgrid=True, gridcolor='#F1F5F9'),
            yaxis2=dict(title="KTNO / Ventas (%)", overlaying='y', side='right', range=[10, 25], showgrid=False),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=420,
            margin=dict(l=40, r=40, t=50, b=40)
        )
        st.plotly_chart(fig_ktno, use_container_width=True)
        
    st.markdown("""
    <div class="insight-box">
        💡 <b>Diagnóstico del Caso: 'Vender sin Generar Caja' superado con éxito</b>:
        <ul style="margin: 6px 0 0 0; padding-left: 20px;">
            <li>En <b>2021</b>, la empresa experimentó una fuerte presión de caja con un <b>CCC de 75.0 días</b> y una inmovilización de <b>18.8% de las ventas en KTNO</b>.</li>
            <li>A partir de <b>2022</b>, la implementación de estrictas políticas de recaudo B2B (DSO reducido de 50.0 a 43.0 días), optimización de stocks (DIO reducido de 65.0 a 58.0 días) y mejor negociación con proveedores (DPO incrementado de 40.0 a 45.0 días) redujeron drásticamente el <b>CCC a 56.0 días en 2025</b> (-19 días).</li>
            <li>Esto liberó <b>capital atrapado</b>, disminuyendo la intensidad de capital de trabajo sobre ventas al <b>14.5%</b>.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Detailed Operational Days Table
    st.markdown("#### Detalle de Métricas de Eficiencia Operativa")
    eff_table = pd.DataFrame({
        'Año': years,
        'Días Cartera (DSO)': [f"{x:.1f} días" for x in metrics_df['DSO']],
        'Días Inventario (DIO)': [f"{x:.1f} días" for x in metrics_df['DIO']],
        'Días Proveedores (DPO)': [f"{x:.1f} días" for x in metrics_df['DPO']],
        'Ciclo Efectivo (CCC)': [f"{x:.1f} días" for x in metrics_df['CCC']],
        'KTNO ($M)': [f"${x:,.0f}M" for x in metrics_df['KTNO']],
        'KTNO / Ventas': [f"{x:.2f}%" for x in metrics_df['KTNO_sobre_Ventas']]
    }).set_index('Año')
    st.dataframe(eff_table, use_container_width=True)

# ==============================================================================
# TAB 3: DINÁMICA DEL FLUJO DE CAJA & DEUDA
# ==============================================================================
with tab3:
    st.subheader("Dinámica del Flujo de Efectivo, CAPEX y Sostenibilidad de Deuda")
    st.markdown("""
    Evaluación de la calidad de las ganancias (Cash Flow Conversion), generación de **Flujo de Caja Libre (FCF)** y cobertura de obligaciones financieras.
    """)
    
    col_t3_1, col_t3_2 = st.columns(2)
    
    with col_t3_1:
        # Cash Flow Breakdown (CFO, CFI, CFF)
        fig_cf = go.Figure()
        fig_cf.add_trace(go.Bar(x=years, y=metrics_df['CFO'], name='Flujo Operativo (CFO)', marker_color='#10B981'))
        fig_cf.add_trace(go.Bar(x=years, y=metrics_df['CFI'], name='Flujo Inversión (CFI / CAPEX)', marker_color='#EF4444'))
        fig_cf.add_trace(go.Bar(x=years, y=metrics_df['CFF'], name='Flujo Financiación (CFF)', marker_color='#6366F1'))
        fig_cf.update_layout(
            barmode='group',
            title="<b>Flujos de Caja por Actividad (COP Millones)</b>",
            xaxis=dict(title="Año"),
            yaxis=dict(title="Flujo Neto (COP)", showgrid=True, gridcolor='#F1F5F9'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=420,
            margin=dict(l=40, r=40, t=50, b=40)
        )
        st.plotly_chart(fig_cf, use_container_width=True)
        
    with col_t3_2:
        # Cash Accumulation & FCF
        fig_fcf = go.Figure()
        fig_fcf.add_trace(go.Bar(
            x=years, y=metrics_df['FCF'], name='Flujo de Caja Libre (FCF)',
            marker_color='#0EA5E9', text=[f"${x:,.0f}M" for x in metrics_df['FCF']],
            textposition='auto'
        ))
        fig_fcf.add_trace(go.Scatter(
            x=years, y=metrics_df['Efectivo'], name='Saldo Final Caja',
            yaxis='y2', mode='lines+markers+text',
            line=dict(color='#059669', width=3),
            marker=dict(size=8), text=[f"${x:,.0f}M" for x in metrics_df['Efectivo']],
            textposition='top center'
        ))
        fig_fcf.update_layout(
            title="<b>Flujo de Caja Libre (FCF) vs. Saldo de Efectivo Acumulado</b>",
            xaxis=dict(title="Año"),
            yaxis=dict(title="FCF (CFO - CAPEX)", showgrid=True, gridcolor='#F1F5F9'),
            yaxis2=dict(title="Efectivo en Caja", overlaying='y', side='right', range=[0, 15000], showgrid=False),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=420,
            margin=dict(l=40, r=40, t=50, b=40)
        )
        st.plotly_chart(fig_fcf, use_container_width=True)
        
    # Free Cash Flow & Debt Metrics
    col_t3_3, col_t3_4 = st.columns(2)
    with col_t3_3:
        fig_cov = go.Figure()
        fig_cov.add_trace(go.Scatter(
            x=years, y=metrics_df['CoberturaIntereses'], name='Cobertura Intereses (EBIT / Intereses)',
            mode='lines+markers+text', line=dict(color='#8B5CF6', width=3),
            marker=dict(size=8), text=[f"{x:.2f}x" for x in metrics_df['CoberturaIntereses']],
            textposition='top center'
        ))
        fig_cov.add_hline(y=3.0, line_dash="dash", line_color="red", annotation_text="Límite Prudencial (3.0x)")
        fig_cov.update_layout(
            title="<b>Capacidad de Servicio de Deuda (Cobertura de Intereses)</b>",
            xaxis=dict(title="Año"),
            yaxis=dict(title="Veces (x)", range=[2, 9], showgrid=True, gridcolor='#F1F5F9'),
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=360,
            margin=dict(l=40, r=40, t=50, b=40)
        )
        st.plotly_chart(fig_cov, use_container_width=True)
        
    with col_t3_4:
        fig_dne = go.Figure()
        fig_dne.add_trace(go.Bar(
            x=years, y=metrics_df['DeudaNeta_EBITDA'], name='Deuda Neta / EBITDA',
            marker_color='#F43F5E', text=[f"{x:.2f}x" for x in metrics_df['DeudaNeta_EBITDA']],
            textposition='auto'
        ))
        fig_dne.update_layout(
            title="<b>Apalancamiento Neto: Deuda Neta / EBITDA</b>",
            xaxis=dict(title="Año"),
            yaxis=dict(title="Ratio (Veces)", range=[0, 2.0], showgrid=True, gridcolor='#F1F5F9'),
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=360,
            margin=dict(l=40, r=40, t=50, b=40)
        )
        st.plotly_chart(fig_dne, use_container_width=True)
        
    st.markdown("""
    <div class="insight-box">
        💡 <b>Solidez del Flujo de Fondos:</b>
        <ul style="margin: 6px 0 0 0; padding-left: 20px;">
            <li>En 2021, el <b>Flujo de Caja Libre fue negativo (-$288M)</b>, lo que explicaba la angustia de liquidez documentada en el caso.</li>
            <li>Gracias a la disciplina de capital de trabajo, el FCF rebotó fuertemente hasta alcanzar <b>+$4,288M en 2025</b>, financiando holgadamente el CAPEX de modernización tecnológica e infraestructura logística ($3,500M en 2025) y el pago de dividendos ($2,340M).</li>
            <li>El ratio <b>Deuda Neta / EBITDA cayó desde 1.69x en 2021 a solo 0.51x en 2025</b>, reduciendo drásticamente el riesgo de quiebra financiera y fortaleciendo la cobertura de intereses de <b>3.84x a 7.59x</b>.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# TAB 4: ESTRUCTURA PATRIMONIAL & SOLVENCIA
# ==============================================================================
with tab4:
    st.subheader("Estructura de Capital, Solvencia y Liquidez Inmediata")
    st.markdown("""
    Evaluación de la composición del Balance General: evolución del pasivo versus patrimonio y robustez de los índices de liquidez corriente y prueba ácida.
    """)
    
    col_t4_1, col_t4_2 = st.columns(2)
    
    with col_t4_1:
        # Capital Structure Stacked Bar
        fig_cap = go.Figure()
        fig_cap.add_trace(go.Bar(
            x=years, y=metrics_df['PasivoTotal'], name='Pasivos Totales',
            marker_color='#64748B', text=[f"${x:,.0f}M" for x in metrics_df['PasivoTotal']],
            textposition='inside'
        ))
        fig_cap.add_trace(go.Bar(
            x=years, y=metrics_df['Patrimonio'], name='Patrimonio Neto',
            marker_color='#0284C7', text=[f"${x:,.0f}M" for x in metrics_df['Patrimonio']],
            textposition='inside'
        ))
        fig_cap.update_layout(
            barmode='stack',
            title="<b>Estructura de Financiamiento: Pasivo vs. Patrimonio (COP M)</b>",
            xaxis=dict(title="Año"),
            yaxis=dict(title="Activo Total Financiado (COP M)", showgrid=True, gridcolor='#F1F5F9'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=420,
            margin=dict(l=40, r=40, t=50, b=40)
        )
        st.plotly_chart(fig_cap, use_container_width=True)
        
    with col_t4_2:
        # Liquidity Ratios
        fig_liq = go.Figure()
        fig_liq.add_trace(go.Scatter(
            x=years, y=metrics_df['RazonCorriente'], name='Razón Corriente (Act. Corr / Pas. Corr)',
            mode='lines+markers+text', line=dict(color='#2563EB', width=3),
            marker=dict(size=8), text=[f"{x:.2f}x" for x in metrics_df['RazonCorriente']],
            textposition='top center'
        ))
        fig_liq.add_trace(go.Scatter(
            x=years, y=metrics_df['PruebaAcida'], name='Prueba Ácida (Sin Inventarios)',
            mode='lines+markers+text', line=dict(color='#F59E0B', width=2.5),
            marker=dict(size=8), text=[f"{x:.2f}x" for x in metrics_df['PruebaAcida']],
            textposition='bottom center'
        ))
        fig_liq.add_hline(y=1.0, line_dash="dash", line_color="red", annotation_text="Límite 1.0x")
        fig_liq.update_layout(
            title="<b>Indicadores de Liquidez: Razón Corriente y Prueba Ácida</b>",
            xaxis=dict(title="Año"),
            yaxis=dict(title="Ratio (Veces)", range=[0.8, 2.5], showgrid=True, gridcolor='#F1F5F9'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=420,
            margin=dict(l=40, r=40, t=50, b=40)
        )
        st.plotly_chart(fig_liq, use_container_width=True)
        
    st.markdown("""
    <div class="insight-box">
        💡 <b>Comentarios de Solvencia:</b>
        <ul style="margin: 6px 0 0 0; padding-left: 20px;">
            <li>El <b>Nivel de Endeudamiento Total se redujo del 53.15% en 2021 al 50.26% en 2025</b>. El patrimonio se fortaleció en un <b>+75.9%</b> gracias a la acumulación de utilidades retenidas ($19,627M en 2025).</li>
            <li>La <b>Razón Corriente aumentó de 1.92x a 2.14x</b> y la <b>Prueba Ácida subió de 1.05x a 1.41x</b>, garantizando solvencia inmediata holgada incluso excluyendo los inventarios.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# TAB 5: DESCOMPOSICIÓN DUPONT & CREACIÓN DE VALOR
# ==============================================================================
with tab5:
    st.subheader("Descomposición DuPont de ROE y Retornos sobre Capital")
    st.markdown("""
    Identifica los motores subyacentes de la rentabilidad financiera (**ROE = Margen Neto × Rotación de Activos × Apalancamiento**), evaluando si el rendimiento proviene de márgenes, productividad de activos o apalancamiento financiero.
    """)
    
    col_t5_1, col_t5_2 = st.columns([1, 1])
    
    with col_t5_1:
        # ROE, ROA, ROCE
        fig_ret = go.Figure()
        fig_ret.add_trace(go.Scatter(
            x=years, y=metrics_df['ROE'], name='ROE (Rentabilidad Financiera)',
            mode='lines+markers+text', line=dict(color='#10B981', width=3),
            marker=dict(size=8), text=[f"{x:.1f}%" for x in metrics_df['ROE']],
            textposition='top center'
        ))
        fig_ret.add_trace(go.Scatter(
            x=years, y=metrics_df['ROCE'], name='ROCE (Rentabilidad Capital Empleado)',
            mode='lines+markers+text', line=dict(color='#8B5CF6', width=2.5),
            marker=dict(size=8), text=[f"{x:.1f}%" for x in metrics_df['ROCE']],
            textposition='bottom center'
        ))
        fig_ret.add_trace(go.Scatter(
            x=years, y=metrics_df['ROA'], name='ROA (Rentabilidad Activo Total)',
            mode='lines+markers+text', line=dict(color='#3B82F6', width=2.5),
            marker=dict(size=8), text=[f"{x:.1f}%" for x in metrics_df['ROA']],
            textposition='bottom center'
        ))
        fig_ret.update_layout(
            title="<b>Evolución de Rentabilidades (ROE, ROCE, ROA %)</b>",
            xaxis=dict(title="Año"),
            yaxis=dict(title="Rentabilidad (%)", range=[5, 30], showgrid=True, gridcolor='#F1F5F9'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=420,
            margin=dict(l=40, r=40, t=50, b=40)
        )
        st.plotly_chart(fig_ret, use_container_width=True)
        
    with col_t5_2:
        # DuPont Components Normalized / Indexed
        fig_dupont = make_subplots(specs=[[{"secondary_y": True}]])
        fig_dupont.add_trace(
            go.Scatter(x=years, y=metrics_df['MargenNeto'], name='1. Margen Neto (%)',
                       line=dict(color='#10B981', width=3), mode='lines+markers'),
            secondary_y=False
        )
        fig_dupont.add_trace(
            go.Scatter(x=years, y=metrics_df['RotacionActivos'], name='2. Rotación Activos (Vtas/Activo)',
                       line=dict(color='#3B82F6', width=3, dash='dash'), mode='lines+markers'),
            secondary_y=True
        )
        fig_dupont.add_trace(
            go.Scatter(x=years, y=metrics_df['ApalancamientoDupont'], name='3. Apalancamiento (Activo/Patrimonio)',
                       line=dict(color='#EF4444', width=3, dash='dot'), mode='lines+markers'),
            secondary_y=True
        )
        fig_dupont.update_layout(
            title="<b>Componentes DuPont (Márgenes vs. Rotación vs. Apalancamiento)</b>",
            xaxis=dict(title="Año"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=420,
            margin=dict(l=40, r=40, t=50, b=40)
        )
        fig_dupont.update_yaxes(title_text="Margen Neto (%)", secondary_y=False, showgrid=True, gridcolor='#F1F5F9')
        fig_dupont.update_yaxes(title_text="Rotación / Apalancamiento (Veces)", secondary_y=True, showgrid=False)
        st.plotly_chart(fig_dupont, use_container_width=True)
        
    st.markdown("#### Matriz DuPont Detallada (2021 - 2025)")
    dupont_df = pd.DataFrame({
        'Año': years,
        'Margen Neto (%)': [f"{x:.2f}%" for x in metrics_df['MargenNeto']],
        '× Rotación Activo (x)': [f"{x:.2f}x" for x in metrics_df['RotacionActivos']],
        '× Apalancamiento Financiero (x)': [f"{x:.2f}x" for x in metrics_df['ApalancamientoDupont']],
        '= ROE DuPont (%)': [f"{x:.2f}%" for x in metrics_df['ROE']],
        'ROA (%)': [f"{x:.2f}%" for x in metrics_df['ROA']],
        'ROCE (%)': [f"{x:.2f}%" for x in metrics_df['ROCE']]
    }).set_index('Año')
    st.dataframe(dupont_df, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box">
        💡 <b>Conclusión DuPont:</b> El ROE pasó de <b>16.58% en 2021 a 21.14% en 2025</b> (+4.56 pp). Lo más destacable es la <b>calidad de este incremento</b>:
        <ul style="margin: 6px 0 0 0; padding-left: 20px;">
            <li>El apalancamiento financiero se <b>redujo de 2.13x a 2.01x</b>, lo que significa que el mayor rendimiento no fue impulsado por mayor endeudamiento riesgoso.</li>
            <li>El motor principal fue la expansión del <b>Margen Neto (de 3.73% a 5.57%)</b>, apalancado por eficiencias operativas y un estricto control de gastos administrativos y de ventas.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# TAB 6: ESTADOS FINANCIEROS & DIAGNÓSTICO ESTRATÉGICO
# ==============================================================================
with tab6:
    st.subheader("Auditoría de Estados Financieros y Matriz Estratégica")
    
    view_option = st.radio("Seleccionar Estado Financiero a Auditar:", 
                           ["Estado de Resultados", "Balance General", "Estado de Flujos de Efectivo", "Diagnóstico Estratégico & Recomendaciones"],
                           horizontal=True)
    
    if view_option == "Estado de Resultados":
        st.markdown("##### Estado de Resultados Integral (Cifras en COP Millones)")
        st.dataframe(er_df, use_container_width=True)
        
    elif view_option == "Balance General":
        st.markdown("##### Balance General Clasificado (Cifras en COP Millones)")
        st.dataframe(bal_df, use_container_width=True)
        
    elif view_option == "Estado de Flujos de Efectivo":
        st.markdown("##### Estado de Flujos de Efectivo (Método Indirecto)")
        st.dataframe(efe_df, use_container_width=True)
        
    else:
        st.markdown("""
        ### Diagnóstico Financiero & Plan de Acción Estratégico
        
        #### 1. Diagnóstico de la Situación Histórica (2021)
        * **El dilema de 'Vender sin Generar Caja':** Andina reportó un crecimiento inicial vigoroso pero padeció un drenaje de liquidez por acumulación en cartera ($10,959M) e inventarios ($10,685M), cerrando 2021 con apenas $740M en caja y un FCF negativo de -$288M.
        * **Dependencia de Financiamiento de Corto Plazo:** Para subsanar la brecha de liquidez del KTNO, la empresa dependía de deuda de corto plazo ($4,385M).
        
        #### 2. Logros del Plan de Reestructuración Operativa (2022 - 2025)
        * **Compresión del Ciclo de Efectivo (CCC):** Se redujo en 19 días enteros (de 75 a 56 días) gracias a la digitalización del canal B2B y acuerdos directos con integradores clave.
        * **Generación Fuerte de Flujo de Caja Libre:** El FCF se tornó consistentemente positivo, alcanzando $4,288M en 2025, robusteciendo la caja a $12,450M.
        * **Desendeudamiento Estructural:** El índice Deuda Neta / EBITDA cayó de 1.69x a 0.51x, garantizando capacidad para asumir nuevas inversiones sin estrés financiero.
        
        #### 3. Recomendaciones Estratégicas para la Junta Directiva (2026 en adelante)
        1. **Optimización del Exceso de Caja:** La compañía cierra 2025 con $12,450M en caja ociosa. Se recomienda estructurar una política formal de reinversión en automatización logística o implementar recompras/dividendos extraordinarios para no diluir el ROE a futuro.
        2. **Profundización del Canal B2B Digital:** Continuar migrando órdenes hacia la plataforma digital propia para acelerar el DSO a menos de 40 días y reducir costos de servicio al cliente.
        3. **Gestión de Portafolio de Marcas Propias:** Fomentar la mezcla hacia líneas de marca propia donde el margen bruto supera la media del 25%, elevando el EBIT agregado.
        """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #94A3B8; font-size: 0.85rem;'>"
    "Dashboard Financiero Corporativo Andina Comercial S.A.S. | Desarrollado con Streamlit & Plotly"
    "</div>",
    unsafe_allow_html=True
)
