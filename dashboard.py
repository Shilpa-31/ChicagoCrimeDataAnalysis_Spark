import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from folium.plugins import HeatMap
from sqlalchemy import create_engine
from streamlit_folium import folium_static
from config.aws_config import POSTGRESQL_CONFIG

class CrimeDashboard:
    def __init__(self):
        self.df = self.load_data()
        # Normalize column names
        self.df.columns = self.df.columns.str.strip().str.lower().str.replace(" ", "_")
        self.df.dropna(subset=['latitude', 'longitude'], inplace=True)

    @staticmethod
    @st.cache_data
    def load_data():
        from config.aws_config import POSTGRESQL_CONFIG
        db_url = POSTGRESQL_CONFIG['url'].replace('jdbc:', '')
        url = f"postgresql://{POSTGRESQL_CONFIG['user']}:{POSTGRESQL_CONFIG['password']}@{db_url.split('//')[1]}"
        engine = create_engine(url)
        df = pd.read_sql("SELECT * FROM analysed_chicago_crime_data", con=engine)
        return df

    def filter_data(self):
        st.sidebar.header("🔍 Filter Options:")

        crime_types = self.df['primary_type'].dropna().unique().tolist()
        selected_types = st.sidebar.multiselect("Crime Type Filter:", crime_types, default=crime_types)

        filtered = self.df[self.df['primary_type'].isin(selected_types)]
        return filtered

    def show_crime_trends(self, df):
        st.subheader("📈 Crime Trends Over Time")
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.dropna(subset=['date'])

        monthly = df.groupby(df['date'].dt.to_period("M")).size().reset_index(name='count')
        monthly['date'] = monthly['date'].astype(str)

        fig = px.line(monthly, x='date', y='count', markers=True, title="Crime Trends")
        st.plotly_chart(fig, use_container_width=True)

    def show_crime_categories(self, df):
        st.subheader("🔍 Crime Type Distribution")
        type_counts = df.groupby('primary_type').size().reset_index(name='count')
        fig = px.bar(type_counts, x='primary_type', y='count', color='primary_type', title="Crime Type")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("🏙️ Crime Type Distrubution by Location")
        loc_counts = df.groupby('location_description').size().reset_index(name='count')
        fig2 = px.bar(loc_counts, x='location_description', y='count', color='location_description', title="Crime by Location")
        st.plotly_chart(fig2, use_container_width=True)

    def show_geospatial_heatmap(self, df):
        st.subheader("🗺️ Chicago Crime Heatmap with Details")

        # Drop rows without coordinates
        heat_df = df[['latitude', 'longitude', 'primary_type', 'location_description']].dropna()

        # Downsample if too large
        if len(heat_df) > 10000:
            heat_df = heat_df.sample(10000, random_state=42)
            st.info("🔄 Displaying a random sample of 10,000 points for performance.")
            
            heat_data = heat_df[['latitude', 'longitude']].values.tolist()
            st.write(f"📌 Heatmap data points used: {len(heat_data)}")

        # Create base map
        m = folium.Map(location=[41.8781, -87.6298], zoom_start=11)

        # Add heatmap layer
        HeatMap(heat_data, radius=10, blur=15).add_to(m)

        # Add optional CircleMarkers for extra info
        for _, row in heat_df.iterrows():
            folium.CircleMarker(
                  location=(row['latitude'], row['longitude']),
                  radius=3,
                  color='red',
                  fill=True,
                  fill_opacity=0.7,
                  popup=folium.Popup(
                        f"<b>Type:</b> {row['primary_type']}<br><b>Location:</b> {row['location_description']}",
                        max_width=300
            ),
        ).add_to(m)

        # Show map
        folium_static(m, width=900, height=600)


    def run(self):
        st.title("---- Chicago Crime Dashboard ----")
        filtered_df = self.filter_data()

        if filtered_df.empty:
            st.warning("No records found with current filters.")
            return

        self.show_crime_trends(filtered_df)
        self.show_crime_categories(filtered_df)
        self.show_geospatial_heatmap(filtered_df)

# Entry point
if __name__ == "__main__":
    app = CrimeDashboard()
    app.run()
