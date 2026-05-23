import streamlit as st
import pandas as pd
import plotly.express as px


def show_dashboard(df):

    # =====================================================
    # DATA CLEANING
    # =====================================================

    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )

    # =====================================================
    # CALCULATED COLUMNS
    # =====================================================

    df["Revenue"] = (
        df["Produced Qty"] *
        df["Per Item Price"]
    )

    df["Tonnage"] = (
        df["Produced Qty"] *
        df["CutWt"]
    ) / 1000

    # =====================================================
    # SIDEBAR
    # =====================================================

    st.sidebar.title("Filters")

    # MODULE FILTER

    module_list = sorted(
        df["ModuleName"].dropna().unique()
    )

    selected_module = st.sidebar.selectbox(
        "Select Module / Zone",
        module_list
    )

    filtered_df = df[
        df["ModuleName"] == selected_module
    ]

    # =====================================================
    # DATE FILTER
    # =====================================================

    start_date = st.sidebar.date_input(
        "Start Date",
        filtered_df["Date"].min()
    )

    end_date = st.sidebar.date_input(
        "End Date",
        filtered_df["Date"].max()
    )

    filtered_df = filtered_df[
        (filtered_df["Date"] >= pd.to_datetime(start_date)) &
        (filtered_df["Date"] <= pd.to_datetime(end_date))
    ]

    # =====================================================
    # SHIFT FILTER
    # =====================================================

    shift_list = sorted(
        filtered_df["Shift"].dropna().unique()
    )

    selected_shift = st.sidebar.multiselect(
        "Select Shift",
        shift_list,
        default=shift_list
    )

    filtered_df = filtered_df[
        filtered_df["Shift"].isin(selected_shift)
    ]

    # =====================================================
    # MACHINE FILTER
    # =====================================================

    machine_list = sorted(
        filtered_df["MachineName"].dropna().unique()
    )

    selected_machine = st.sidebar.multiselect(
        "Select Machine",
        machine_list,
        default=machine_list
    )

    filtered_df = filtered_df[
        filtered_df["MachineName"].isin(selected_machine)
    ]

    # =====================================================
    # OPERATOR FILTER
    # =====================================================

    operator_list = sorted(
        filtered_df["OperatorName"].dropna().unique()
    )

    selected_operator = st.sidebar.multiselect(
        "Select Operator",
        operator_list,
        default=operator_list
    )

    filtered_df = filtered_df[
        filtered_df["OperatorName"].isin(selected_operator)
    ]

    # =====================================================
    # KPI CALCULATIONS
    # =====================================================

    total_qty = filtered_df["Produced Qty"].sum()

    total_revenue = filtered_df["Revenue"].sum()

    total_tonnage = filtered_df["Tonnage"].sum()

    total_orders = filtered_df["Order Qty"].sum()

    achievement = 0

    if total_orders > 0:

        achievement = (
            total_qty / total_orders
        ) * 100

    active_machines = (
        filtered_df["MachineName"]
        .nunique()
    )

    active_operators = (
        filtered_df["OperatorName"]
        .nunique()
    )

    # =====================================================
    # TITLE
    # =====================================================

    st.title("Machining Analytics Dashboard")

    st.subheader(
        f"Zone : {selected_module}"
    )

    # =====================================================
    # KPI SECTION
    # =====================================================

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Produced Qty",
        f"{total_qty:,.0f}"
    )

    col2.metric(
        "Revenue",
        f"₹ {total_revenue:,.0f}"
    )

    col3.metric(
        "Tonnage",
        f"{total_tonnage:,.2f} Ton"
    )

    col4, col5, col6 = st.columns(3)

    col4.metric(
        "Achievement %",
        f"{achievement:.1f}%"
    )

    col5.metric(
        "Active Machines",
        active_machines
    )

    col6.metric(
        "Active Operators",
        active_operators
    )

    st.divider()

    # =====================================================
    # MACHINE ANALYTICS
    # =====================================================

    col1, col2 = st.columns(2)

    with col1:

        machine_prod = (
            filtered_df.groupby("MachineName")
            ["Produced Qty"]
            .sum()
            .reset_index()
            .sort_values(
                by="Produced Qty",
                ascending=False
            )
        )

        fig_machine = px.bar(
            machine_prod,
            x="MachineName",
            y="Produced Qty",
            color="Produced Qty",
            title="Machine-wise Production"
        )

        st.plotly_chart(
            fig_machine,
            use_container_width=True
        )

    with col2:

        machine_revenue = (
            filtered_df.groupby("MachineName")
            ["Revenue"]
            .sum()
            .reset_index()
        )

        fig_machine_rev = px.bar(
            machine_revenue,
            x="MachineName",
            y="Revenue",
            color="Revenue",
            title="Machine-wise Revenue"
        )

        st.plotly_chart(
            fig_machine_rev,
            use_container_width=True
        )

    # =====================================================
    # OPERATOR ANALYTICS
    # =====================================================

    col1, col2 = st.columns(2)

    with col1:

        operator_prod = (
            filtered_df.groupby("OperatorName")
            ["Produced Qty"]
            .sum()
            .reset_index()
        )

        fig_operator = px.bar(
            operator_prod,
            x="OperatorName",
            y="Produced Qty",
            color="Produced Qty",
            title="Operator-wise Production"
        )

        st.plotly_chart(
            fig_operator,
            use_container_width=True
        )

    with col2:

        operator_revenue = (
            filtered_df.groupby("OperatorName")
            ["Revenue"]
            .sum()
            .reset_index()
        )

        fig_operator_rev = px.pie(
            operator_revenue,
            names="OperatorName",
            values="Revenue",
            hole=0.5,
            title="Operator Revenue Contribution"
        )

        st.plotly_chart(
            fig_operator_rev,
            use_container_width=True
        )

    # =====================================================
    # DAILY TREND
    # =====================================================

    daily_prod = (
        filtered_df.groupby("Date")
        ["Produced Qty"]
        .sum()
        .reset_index()
    )

    fig_daily = px.line(
        daily_prod,
        x="Date",
        y="Produced Qty",
        markers=True,
        title="Daily Production Trend"
    )

    st.plotly_chart(
        fig_daily,
        use_container_width=True
    )

    # =====================================================
    # RAW DATA
    # =====================================================

    st.divider()

    st.subheader("Production Data")

    st.dataframe(
        filtered_df,
        use_container_width=True
    )