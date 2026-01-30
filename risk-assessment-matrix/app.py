"""
Risk Assessment Matrix Tool
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from risk_calculator import (
    RiskEntry, 
    get_risk_rating, 
    get_rating_color, 
    get_action_required,
    generate_risk_matrix,
    LIKELIHOOD_SCALE,
    IMPACT_SCALE
)


# config page
st.set_page_config(
    page_title="Risk Assessment Matrix",
    page_icon="🎯",
    layout="wide"
)

# set css, simple markdown
st.markdown("""
<style>
    .risk-low { background-color: #28a745; color: white; padding: 5px 10px; border-radius: 4px; }
    .risk-medium { background-color: #ffc107; color: black; padding: 5px 10px; border-radius: 4px; }
    .risk-high { background-color: #fd7e14; color: white; padding: 5px 10px; border-radius: 4px; }
    .risk-critical { background-color: #dc3545; color: white; padding: 5px 10px; border-radius: 4px; }
    .metric-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session and states."""
    if 'risks' not in st.session_state:
        st.session_state.risks = []


def create_heat_map(risks: list) -> go.Figure:
    # Numeric axes for a true 5x5 matrix
    x_vals = [1, 2, 3, 4, 5]          # impact of risk
    y_vals = [5, 4, 3, 2, 1]          # likelihood of risk

    z_values = [[0]*5 for _ in range(5)]
    hover_text = [[""]*5 for _ in range(5)]

    base_colors = [         # set colors
        [0, '#e8f5e9'],
        [0.16, '#28a745'],
        [0.36, '#ffc107'],
        [0.64, '#fd7e14'],
        [1, '#dc3545']
    ]

    matrix = generate_risk_matrix()
    for i, row in enumerate(matrix):         # -> likelihood
        for j, cell in enumerate(row):       # -> impact
            z_values[i][j] = cell["score"]
            hover_text[i][j] = f"Score: {cell['score']}<br>Rating: {cell['rating']}"

    # Add risk entries
    for risk in risks:
        inh_i = 5 - risk.likelihood_inherent   # likelihood 5->0, 1->4
        inh_j = risk.impact_inherent - 1       # impact 1->0, 5->4
        hover_text[inh_i][inh_j] += f"<br><br>📍 {risk.asset} (Inherent)"

        res_i = 5 - risk.likelihood_residual
        res_j = risk.impact_residual - 1
        hover_text[res_i][res_j] += f"<br><br>🎯 {risk.asset} (Residual)"

    fig = go.Figure(data=go.Heatmap(
        z=z_values,
        x=x_vals,
        y=y_vals,
        colorscale=base_colors,
        showscale=True,
        colorbar=dict(title="Risk Score"),
        hovertemplate='%{text}<extra></extra>',
        text=hover_text
    ))

    # Where to place score
    for i, row in enumerate(matrix):
        for j, cell in enumerate(row):
            fig.add_annotation(
                x=j + 1,                # impact 1..5
                y=5 - i,                # likelihood 5..1
                text=str(cell["score"]),
                showarrow=False,
                font=dict(color='white' if cell['score'] > 6 else 'black', size=14)
            )

    # Where to place risk markers
    for idx, risk in enumerate(risks):
        fig.add_trace(go.Scatter(
            x=[risk.impact_inherent],
            y=[risk.likelihood_inherent],
            mode='markers+text',
            marker=dict(size=20, color='white', line=dict(color='black', width=2)),
            text=[f"I{idx+1}"],
            textposition="middle center",
            name=f"{risk.asset} (Inherent)",
            hoverinfo='name'
        ))

        fig.add_trace(go.Scatter(
            x=[risk.impact_residual],
            y=[risk.likelihood_residual],
            mode='markers+text',
            marker=dict(size=20, color='black', line=dict(color='white', width=2)),
            text=[f"R{idx+1}"],
            textposition="middle center",
            name=f"{risk.asset} (Residual)",
            hoverinfo='name'
        ))

    # Labels
    fig.update_layout(
        title="Risk Assessment Heat Map",
        xaxis=dict(
            title="Impact",
            tickmode="array",
            tickvals=[1,2,3,4,5],
            ticktext=['Negligible (1)', 'Minor (2)', 'Moderate (3)', 'Major (4)', 'Severe (5)'],
            range=[0.5, 5.5]
        ),
        yaxis=dict(
            title="Likelihood",
            tickmode="array",
            tickvals=[5,4,3,2,1],
            ticktext=['Almost Certain (5)', 'Likely (4)', 'Possible (3)', 'Unlikely (2)', 'Rare (1)'],
            range=[0.5, 5.5]
        ),
        height=500,
        showlegend=True if risks else False,
        legend=dict(orientation="h", yanchor="bottom", y=-0.3)
    )

    return fig


def render_risk_form():
    """Visualize risk entry"""
    st.subheader("Add New Risk")
    
    with st.form("risk_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            asset = st.text_input("Asset / System Name *", placeholder="Database")
            threat = st.text_area("Threat Description *", placeholder="Unauthorized access")
        
        with col2:
            controls = st.text_area("Existing/Planned Controls", placeholder="Multi-Factor-Authentication")
        
        st.markdown("---")
        st.markdown("#### Inherent Risk (Before Controls)")
        
        col3, col4 = st.columns(2)
        with col3:
            likelihood_inh = st.select_slider(
                "Likelihood",
                options=[1, 2, 3, 4, 5],
                value=3,
                format_func=lambda x: f"{x} - {LIKELIHOOD_SCALE[x][0]}",
                key="likelihood_inh"
            )
            st.caption(LIKELIHOOD_SCALE[likelihood_inh][1])
        
        with col4:
            impact_inh = st.select_slider(
                "Impact",
                options=[1, 2, 3, 4, 5],
                value=3,
                format_func=lambda x: f"{x} - {IMPACT_SCALE[x][0]}",
                key="impact_inh"
            )
            st.caption(IMPACT_SCALE[impact_inh][1])
        
        st.markdown("#### Residual Risk (After Controls)")
        
        col5, col6 = st.columns(2)
        with col5:
            likelihood_res = st.select_slider(
                "Likelihood",
                options=[1, 2, 3, 4, 5],
                value=2,
                format_func=lambda x: f"{x} - {LIKELIHOOD_SCALE[x][0]}",
                key="likelihood_res"
            )
        
        with col6:
            impact_res = st.select_slider(
                "Impact",
                options=[1, 2, 3, 4, 5],
                value=2,
                format_func=lambda x: f"{x} - {IMPACT_SCALE[x][0]}",
                key="impact_res"
            )
        
        submitted = st.form_submit_button("Add Risk", use_container_width=True, type="primary")
        
        if submitted:
            if not asset or not threat:
                st.error("Fill in Asset and Threat fields.")
            else:
                risk = RiskEntry(
                    asset=asset,
                    threat=threat,
                    likelihood_inherent=likelihood_inh,
                    impact_inherent=impact_inh,
                    controls=controls,
                    likelihood_residual=likelihood_res,
                    impact_residual=impact_res
                )
                st.session_state.risks.append(risk)
                st.success(f"Added risk for '{asset}'")
                st.rerun()


def render_risk_table():
    """Visualize risk assessment table."""
    if not st.session_state.risks:
        st.info("No risks added yet. Use the form above to add your first risk.")
        return
    
    st.subheader("Risk Register")
    
    # Create DataFrame
    data = []
    for idx, risk in enumerate(st.session_state.risks):
        inh_rating = risk.inherent_risk_rating
        res_rating = risk.residual_risk_rating
        data.append({
            "#": idx + 1,
            "Asset": risk.asset,
            "Threat": risk.threat[:50] + "..." if len(risk.threat) > 50 else risk.threat,
            "Inherent Score": risk.inherent_risk_score,
            "Inherent Rating": inh_rating.value,
            "Controls": risk.controls[:30] + "..." if len(risk.controls) > 30 else risk.controls,
            "Residual Score": risk.residual_risk_score,
            "Residual Rating": res_rating.value,
            "Reduction": f"{risk.risk_reduction}%",
            "Action": get_action_required(res_rating)
        })
    
    df = pd.DataFrame(data)
    
    # Style für dataframe
    def color_rating(val):
        colors = {
            "Low": "background-color: #28a745; color: white",
            "Medium": "background-color: #ffc107; color: black",
            "High": "background-color: #fd7e14; color: white",
            "Critical": "background-color: #dc3545; color: white"
        }
        return colors.get(val, "")
    
    styled_df = df.style.applymap(color_rating, subset=["Inherent Rating", "Residual Rating"])
    st.dataframe(styled_df, use_container_width=True, hide_index=True)
    
    # Export
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        csv = df.to_csv(index=False)
        st.download_button(
            "Export CSV",
            csv,
            "risk_assessment.csv",
            "text/csv",
            use_container_width=True
        )
    with col2:
        if st.button("Clear All", use_container_width=True):
            st.session_state.risks = []
            st.rerun()


def render_summary_metrics():
    """Render summary metrics cards."""
    if not st.session_state.risks:
        return
    
    st.subheader("Assessment Summary")
    
    total = len(st.session_state.risks)
    critical = sum(1 for r in st.session_state.risks if r.residual_risk_rating.value == "Critical")
    high = sum(1 for r in st.session_state.risks if r.residual_risk_rating.value == "High")
    avg_reduction = sum(r.risk_reduction for r in st.session_state.risks) / total if total > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Risks", total)
    with col2:
        st.metric("Critical Risks", critical, delta=None if critical == 0 else f"{critical} require immediate action", delta_color="inverse")
    with col3:
        st.metric("High Risks", high)
    with col4:
        st.metric("Avg. Risk Reduction", f"{avg_reduction:.0f}%")


def main():
    """Main application entry point."""
    init_session_state()
    
    # Header
    st.title("Risk Assessment Tool")
    st.markdown("*Calculate (inherent and residual) risk, visualize w/ heat map, track risks*")
    st.markdown("---")
    
    # Set layout
    col_left, col_right = st.columns([1, 1.2])
    
    with col_left:
        render_risk_form()
    
    with col_right:
        st.subheader("Risk Heat Map")
        fig = create_heat_map(st.session_state.risks)
        st.plotly_chart(fig, use_container_width=True)
        if st.session_state.risks:
            st.caption("**I** = Inherent Risk | **R** = Residual Risk")
    
    st.markdown("---")
    
    # Summary and Table
    render_summary_metrics()
    render_risk_table()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <small>Risk Assessment Matrix Tool | Built for IT Audit & GRC Professionals</small>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
