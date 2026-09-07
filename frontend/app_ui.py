import streamlit as st
import requests

API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Course Enrollment Portal", page_icon="🎓", layout="wide")


st.markdown("""
    <style>
    .block-container { padding-top: 2rem; }
    div[data-testid="stMetricValue"] { font-size: 1.8rem; }
    </style>
""", unsafe_allow_html=True)

st.title("🎓 Course Enrollment Dashboard")
st.caption("Manage students, courses, and active enrollments seamlessly.")

col1, col2, col3 = st.columns(3)
with col1:
    try:
        s_res = requests.get(f"{API_BASE_URL}/students/").json()
        st.metric("Total Students Registered", len(s_res))
    except:
        st.metric("Total Students Registered", "N/A")

with col2:
    try:
        c_res = requests.get(f"{API_BASE_URL}/courses/available").json()
        st.metric("Available Courses", len(c_res))
    except:
        st.metric("Available Courses", "N/A")

with col3:
    try:
        e_res = requests.get(f"{API_BASE_URL}/enrollment/").json()
        st.metric("Active Enrollments", len(e_res))
    except:
        st.metric("Active Enrollments", "N/A")

st.divider()

section = st.sidebar.selectbox(
    "📌 Navigation Menu",
    ["📊 Dashboard Overview", "👤 Manage Students", "📚 Manage Courses", "📝 Manage Enrollments"]
)


if section == "📊 Dashboard Overview":
    st.header("📊 System Overview")
    st.write("Welcome to the Course Enrollment Portal. Use the navigation panel on the left to manage resources.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Recent Enrollments")
        try:
            res = requests.get(f"{API_BASE_URL}/enrollment/")
            if res.status_code == 200:
                st.dataframe(res.json(), use_container_width=True)
        except Exception as e:
            st.error("Backend offline. Please start Uvicorn server.")

    with col_b:
        st.subheader("Courses with Available Seats")
        try:
            res = requests.get(f"{API_BASE_URL}/courses/available")
            if res.status_code == 200:
                st.dataframe(res.json(), use_container_width=True)
        except Exception as e:
            st.error("Backend offline. Please start Uvicorn server.")



elif section == "👤 Manage Students":
    st.header("👤 Student Management")
    
    col_left, col_right = st.columns([1.5, 1])
    
    with col_left:
        st.subheader("Student Database")
        
        with st.expander("🔍 Search Student by ID"):
            search_id = st.number_input("Student ID", min_value=1, step=1, key="s_search_id")
            if st.button("Search Student"):
                res = requests.get(f"{API_BASE_URL}/students/{search_id}")
                if res.status_code == 200:
                    st.json(res.json())
                else:
                    st.error(res.json().get("detail", "Student not found."))
        
        if st.button("🔄 Refresh Student List", use_container_width=True):
            st.rerun()
            
        res = requests.get(f"{API_BASE_URL}/students/")
        if res.status_code == 200:
            st.dataframe(res.json(), use_container_width=True)
        else:
            st.error("Unable to load students.")


    with col_right:
        # Create Student (POST /students/)
        with st.expander("➕ Register New Student", expanded=True):
            name = st.text_input("Full Name", key="s_add_name")
            email = st.text_input("Email Address", key="s_add_email")
            if st.button("Submit Registration", use_container_width=True):
                res = requests.post(f"{API_BASE_URL}/students/", json={"name": name, "email": email})
                if res.status_code == 201:
                    st.success("Student added successfully!")
                    st.rerun()
                else:
                    st.error(res.json().get("detail", "Error creating student."))

        with st.expander("✏️ Update Student Details"):
            up_id = st.number_input("Student ID to Update", min_value=1, step=1, key="s_up_id")
            up_name = st.text_input("New Name (Optional)", key="s_up_name")
            up_email = st.text_input("New Email (Optional)", key="s_up_email")
            if st.button("Update Student", use_container_width=True):
                payload = {}
                if up_name: payload["name"] = up_name
                if up_email: payload["email"] = up_email
                res = requests.put(f"{API_BASE_URL}/students/{up_id}", json=payload)
                if res.status_code == 200:
                    st.success("Student updated successfully!")
                    st.rerun()
                else:
                    st.error(res.json().get("detail", "Update failed."))

    
        with st.expander("🗑️ Delete Student"):
            del_id = st.number_input("Student ID to Delete", min_value=1, step=1, key="s_del_id")
            if st.button("Delete Student", type="primary", use_container_width=True):
                res = requests.delete(f"{API_BASE_URL}/students/{del_id}")
                if res.status_code == 204:
                    st.success(f"Student ID {del_id} deleted.")
                    st.rerun()
                else:
                    st.error(res.json().get("detail", "Delete failed."))


