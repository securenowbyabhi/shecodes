/**********************************************************************************************************
 * @file        ProjectComponent.jsx
 * @description Component to create new Project in the system
 * @team        SheCodes-Hub (MSITM'26 @ McComb School of Business, UT Austin)
 * @created     2025-07-26
 * @version     
 * v1.0.0       Initial Draft(Structure)           2025-07-26
 * v1.0.1       Developed the feature              2025-08-04
 **********************************************************************************************************/
import React,{useState,useEffect} from 'react';
import ReusableHeaderComponent from './ReusableHeaderComponent'
import { useOutletContext,useNavigate  } from 'react-router-dom';
import CancelButton from './CancelButton';

import { postToEndpoint } from "../utils/apiHelpers";
import { showSuccess, showError } from "../utils/toastUtils";

function ProjectComponent() {

  const { setIsLoggedIn } = useOutletContext();

    //setting context variable 'isLoggedIn' to true to have same tabs look and feel when user is loggedIn as compare to logged out of app
  useEffect(() => {
    setIsLoggedIn(true);
  }, [setIsLoggedIn]);
    
  const navigate = useNavigate();
  
  const [formData, setFormData] = useState({ projectid: "",projectname: "",description: "" });

  const handleChange = (event) => {
    setFormData({ ...formData, [event.target.name]: event.target.value });
  };

  //This will be passed via the props to the CancelButton component
  const resetForm = () => {
    setFormData({projectid: "",projectname: "",description: ""});
  };

  const handleSubmit = async (event) => {

    event.preventDefault();

    try {
      const { ok, data } = await postToEndpoint("createproject", {
        projectid: formData.projectid,
        projectname: formData.projectname,
        description: formData.description,
      });
    
      if (ok) {
        showSuccess(`Success: ${data.message}`);
        navigate("/resource");
      } else {
        showError(`Error: ${data.message || "Unknown error"}`);
      }
    } catch (error) {
      showError(`Error: ${error.message}`);
    }
  };

    return (
    <div style={{width: '80vw', maxWidth: '700px', margin: '40px auto'  }}>
        <ReusableHeaderComponent 
          title="Welcome to New Project page" 
          message="" 
        />
        <form onSubmit={handleSubmit}>

        <div style={{display: "flex", alignItems: "center", marginBottom: "10px", marginTop: "2rem"}}>
          <label style={{ width: "100px" }}>Project ID</label>
          <input
            type="text"
            name="projectid"
            value={formData.projectid}
            onChange={handleChange}
            required
          />
        </div>

        <div
          style={{
            display: "flex",
            alignItems: "center",
            marginBottom: "10px",
          }}
        >
          <label style={{ width: "100px" }}>Project Name</label>
          <input
            type="text"
            name="projectname"
            value={formData.projectname}
            onChange={handleChange}
            required
          />
        </div>


        <div
          style={{
            display: "flex",
            alignItems: "center",
            marginBottom: "10px",
          }}
        >
          <label style={{ width: "100px" }}>Description</label>
          <input
            type="text"
            name="description"
            value={formData.description}
            onChange={handleChange}
            required
          />
        </div>
        

        <button type="submit">
          Add Project
        </button>

        {/*Calling reusable CancelButton component*/}
        <CancelButton 
          resetForm={resetForm} 
          redirectTo="/resource" 
        />

      </form>

      </div>
    );
}
export default ProjectComponent;