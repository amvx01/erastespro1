# Simpan kode di sini

import streamlit as st
from sqlalchemy import text

list_ticket_types = ['', 'VIP', 'General Admission']

conn = st.connection("postgresql", type="sql", 
                     url="postgresql://linomanusia:q7meCLNZvw4P@ep-wandering-boat-05196099.us-east-2.aws.neon.tech/etsets")

st.header('TAYLOR SWIFT ERAS TOUR TICKET MANAGEMENT')
page = st.sidebar.selectbox("Select Menu", ["View Tickets", "Edit Tickets"])

if page == "View Tickets":
    data = conn.query('SELECT * FROM concert_tickets ORDER BY ticket_id;', ttl="0").set_index('ticket_id')
    st.dataframe(data)

if page == "Edit Tickets":
    if st.button('Add Ticket'):
        with conn.session as session:
            query = text('INSERT INTO concert_tickets (concert_name, ticket_type, price, buyer_name, email, phone_number, purchase_date) \
                          VALUES (:1, :2, :3, :4, :5, :6, :7);')
            session.execute(query, {'1':'Taylor Swift Eras Tour', '2':'', '3':0.0, '4':'', '5':'', '6':'', '7':None})
            session.commit()

    data = conn.query('SELECT * FROM concert_tickets ORDER BY ticket_id;', ttl="0")
    for _, result in data.iterrows():        
        ticket_id = result['ticket_id']
        concert_name_lama = result["concert_name"]
        ticket_type_lama = result["ticket_type"]
        price_lama = result["price"]
        buyer_name_lama = result["buyer_name"]
        email_lama = result["email"]
        phone_number_lama = result["phone_number"]
        purchase_date_lama = result["purchase_date"]

        with st.expander(f'Ticket ID: {ticket_id}'):
            with st.form(f'ticket-{ticket_id}'):
                ticket_type_baru = st.selectbox("Ticket Type", list_ticket_types, list_ticket_types.index(ticket_type_lama))
                price_baru = st.number_input("Price", value=float(price_lama))
                buyer_name_baru = st.text_input("Buyer Name", buyer_name_lama)
                email_baru = st.text_input("Email", email_lama)
                phone_number_baru = st.text_input("Phone Number", phone_number_lama)
                purchase_date_baru = st.date_input("Purchase Date", purchase_date_lama)
                
                if st.form_submit_button('Update Ticket'):
                    with conn.session as session:
                        query = text('UPDATE concert_tickets \
                                      SET ticket_type=:1, price=:2, buyer_name=:3, email=:4, phone_number=:5, purchase_date=:6 \
                                      WHERE ticket_id=:7;')
                        session.execute(query, {'1':ticket_type_baru, '2':price_baru, '3':buyer_name_baru, '4':email_baru, 
                                                '5':phone_number_baru, '6':purchase_date_baru, '7':ticket_id})
                        session.commit()
                        st.experimental_rerun()
                
                if st.form_submit_button('Delete Ticket'):
                    with conn.session as session:
                        query = text('DELETE FROM concert_tickets WHERE ticket_id=:1;')
                        session.execute(query, {'1':ticket_id})
                        session.commit()
                        st.experimental_rerun()
