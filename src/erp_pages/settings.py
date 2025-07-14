import streamlit as st
import pandas as pd
from datetime import datetime
from utils.translations import t, get_current_language, set_language

def show_settings():
    """Settings Management Page"""
    st.header(f"⚙️ {t('settings')}")
    
    tab1, tab2, tab3, tab4 = st.tabs([t("general"), "Users", "System", t("language")])
    
    with tab1:
        st.subheader("General Settings")
        
        with st.form("general_settings"):
            company_name = st.text_input("Company Name", value="PenzFlow Corp")
            currency = st.selectbox("Currency", ["IDR", "USD", "EUR", "GBP", "JPY"], index=0)
            timezone = st.selectbox("Timezone", ["Asia/Jakarta (GMT+7)", "UTC", "EST", "PST", "GMT"], index=0)
            
            # Business settings
            st.subheader("Business Configuration")
            tax_rate = st.number_input("Default Tax Rate (%)", min_value=0.0, max_value=100.0, value=11.0, step=0.1)
            fiscal_year_start = st.selectbox("Fiscal Year Start", ["January", "April", "July", "October"])
            
            if st.form_submit_button(t("save")):
                st.success(f"{t('success')}!")
    
    with tab4:
        st.subheader(f"🌐 {t('language')} / Language Settings")
        st.write(f"{t('language')} saat ini / Current language: **{get_current_language().upper()}**")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            current_lang = get_current_language()
            lang_options = {
                "🇮🇩 Bahasa Indonesia": "id", 
                "🇺🇸 English": "en"
            }
            
            selected_lang = st.selectbox(
                f"{t('language')} / Language",
                options=list(lang_options.keys()),
                index=0 if current_lang == 'id' else 1,
                help="Pilih bahasa untuk antarmuka aplikasi / Select language for the application interface"
            )
            
            if st.button(f"💾 {t('save')} {t('language')}", use_container_width=True):
                new_lang = lang_options[selected_lang]
                if new_lang != current_lang:
                    set_language(new_lang)
                    st.success(f"✅ {t('language')} berhasil diubah / Language successfully changed!")
                    st.rerun()
                else:
                    st.info(f"ℹ️ {t('language')} sudah dipilih / Language already selected")
        
        with col2:
            st.markdown("### 📋 Language Information")
            st.markdown("""
            **Available Languages:**
            - 🇮🇩 **Bahasa Indonesia** - Default untuk pengguna lokal
            - 🇺🇸 **English** - For international users
            
            **Features:**
            - ✅ Interface translation
            - ✅ Menu navigation
            - ✅ Business terminology
            - ✅ Error messages
            - ✅ FMCG-specific terms
            
            **Note:** Currency and date formats remain in Indonesian standard regardless of language selection.
            """)
    
    with tab2:
        st.subheader("User Management")
        
        # User list
        users_data = {
            'Username': ['admin', 'budi.santoso', 'sari.wulandari', 'ahmad.rahman'],
            'Name': ['Administrator', 'Budi Santoso', 'Sari Wulandari', 'Ahmad Rahman'],
            'Role': ['Administrator', 'Salesman', 'Salesman', 'Sales Manager'],
            'Status': ['Active', 'Active', 'Active', 'Active'],
            'Last Login': ['20-01-2024', '19-01-2024', '20-01-2024', '20-01-2024']
        }
        
        df = pd.DataFrame(users_data)
        st.dataframe(df, use_container_width=True)
        
        # User actions
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("➕ Add User"):
                st.info("Add user feature coming soon!")
        with col2:
            if st.button("✏️ Edit User"):
                st.info("Edit user feature coming soon!")
        with col3:
            if st.button("🗑️ Delete User"):
                st.info("Delete user feature coming soon!")
        
        st.markdown("---")
        st.subheader("Add New User")
        with st.form("add_user"):
            col1, col2 = st.columns(2)
            with col1:
                new_username = st.text_input("Username")
                new_name = st.text_input("Full Name")
                new_role = st.selectbox("Role", ["Administrator", "Sales Manager", "Salesman", "Viewer"])
            with col2:
                new_email = st.text_input("Email")
                new_password = st.text_input("Password", type="password")
                new_phone = st.text_input("Phone Number")
            
            if st.form_submit_button("Add User"):
                if new_username and new_name and new_email and new_password:
                    st.success(f"User '{new_username}' added successfully!")
                else:
                    st.error("Please fill in all required fields")
    
    with tab3:
        st.subheader("System Information")
        
        col1, col2 = st.columns(2)
        with col1:
            st.info("**Version:** 1.0.0")
            st.info("**Database:** SQLite")
            st.info("**Framework:** Streamlit")
            st.info("**Python:** 3.12+")
        
        with col2:
            st.info("**Timezone:** Asia/Jakarta (GMT+7)")
            st.info("**Currency:** Indonesian Rupiah (IDR)")
            st.info("**Tax Rate:** 11% (PPN)")
            st.info("**Locale:** Indonesia")
        
        st.markdown("---")
        st.subheader("System Maintenance")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔄 Clear Cache"):
                st.success("Cache cleared successfully!")
        with col2:
            if st.button("📊 Database Stats"):
                st.info("Database statistics feature coming soon!")
        with col3:
            if st.button("📤 Export Data"):
                st.info("Data export feature coming soon!")
        
        # System logs
        st.subheader("Recent System Activity")
        log_data = {
            'Timestamp': ['2024-01-20 10:30:15', '2024-01-20 09:45:22', '2024-01-20 08:15:45'],
            'User': ['admin', 'budi.santoso', 'sari.wulandari'],
            'Action': ['Settings updated', 'Order created', 'Customer visit logged'],
            'Status': ['✅ Success', '✅ Success', '✅ Success']
        }
        
        df_logs = pd.DataFrame(log_data)
        st.dataframe(df_logs, use_container_width=True)