elif section == "📚 Manage Courses":
    st.header("📚 Course Management")
    
    col_left, col_right = st.columns([1.5, 1])
    
    # Left Column: View & Filters
    with col_left:
        st.subheader("Courses Catalog")
        
        c_filter = st.radio("Filter View", ["All Courses", "Available Courses Only"], horizontal=True)
        
        # Search Course by ID (GET /courses/{course_id})
        with st.expander("🔍 Search Course by ID"):
            c_search_id = st.number_input("Course ID", min_value=1, step=1, key="c_search_id")
            if st.button("Search Course"):
                res = requests.get(f"{API_BASE_URL}/courses/{c_search_id}")
                if res.status_code == 200:
                    st.json(res.json())
                else:
                    st.error(res.json().get("detail", "Course not found."))

        # GET /courses/ or GET /courses/available
        if c_filter == "Available Courses Only":
            res = requests.get(f"{API_BASE_URL}/courses/available")
        else:
            res = requests.get(f"{API_BASE_URL}/courses/")
            
        if res.status_code == 200:
            st.dataframe(res.json(), use_container_width=True)
        else:
            st.error("Unable to load courses.")

    # Right Column: Actions (Create, Update, Delete)
    with col_right:
        # Create Course (POST /courses/)
        with st.expander("➕ Create New Course", expanded=True):
            title = st.text_input("Course Title", key="c_add_title")
            inst = st.text_input("Instructor Name", key="c_add_inst")
            cap = st.number_input("Seat Capacity", min_value=1, step=1, key="c_add_cap")
            fee = st.number_input("Course Fee ($)", min_value=0.0, step=10.0, key="c_add_fee")
            if st.button("Create Course", use_container_width=True):
                payload = {"title": title, "instructor": inst, "capacity": int(cap), "fee": float(fee)}
                res = requests.post(f"{API_BASE_URL}/courses/", json=payload)
                if res.status_code == 201:
                    st.success("Course created!")
                    st.rerun()
                else:
                    st.error(res.json().get("detail", "Error creating course."))

        # Update Course (PUT /courses/{course_id})
        with st.expander("✏️ Update Course Details"):
            u_c_id = st.number_input("Course ID to Update", min_value=1, step=1, key="c_up_id")
            u_title = st.text_input("New Title (Optional)", key="c_up_title")
            u_inst = st.text_input("New Instructor (Optional)", key="c_up_inst")
            u_cap = st.number_input("New Capacity (Optional, 0 to keep)", min_value=0, step=1, key="c_up_cap")
            u_fee = st.number_input("New Fee (Optional, 0 to keep)", min_value=0.0, step=10.0, key="c_up_fee")
            if st.button("Update Course", use_container_width=True):
                payload = {}
                if u_title: payload["title"] = u_title
                if u_inst: payload["instructor"] = u_inst
                if u_cap > 0: payload["capacity"] = int(u_cap)
                if u_fee > 0: payload["fee"] = float(u_fee)
                res = requests.put(f"{API_BASE_URL}/courses/{u_c_id}", json=payload)
                if res.status_code == 200:
                    st.success("Course updated!")
                    st.rerun()
                else:
                    st.error(res.json().get("detail", "Update failed."))

        # Delete Course (DELETE /courses/{course_id})
        with st.expander("🗑️ Delete Course"):
            del_c_id = st.number_input("Course ID to Delete", min_value=1, step=1, key="c_del_id")
            if st.button("Delete Course", type="primary", use_container_width=True):
                res = requests.delete(f"{API_BASE_URL}/courses/{del_c_id}")
                if res.status_code == 204:
                    st.success(f"Course ID {del_c_id} deleted.")
                    st.rerun()
                else:
                    st.error(res.json().get("detail", "Delete failed."))



elif section == "📝 Manage Enrollments":
    st.header("📝 Enrollment Management")
    
    col_left, col_right = st.columns([1.5, 1])
    
    # Left Column: View & Searches
    with col_left:
        st.subheader("Active Enrollment Records")
        
        search_mode = st.radio("Search Filter", ["View All Records", "Search by Enrollment ID", "Search by Student ID"], horizontal=True)
        
        # GET /enrollment/{enrollment_id}
        if search_mode == "Search by Enrollment ID":
            e_id = st.number_input("Enrollment ID", min_value=1, step=1, key="e_search_id")
            if st.button("Get Record"):
                res = requests.get(f"{API_BASE_URL}/enrollment/{e_id}")
                if res.status_code == 200:
                    st.json(res.json())
                else:
                    st.error(res.json().get("detail", "Enrollment record not found."))

        # GET /enrollment/student/{student_id}
        elif search_mode == "Search by Student ID":
            e_s_id = st.number_input("Student ID", min_value=1, step=1, key="e_search_s_id")
            if st.button("Get Student Enrollments"):
                res = requests.get(f"{API_BASE_URL}/enrollment/student/{e_s_id}")
                if res.status_code == 200:
                    st.dataframe(res.json(), use_container_width=True)
                else:
                    st.error(res.json().get("detail", "No enrollments found for this student."))

        # GET /enrollment/
        else:
            res = requests.get(f"{API_BASE_URL}/enrollment/")
            if res.status_code == 200:
                st.dataframe(res.json(), use_container_width=True)
            else:
                st.error("Unable to load enrollments.")

    # Right Column: Actions (Create & Delete)
    with col_right:
        # Create Enrollment (POST /enrollment/)
        with st.expander("📝 Enroll Student in Course", expanded=True):
            enr_stu_id = st.number_input("Student ID", min_value=1, step=1, key="e_enr_stu")
            enr_crs_id = st.number_input("Course ID", min_value=1, step=1, key="e_enr_crs")
            if st.button("Submit Enrollment", use_container_width=True):
                res = requests.post(f"{API_BASE_URL}/enrollment/", json={"student_id": int(enr_stu_id), "course_id": int(enr_crs_id)})
                if res.status_code == 201:
                    st.success("Enrollment Successful!")
                    st.rerun()
                else:
                    st.error(res.json().get("detail", "Enrollment failed."))

        # Delete Enrollment (DELETE /enrollment/{enrollment_id})
        with st.expander("❌ Cancel / Delete Enrollment"):
            del_e_id = st.number_input("Enrollment ID to Cancel", min_value=1, step=1, key="e_del_id")
            if st.button("Cancel Enrollment", type="primary", use_container_width=True):
                res = requests.delete(f"{API_BASE_URL}/enrollment/{del_e_id}")
                if res.status_code == 204:
                    st.success(f"Enrollment ID {del_e_id} canceled and seat restored.")
                    st.rerun()
                else:
                    st.error(res.json().get("detail", "Cancellation failed."))