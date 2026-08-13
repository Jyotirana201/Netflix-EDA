import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined"
rel="stylesheet">
""", unsafe_allow_html=True)
# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Netflix Explorer",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

html, body {
    background-color: #080808 !important;
}

.stApp {
    background-color: #080808 !important;
    color: white !important;
}

/* Remove Streamlit top white/header area */
header[data-testid="stHeader"] {
    background-color: #080808 !important;
}

div[data-testid="stAppViewContainer"] {
    background-color: #080808 !important;
}

div[data-testid="stMain"] {
    background-color: #080808 !important;
}

            
/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #050505 !important;
    border-right: 1px solid #292929;
}

section[data-testid="stSidebar"] > div {
    background-color: #050505 !important;
}


/* Netflix logo */
.netflix-logo {
    color: #E50914;
    font-size: 38px;
    font-weight: 900;
    letter-spacing: 2px;
    margin-top: 10px;
    margin-bottom: 30px;
}


/* Sidebar menu */
.menu-title {
    color: #E50914;
    font-size: 13px;
    font-weight: bold;
    letter-spacing: 1px;
    margin-bottom: 10px;
}


/* Sidebar radio buttons */
section[data-testid="stSidebar"] label {
    color: #eeeeee !important;
}

div[role="radiogroup"] label {
    background-color: transparent;
    border-radius: 8px;
    padding: 8px;
}

div[role="radiogroup"] label:hover {
    background-color: #191919;
}


/* Main heading */
.main-title {
    font-size: 42px;
    font-weight: 900;
    letter-spacing: 1px;
    color: #ffffff;
    margin-top: 0px;
    margin-bottom: 5px;
}

.main-title span {
    color: #E50914;
}

.subtitle {
    color: #999999;
    font-size: 17px;
    margin-bottom: 28px;
}


/* Metric cards */
.metric-card {
    background: linear-gradient(
        145deg,
        #191919,
        #0d0d0d
    );

    border: 1px solid #292929;
    border-radius: 15px;

    padding: 18px;

    min-height: 105px;

    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.35);
}

.metric-card:hover {
    border-color: #E50914;
}

.metric-icon {
    font-size: 25px;
    float: left;
    margin-right: 12px;
}

.metric-title {
    color: #cecece;
    font-size: 18px;
    padding-top: 3px;
}

.metric-value {
    color: #E50914;
    font-size: 30px;
    font-weight: 800;
    margin-top: 7px;
}
            
.metric-icon {
    font-size: 28px;
    color: #E50914;
    float: left;
    margin-right: 12px;
    width: 35px;
}

.material-symbols-outlined {
    font-size: 28px;
}


/* Footer */
.footer {
    text-align: center;
    color: #666666;
    font-size: 13px;
    padding: 25px;
}

.footer span {
    color: #E50914;
}


/* Hide Streamlit branding */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    data = pd.read_csv("netflix_titles.csv")

    # Convert date_added
    data["date_added"] = pd.to_datetime(
        data["date_added"],
        errors="coerce"
    )

    # Year added
    data["year_added"] = data["date_added"].dt.year

    # Movie duration in minutes
    data["duration_minutes"] = (
        data["duration"]
        .str.extract(r"(\d+)")
        .astype(float)
    )

    # TV show seasons
    data["duration_seasons"] = (
        data["duration"]
        .str.extract(r"(\d+)")
        .astype(float)
    )

    return data


df = load_data()


# ============================================================
# BASIC STATISTICS
# ============================================================

total_titles = len(df)

total_movies = (
    df["type"] == "Movie"
).sum()

total_tv_shows = (
    df["type"] == "TV Show"
).sum()

total_countries = (
    df["country"]
    .dropna()
    .str.split(", ")
    .explode()
    .nunique()
)


# ============================================================
# CHART STYLE
# ============================================================

def style_chart(fig, height=400):

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#111111",
        plot_bgcolor="#111111",
        font=dict(
            color="#f3f5ee"
        ),
        height=height,
        margin=dict(
            l=45,
            r=25,
            t=60,
            b=45
        ),
        title_font=dict(
            size=20,
            color="#ffffff"
        ),
        hoverlabel=dict(
            bgcolor="#1a1a1a",
            font_color="#ffffff"
        )
    )

    return fig


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="netflix-logo">NETFLIX</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="menu-title">MENU</div>',
        unsafe_allow_html=True
    )

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Movies vs TV Shows",
            "Content Added by Year",
            "Ratings Distribution",
            "Top Genres",
            "Top Countries",
            "Movie Duration",
            "TV Show Seasons"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.markdown(
        """
        <div style="
            color:#777777;
            font-size:13px;
            line-height:1.6;
        ">
            <span style="color:#E50914;">
            Netflix Explorer
            </span>
            <br>
            Exploratory Data Analysis
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="main-title">
            NETFLIX <span>EXPLORER</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="subtitle">
            Explore Netflix Movies & TV Shows through data
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(
    f"""
    <div class="metric-card">
        <div class="metric-icon">
            <span class="material-symbols-outlined">video_library</span>
        </div>
        <div class="metric-title">Total Titles</div>
        <div class="metric-value">{total_titles:,}</div>
    </div>
    """,
    unsafe_allow_html=True
)

    with col2:

        st.markdown(
    f"""
    <div class="metric-card">
        <div class="metric-icon">
            <span class="material-symbols-outlined">movie</span>
        </div>
        <div class="metric-title">Movies</div>
        <div class="metric-value">{total_movies:,}</div>
    </div>
    """,
    unsafe_allow_html=True
)

    with col3:

        st.markdown(
    f"""
    <div class="metric-card">
        <div class="metric-icon">
            <span class="material-symbols-outlined">tv</span>
        </div>
        <div class="metric-title">TV Shows</div>
        <div class="metric-value">{total_tv_shows:,}</div>
    </div>
    """,
    unsafe_allow_html=True
)

    with col4:

        st.markdown(
    f"""
    <div class="metric-card">
        <div class="metric-icon">
            <span class="material-symbols-outlined">public</span>
        </div>
        <div class="metric-title">Countries</div>
        <div class="metric-value">{total_countries:,}</div>
    </div>
    """,
    unsafe_allow_html=True
)


    st.markdown("<br>", unsafe_allow_html=True)


    # ========================================================
    # ROW 1
    # ========================================================

    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # MOVIES VS TV SHOWS
    # --------------------------------------------------------

    with col1:

        type_count = df["type"].value_counts()

        fig = go.Figure(
            data=[
                go.Pie(
                    labels=type_count.index,
                    values=type_count.values,
                    hole=0.58,

                    marker=dict(
                        colors=[
                            "#E50914",
                            "#444444"
                        ]
                    ),

                    textinfo="label+percent",

                    hovertemplate=
                    "<b>%{label}</b><br>"
                    "Titles: %{value:,}<br>"
                    "Percentage: %{percent}"
                    "<extra></extra>"
                )
            ]
        )

        fig.update_layout(
            title="Movies vs TV Shows",
            template="plotly_dark",
            paper_bgcolor="#111111",
            plot_bgcolor="#111111",
            font=dict(color="white"),
            height=390,
            margin=dict(
                l=20,
                r=20,
                t=60,
                b=20
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # --------------------------------------------------------
    # CONTENT ADDED BY YEAR
    # --------------------------------------------------------

    with col2:

        yearly = (
            df["year_added"]
            .dropna()
            .astype(int)
            .value_counts()
            .sort_index()
        )

        fig = px.line(
            x=yearly.index,
            y=yearly.values,
            markers=True,
            title="Content Added by Year",
            labels={
                "x": "Year",
                "y": "Number of Titles"
            }
        )

        fig.update_traces(
            line=dict(
                color="#E50914",
                width=3
            ),
            marker=dict(
                color="#E50914",
                size=7
            )
        )

        style_chart(fig, 390)

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # ========================================================
    # ROW 2
    # ========================================================

    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # TOP GENRES
    # --------------------------------------------------------

    with col1:

        genres = (
            df["listed_in"]
            .dropna()
            .str.split(", ")
            .explode()
            .value_counts()
            .head(10)
            .sort_values()
        )

        fig = px.bar(
            x=genres.values,
            y=genres.index,
            orientation="h",
            title="Top 10 Genres",
            labels={
                "x": "Number of Titles",
                "y": "Genre"
            }
        )

        fig.update_traces(
            marker_color="#E50914"
        )

        style_chart(fig, 420)

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # --------------------------------------------------------
    # TOP COUNTRIES
    # --------------------------------------------------------

    with col2:

        countries = (
            df["country"]
            .dropna()
            .str.split(", ")
            .explode()
            .value_counts()
            .head(10)
            .sort_values()
        )

        fig = px.bar(
            x=countries.values,
            y=countries.index,
            orientation="h",
            title="Top 10 Countries",
            labels={
                "x": "Number of Titles",
                "y": "Country"
            }
        )

        fig.update_traces(
            marker_color="#E50914"
        )

        style_chart(fig, 420)

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # ========================================================
    # ROW 3
    # ========================================================

    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # MOVIE DURATION
    # --------------------------------------------------------

    with col1:

        movie_duration = (
            df[
                df["type"] == "Movie"
            ]["duration_minutes"]
            .dropna()
        )

        fig = px.histogram(
            movie_duration,
            x="duration_minutes",
            nbins=30,
            title="Movie Duration",
            labels={
                "duration_minutes":
                "Duration (Minutes)"
            }
        )

        fig.update_traces(
            marker_color="#E50914"
        )

        style_chart(fig, 400)

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # --------------------------------------------------------
    # TV SHOW SEASONS
    # --------------------------------------------------------

    with col2:

        seasons = (
            df[
                df["type"] == "TV Show"
            ]["duration_seasons"]
            .dropna()
            .value_counts()
            .sort_index()
        )

        fig = px.bar(
            x=seasons.index,
            y=seasons.values,
            title="TV Show Seasons",
            labels={
                "x": "Number of Seasons",
                "y": "Number of TV Shows"
            }
        )

        fig.update_traces(
            marker_color="#E50914"
        )

        style_chart(fig, 400)

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# MOVIES VS TV SHOWS
# ============================================================

elif page == "Movies vs TV Shows":

    st.markdown(
        """
        <div class="main-title">
            Movies <span>vs TV Shows</span>
        </div>

        <div class="subtitle">
            Distribution of Netflix content by type
        </div>
        """,
        unsafe_allow_html=True
    )

    type_count = df["type"].value_counts()

    fig = go.Figure(
        data=[
            go.Pie(
                labels=type_count.index,
                values=type_count.values,
                hole=0.60,
                marker=dict(
                    colors=[
                        "#E50914",
                        "#444444"
                    ]
                ),
                textinfo="label+percent"
            )
        ]
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#111111",
        plot_bgcolor="#111111",
        height=550,
        title="Movies vs TV Shows"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# CONTENT ADDED BY YEAR
# ============================================================

elif page == "Content Added by Year":

    st.markdown(
        """
        <div class="main-title">
            Content Added <span>by Year</span>
        </div>

        <div class="subtitle">
            Netflix content added over time
        </div>
        """,
        unsafe_allow_html=True
    )

    yearly = (
        df["year_added"]
        .dropna()
        .astype(int)
        .value_counts()
        .sort_index()
    )

    fig = px.line(
        x=yearly.index,
        y=yearly.values,
        markers=True,
        title="Netflix Content Added Over Time",
        labels={
            "x": "Year",
            "y": "Number of Titles"
        }
    )

    fig.update_traces(
        line=dict(
            color="#E50914",
            width=4
        ),
        marker=dict(
            color="#E50914",
            size=8
        )
    )

    style_chart(fig, 550)

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# RATINGS
# ============================================================

elif page == "Ratings Distribution":

    st.markdown(
        """
        <div class="main-title">
            Ratings <span>Distribution</span>
        </div>

        <div class="subtitle">
            Most common ratings in the Netflix dataset
        </div>
        """,
        unsafe_allow_html=True
    )

    ratings = (
        df["rating"]
        .dropna()
        .value_counts()
        .head(12)
        .sort_values()
    )

    fig = px.bar(
        x=ratings.values,
        y=ratings.index,
        orientation="h",
        title="Most Common Netflix Ratings",
        labels={
            "x": "Number of Titles",
            "y": "Rating"
        }
    )

    fig.update_traces(
        marker_color="#E50914"
    )

    style_chart(fig, 550)

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# TOP GENRES
# ============================================================

elif page == "Top Genres":

    st.markdown(
        """
        <div class="main-title">
            Top <span>Genres</span>
        </div>

        <div class="subtitle">
            Most common genres available on Netflix
        </div>
        """,
        unsafe_allow_html=True
    )

    genres = (
        df["listed_in"]
        .dropna()
        .str.split(", ")
        .explode()
        .value_counts()
        .head(15)
        .sort_values()
    )

    fig = px.bar(
        x=genres.values,
        y=genres.index,
        orientation="h",
        title="Top 15 Netflix Genres",
        labels={
            "x": "Number of Titles",
            "y": "Genre"
        }
    )

    fig.update_traces(
        marker_color="#E50914"
    )

    style_chart(fig, 600)

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# TOP COUNTRIES
# ============================================================

elif page == "Top Countries":

    st.markdown(
        """
        <div class="main-title">
            Top <span>Countries</span>
        </div>

        <div class="subtitle">
            Countries represented in the Netflix dataset
        </div>
        """,
        unsafe_allow_html=True
    )

    countries = (
        df["country"]
        .dropna()
        .str.split(", ")
        .explode()
        .value_counts()
        .head(15)
        .sort_values()
    )

    fig = px.bar(
        x=countries.values,
        y=countries.index,
        orientation="h",
        title="Top 15 Countries",
        labels={
            "x": "Number of Titles",
            "y": "Country"
        }
    )

    fig.update_traces(
        marker_color="#E50914"
    )

    style_chart(fig, 600)

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# MOVIE DURATION
# ============================================================

elif page == "Movie Duration":

    st.markdown(
        """
        <div class="main-title">
            Movie <span>Duration</span>
        </div>

        <div class="subtitle">
            Distribution of movie durations
        </div>
        """,
        unsafe_allow_html=True
    )

    movie_duration = (
        df[
            df["type"] == "Movie"
        ]["duration_minutes"]
        .dropna()
    )

    fig = px.histogram(
        movie_duration,
        x="duration_minutes",
        nbins=35,
        title="Distribution of Movie Durations",
        labels={
            "duration_minutes":
            "Duration (Minutes)"
        }
    )

    fig.update_traces(
        marker_color="#E50914"
    )

    style_chart(fig, 550)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.metric(
        "Average Movie Duration",
        f"{movie_duration.mean():.1f} minutes"
    )


# ============================================================
# TV SHOW SEASONS
# ============================================================

elif page == "TV Show Seasons":

    st.markdown(
        """
        <div class="main-title">
            TV Show <span>Seasons</span>
        </div>

        <div class="subtitle">
            Distribution of TV shows by number of seasons
        </div>
        """,
        unsafe_allow_html=True
    )

    seasons = (
        df[
            df["type"] == "TV Show"
        ]["duration_seasons"]
        .dropna()
        .value_counts()
        .sort_index()
    )

    fig = px.bar(
        x=seasons.index,
        y=seasons.values,
        title="TV Shows by Number of Seasons",
        labels={
            "x": "Number of Seasons",
            "y": "Number of TV Shows"
        }
    )

    fig.update_traces(
        marker_color="#E50914"
    )

    style_chart(fig, 550)

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        Netflix Explorer |
        <span>Exploratory Data Analysis</span>
        using Python, Pandas, Plotly & Streamlit
    </div>
    """,
    unsafe_allow_html=True
)