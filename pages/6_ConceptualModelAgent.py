import streamlit as st
import plotly.graph_objects as go

st.title("🔗 Conceptual Model Agent (Plotly Version)")
st.markdown("Define your constructs and visualize your conceptual model.")

# Step 1: Inputs
with st.form("conceptual_model"):
    constructs = st.text_area("Enter constructs (comma-separated):", value="A, B, C")
    arrows = st.text_area("Enter relationships (one per line, use A->B format):", value="A->B\nB->C")
    labels = st.text_area("Optional: Label paths (e.g. A->B: H1)", value="A->B: H1\nB->C: H2")
    submit = st.form_submit_button("🎨 Generate Diagram")

if submit:
    # Parse constructs
    construct_list = [c.strip() for c in constructs.split(",") if c.strip()]
    construct_coords = {}
    spacing = 1.5
    for i, c in enumerate(construct_list):
        construct_coords[c] = (i * spacing, 0)

    # Parse relationships
    edges = []
    edge_labels = {}
    for line in arrows.strip().split("\n"):
        if "->" in line:
            src, tgt = [s.strip() for s in line.split("->")]
            edges.append((src, tgt))

    for line in labels.strip().split("\n"):
        if ":" in line:
            path, label = line.split(":", 1)
            edge_labels[path.strip()] = label.strip()

    # Build Plotly figure
    fig = go.Figure()

    # Add nodes
    for name, (x, y) in construct_coords.items():
        fig.add_trace(go.Scatter(
            x=[x], y=[y], mode='markers+text',
            marker=dict(size=60, color='lightblue'),
            text=[name], textposition="middle center",
            hoverinfo='text', showlegend=False
        ))

    # Add arrows
    for (src, tgt) in edges:
        if src not in construct_coords or tgt not in construct_coords:
            continue
        x0, y0 = construct_coords[src]
        x1, y1 = construct_coords[tgt]
        label = edge_labels.get(f"{src}->{tgt}", "")

        # Draw arrow line
        fig.add_annotation(
            x=x1, y=y1, ax=x0, ay=y0,
            xref='x', yref='y', axref='x', ayref='y',
            showarrow=True, arrowhead=3, arrowsize=1.5,
            arrowwidth=2, arrowcolor="gray"
        )

        # Label the arrow
        if label:
            lx = (x0 + x1) / 2
            ly = (y0 + y1) / 2 + 0.3
            fig.add_annotation(
                x=lx, y=ly, text=label, showarrow=False,
                font=dict(size=12, color="black")
            )

    # Final layout
    fig.update_layout(
        height=400,
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis=dict(visible=False), yaxis=dict(visible=False),
        plot_bgcolor="white"
    )

    st.plotly_chart(fig, use_container_width=True)
