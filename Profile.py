import streamlit as st
page_bg_img = '''
<style>
[data-testid="stSidebarContent"]{
    background: linear-gradient(0deg, #588EAD 0%, #151414 100%);   
}
.reportview-container {
    background: url("https://images.unsplash.com/photo-1487147264018-f937fba0c817");
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)
def main():
    st.title("YOUR LEGIT Profile")

    # Check if profile data is already set
    if 'profile_data' not in st.session_state:
        st.session_state.profile_data = {
            'name': None,
            'email': None,
            'bio': None
        }

    # Display profile form
    st.header("Edit Profile")
    name = st.text_input("Name", st.session_state.profile_data['name'])
    email = st.text_input("Email", st.session_state.profile_data['email'])
    bio = st.text_area("Bio", st.session_state.profile_data['bio'])

    if st.button("Save Profile"):
        # Update session state with new profile data
        st.session_state.profile_data['name'] = name
        st.session_state.profile_data['email'] = email
        st.session_state.profile_data['bio'] = bio

        st.success("Profile updated successfully!")

    # Display user's profile
    st.header("Your Profile")
    st.write(f"**Name:** {st.session_state.profile_data['name']}")
    st.write(f"**Email:** {st.session_state.profile_data['email']}")
    st.write(f"**Bio:** {st.session_state.profile_data['bio']}")

    if st.button("Back to HOME"):
        st.experimental_rerun()
if __name__ == '__main__':
    main()
