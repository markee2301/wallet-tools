import json
import pandas as pd
import streamlit as st
import webbrowser

# Title of the app
st.title("Wallet Tools by MARK")

# Define two functions for clarity
def wallet_scraper():
    # Upload the JSON file
    uploaded_file = st.file_uploader("Wallet Extractor", type=["json"])

    if uploaded_file is not None:
        try:
            # Load JSON data
            data = json.load(uploaded_file)
            # Navigate to the list under "byRealizedProfit"
            realized_profit_data = data.get("data", {}).get("byRealizedProfit", [])

            if realized_profit_data:
                # Extract addresses
                addresses = [entry.get('address') for entry in realized_profit_data if isinstance(entry, dict)]

                # Create a DataFrame
                df = pd.DataFrame(addresses, columns=['Wallet Address'])

                # Input token name
                token_name = st.text_input("Enter the token name for the Excel file.", placeholder="Enter token name")

                if token_name:
                    # Export to Excel
                    excel_filename = f'{token_name}.xlsx'
                    df.to_excel(excel_filename, index=False)

                    # Download the Excel file
                    with open(excel_filename, "rb") as file:
                        st.download_button(
                            label="Download Excel file",
                            data=file,
                            file_name=excel_filename,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                    st.success(f"Addresses have been successfully exported to {excel_filename}.")
                else:
                    st.warning("Enter a token name to save the Excel file.")
            else:
                st.warning("No data found.")
        except json.JSONDecodeError as e:
            st.error(f"Error decoding JSON: {e}")


def wallet_explorer():
    # Replace this with your desired base URL
    base_url = "https://app.cielo.finance/profile/{wallet_address}/pnl/tokens"

    def append_wallet_address(wallet_address):
        """Appends the provided wallet address to the static base URL."""
        return base_url.format(wallet_address=wallet_address)

    # File uploader for Excel file
    uploaded_file = st.file_uploader("Wallet Explorer", type=["xlsx"])

    if uploaded_file is not None:
        # Read Excel file into a DataFrame
        df = pd.read_excel(uploaded_file)

        if not df.empty:  # Check if DataFrame is not empty
            for index, row in df.iterrows():
                try:
                    # Use the correct column name
                    wallet_address = row['Wallet Address']
                    complete_url = append_wallet_address(wallet_address)

                    # Display wallet address and button in one line
                    col1, col2 = st.columns([8, 2])
                    col1.write(f"{wallet_address}", unsafe_allow_html=True)
                    with col2:
                        st.button(f"View Wallet {index + 1}", key=wallet_address,
                                  on_click=lambda url=complete_url: webbrowser.open(url, new=2),
                                  use_container_width=True)

                except KeyError:
                    st.error(f"Error processing row {index+1}: 'Wallet Address' column not found.")
        else:
            st.error("The uploaded file is empty or doesn't contain any data.")


# Display both functionalities side-by-side
st.columns([1, 1])  # Two columns with equal width
with st.container():
    wallet_scraper()
with st.container():
    wallet_explorer()